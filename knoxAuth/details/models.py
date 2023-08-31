from django.db import models

# Create your models here.
# Create your models here.

class Employee(models.Model):
    def nameFile(instance, filename):
        return '/'.join(['images',str(instance.name),filename])
    empId = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.IntegerField()
    address = models.TextField(max_length=100)
    picture = models.ImageField(upload_to=nameFile,blank=True)
    # photo = models.ImageField(upload_to="pictures",blank=True)


    def __str__(self):
        return f"empId: {self.empId},name: {self.name},  phone: {self.phone}, email: {self.email}, address: {self.address} and picture:{self.picture}"


