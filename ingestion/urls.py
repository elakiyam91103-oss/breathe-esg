from django.urls import path
from .views import UploadView, RecordsView, ReviewView, StatsView, ClientListView

urlpatterns = [
    path('upload/', UploadView.as_view(), name='upload'),
    path('records/', RecordsView.as_view(), name='records'),
    path('records/<int:pk>/review/', ReviewView.as_view(), name='review'),
    path('stats/', StatsView.as_view(), name='stats'),
    path('clients/', ClientListView.as_view(), name='clients'),
]