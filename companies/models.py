from django.db   import models
from core.models import TimeStampModel

class Company(TimeStampModel):
    name        = models.CharField(max_length=200)
    location    = models.CharField(max_length=200)
    country     = models.CharField(max_length=200)
    image_url   = models.CharField(max_length=2000, null=True)
    description = models.CharField(max_length=1000, null=True)
    
    class Meta:
        db_table = 'companies'
    

class Position(TimeStampModel):
    
    STATUS_TYPES = [
        ('under_recruitment', 'Under Recruitment'),
        ('recruitment_ended', 'Recruitment Ended'),
        ('deleted', 'Deleted'),
    ]
    
    title         = models.CharField(max_length=200)
    description   = models.CharField(max_length=1000)
    position      = models.CharField(max_length=200)
    technology    = models.CharField(max_length=200)
    status        = models.CharField(max_length=200, choices=STATUS_TYPES, default='under_recruitment')
    compensation  = models.PositiveIntegerField()
    due_date      = models.DateField()
    companies     = models.ForeignKey('companies.Company', on_delete=models.CASCADE)
    subcategories = models.ForeignKey('companies.Subcategory', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'job_positions'


class Subcategory(models.Model):
    name       = models.CharField(max_length=200)
    categories = models.ForeignKey('companies.Category', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'job_subcategories'
        
        
class Category(models.Model):
    name = models.CharField(max_length=200)
    
    class Meta:
        db_table = 'job_categories'   
