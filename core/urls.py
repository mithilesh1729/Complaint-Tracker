from django.urls import path
from . import views

urlpatterns = [
    path('api/complaints/', views.complaint_list, name='complaint_list'),
    path('api/complaints/create/', views.complaint_create, name='complaint_create'),
    path('api/complaints/<uuid:complaint_id>/', views.complaint_detail, name='complaint_detail'),
    path('api/complaints/<uuid:complaint_id>/update/', views.complaint_update, name='complaint_update'),
    path('api/complaints/<uuid:complaint_id>/delete/', views.complaint_delete, name='complaint_delete'),
]