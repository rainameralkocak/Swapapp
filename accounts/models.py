from django.db import models
from datetime import datetime
from django.contrib.auth.models import User


class InstructorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    # Add any other fields relevant to instructors


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    enrollment_date = models.DateField()
    # Add any other fields relevant to students


class Category(models.Model):
    name = models.CharField(max_length=255)
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                                        related_name='subcategories')
    image_path = models.TextField(null=True, blank=True)


class Course(models.Model):
    name = models.CharField(max_length=150)
    # category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, default=None)
    categories = models.ManyToManyField(Category, related_name='courses')
    instructor = models.ForeignKey(InstructorProfile, on_delete=models.CASCADE, default=None)
    details = models.CharField(max_length=150)
    rating = models.FloatField()
    price = models.FloatField()
    image_path = models.CharField(max_length=300, default=None)


class Purchase(models.Model):
    date = models.DateTimeField()
    item = models.ForeignKey(Course, on_delete=models.DO_NOTHING, default=None)
    student = models.ForeignKey(StudentProfile, on_delete=models.DO_NOTHING, default=None)




class Meeting(models.Model):
    date = models.DateTimeField(default=None, null=True, blank=True)
    url = models.CharField(max_length=150, default=None, null=True, blank=True)
    video_url = models.CharField(max_length=200, default=None, null=True, blank=True)
    status = models.CharField(max_length=20, default="WaitingInstructor")
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, default=None,related_name='meetings')

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, related_name='notifications', null=True, blank=True)

class CreditCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    card_name = models.CharField(max_length=100, default=None)
    card_icon_url = models.CharField(max_length=300, default=None)
    owner_name = models.CharField(max_length=100)
    card_number = models.CharField(max_length=19)
    cvv = models.CharField(max_length=3)
    expiry = models.CharField(max_length=5)


class UserDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=150, default=None, null=True, blank=True)
    phone = models.CharField(max_length=20, default=None, null=True, blank=True)
    country = models.CharField(max_length=20, default=None, null=True, blank=True)
    city = models.CharField(max_length=20, default=None, null=True, blank=True)
