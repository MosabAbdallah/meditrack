from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('add/', views.add_patient, name='add_patient'),
    path('<int:patient_id>/', views.patient_detail, name='patient_detail'),
    path('<int:patient_id>/edit/', views.edit_patient, name='edit_patient'),
    path('<int:patient_id>/delete/', views.delete_patient, name='delete_patient'),
    path('<int:patient_id>/add_vital/', views.add_vital, name='add_vital'),
    path('api/vitals/<int:patient_id>/', views.vitals_api, name='vitals_api')
]
