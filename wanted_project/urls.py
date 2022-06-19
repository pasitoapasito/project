from django.urls import path, include

urlpatterns = [
    path('companies', include('companies.urls')),
]
