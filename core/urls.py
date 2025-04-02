from django.urls import path
from . import views

urlpatterns = [
    path('complaints/', views.complaint_list, name='complaint_list'),
    path('complaints/create/', views.complaint_create, name='complaint_create'),
    path('complaints/<uuid:complaint_id>/', views.complaint_detail, name='complaint_detail'),
    path('complaints/<uuid:complaint_id>/update/', views.complaint_update, name='complaint_update'),
    path('complaints/<uuid:complaint_id>/delete/', views.complaint_delete, name='complaint_delete'),
]