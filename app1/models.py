from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    contact_number = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        db_table="UserProfile"
    
class RIVUE(models.Model):
    ProModel = models.CharField(max_length=50)
    ProName = models.CharField(max_length=200)
    ProRev = models.CharField(max_length=1000)
    ProEmail = models.EmailField()
    ProCom = models.CharField(max_length=150)
    ProImage=models.FileField(upload_to='images/',default=r"D:\DBMS\RIVUE-main\registration\media\images\notes.png")
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=1)

    class Meta:
        db_table="RIVUE"


