from django.db   import models
from core.models import TimeStampModel

class Application(TimeStampModel):
    
    STATUS_TYPES = [
        ('application_complete', 'Application Complete'),
        ('application_fail', 'Application Fail'),
        ('document_pass', 'Document Pass'),
        ('final_pass', 'Final Pass'),
    ]
    
    users              = models.ForeignKey('users.User', on_delete=models.CASCADE)
    job_positions      = models.ForeignKey('companies.Position', on_delete=models.CASCADE)
    application_status = models.CharField(max_length=200, choices=STATUS_TYPES, default='application_complete')

    class Meta:
        db_table = 'applications'
        

class ResumeApplication(TimeStampModel):
    resumes      = models.ForeignKey('users.Resume', on_delete=models.CASCADE)
    applications = models.ForeignKey('applications.Application', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'resume_application'