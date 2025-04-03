from django.urls import path
from .views import *

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/',logout_view, name='logout'),
    path('complaints/', ComplaintListView.as_view(), name='complaint-list'),
    path('complaints/create/', complaint_create, name='complaint-create'),
    path('complaints/<uuid:complaint_id>/', complaint_detail, name='complaint-detail'),
    path('complaints/<uuid:complaint_id>/update/', complaint_update, name='complaint-update'),
    path('complaints/<uuid:complaint_id>/delete/', complaint_delete, name='complaint-delete'),
]
