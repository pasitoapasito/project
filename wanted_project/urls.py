from django.urls import path, include

urlpatterns = [
    path('companies', include('companies.urls')),
    path('applications', include('applications.urls')),
]
