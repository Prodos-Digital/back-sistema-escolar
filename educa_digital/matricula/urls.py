# matricula/urls.py
from django.urls import path
from .views import EnrollmentCreateView, EnrollmentDetailView, EnrollmentDocumentsView

urlpatterns = [
    path('enrollment/', EnrollmentCreateView.as_view(), name='enrollment-create'),
    path('enrollment/<int:pk>/', EnrollmentDetailView.as_view(), name='enrollment-detail'),
    path('enrollment/documents/', EnrollmentDocumentsView.as_view(), name='enrollment-documents'),
]
