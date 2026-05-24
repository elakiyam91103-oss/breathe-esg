from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from .models import Client, DataIngestion, EmissionRecord, AuditLog
from .parsers import parse_sap, parse_utility, parse_travel
from .serializers import EmissionRecordSerializer, DataIngestionSerializer, ClientSerializer

class ClientListView(APIView):
    def get(self, request):
        clients = Client.objects.all()
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

class UploadView(APIView):
    def post(self, request):
        source_type = request.data.get('source_type')
        file = request.FILES.get('file')
        client_id = request.data.get('client_id', 1)

        try:
            client = Client.objects.get(id=client_id)
        except Client.DoesNotExist:
            client = Client.objects.create(name='Default Client')

        ingestion = DataIngestion.objects.create(
            client=client,
            source_type=source_type,
            uploaded_by=None,
            file_name=file.name,
        )

        parsers = {
            'SAP': parse_sap,
            'UTILITY': parse_utility,
            'TRAVEL': parse_travel
        }
        parser = parsers.get(source_type)

        if not parser:
            return Response({'error': 'Invalid source type'}, status=400)

        records_data = parser(file)
        created = 0
        for r in records_data:
            flag = r.pop('flag_reason', '')
            EmissionRecord.objects.create(
                client=client,
                ingestion=ingestion,
                flag_reason=flag,
                status='FLAGGED' if flag else 'PENDING',
                **r,
            )
            created += 1

        ingestion.row_count = created
        ingestion.save()

        return Response({'ingestion_id': ingestion.id, 'rows_created': created})

class RecordsView(APIView):
    def get(self, request):
        records = EmissionRecord.objects.all().order_by('-created_at')
        source = request.query_params.get('source_type')
        status_filter = request.query_params.get('status')
        if source:
            records = records.filter(source_type=source)
        if status_filter:
            records = records.filter(status=status_filter)
        serializer = EmissionRecordSerializer(records, many=True)
        return Response(serializer.data)

class ReviewView(APIView):
    def patch(self, request, pk):
        try:
            record = EmissionRecord.objects.get(pk=pk)
        except EmissionRecord.DoesNotExist:
            return Response({'error': 'Not found'}, status=404)

        if record.is_locked:
            return Response({'error': 'Record is locked for audit'}, status=400)

        new_status = request.data.get('status')
        old_status = record.status

        AuditLog.objects.create(
            record=record,
            changed_by=None,
            field_changed='status',
            old_value=old_status,
            new_value=new_status,
        )

        record.status = new_status
        record.reviewed_at = timezone.now()
        record.save()

        return Response({'success': True, 'new_status': new_status})

class StatsView(APIView):
    def get(self, request):
        total = EmissionRecord.objects.count()
        pending = EmissionRecord.objects.filter(status='PENDING').count()
        approved = EmissionRecord.objects.filter(status='APPROVED').count()
        flagged = EmissionRecord.objects.filter(status='FLAGGED').count()
        rejected = EmissionRecord.objects.filter(status='REJECTED').count()

        scope1 = sum(r.normalized_kgco2e for r in EmissionRecord.objects.filter(scope=1))
        scope2 = sum(r.normalized_kgco2e for r in EmissionRecord.objects.filter(scope=2))
        scope3 = sum(r.normalized_kgco2e for r in EmissionRecord.objects.filter(scope=3))

        return Response({
            'total': total,
            'pending': pending,
            'approved': approved,
            'flagged': flagged,
            'rejected': rejected,
            'scope1_kgco2e': round(scope1, 2),
            'scope2_kgco2e': round(scope2, 2),
            'scope3_kgco2e': round(scope3, 2),
        })
