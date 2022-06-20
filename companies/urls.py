from django.urls     import path
from companies.views import JobPositionView, JobPositionListView, JobPositionDetailView

urlpatterns = [
    path('/positions', JobPositionListView.as_view()),
    path('/position/<int:job_position_id>', JobPositionDetailView.as_view()),
    path('/position', JobPositionView.as_view()),
]

