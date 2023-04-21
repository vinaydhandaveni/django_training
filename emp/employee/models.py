from django.db import models
from django.db import models 

class Dept(models.Model):
    edept=models.CharField(max_length=20,primary_key=True)
    edepname=models.CharField(max_length=20)
    owner = models.ForeignKey('auth.User', related_name='department', on_delete=models.CASCADE)
    def __str__(self):
        return self.edept

class Employee(models.Model):  
    eid = models.CharField(max_length=20)  
    ename = models.CharField(max_length=100)  
    eemail = models.EmailField()  
    edept= models.ForeignKey(Dept,on_delete=models.CASCADE,null=True)
    econtact = models.CharField(max_length=15) 
    owner = models.ForeignKey('auth.User', related_name='employee', on_delete=models.CASCADE)
    def __str__(self):
        return self.ename 
# Create your models here.
