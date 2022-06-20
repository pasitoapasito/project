from django.urls        import path
from applications.views import ApplicationView

urlpatterns = [
    path('/<int:job_position_id>', ApplicationView.as_view()),
]
