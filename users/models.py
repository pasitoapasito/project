from django.db   import models
from core.models import TimeStampModel

class User(TimeStampModel):
    name          = models.CharField(max_length=200)
    phone_number  = models.CharField(max_length=200, null=True)
    email         = models.CharField(max_length=200, null=True)
    profile_image = models.CharField(max_length=200, null=True)
    career        = models.PositiveIntegerField(null=True)
    salary        = models.PositiveIntegerField(null=True)
    
    class Meta:
        db_table = 'users'
        

class Resume(TimeStampModel):
    name     = models.CharField(max_length=200)
    file_url = models.CharField(max_length=2000)
    users    = models.ForeignKey('users.User', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'resumes'
        

    
        
    