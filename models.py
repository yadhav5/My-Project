from django.db import models
from django.utils import timezone

class Class(models.Model): 
    class_name = models.CharField(max_length=80, null=True) 
    class_numeric = models.IntegerField(null=True) 
    section = models.CharField(max_length=5, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    updation_date = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"{self.class_name} - {self.section}"



class Subject(models.Model):
    subject_name = models.CharField(max_length=100)
    subject_code = models.CharField(max_length=100, null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    updation_date = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.subject_name


class Student(models.Model):
    
    GENDER_CHOICES = (  
        ('Male', 'Male'), 
        ('Female', 'Female'),
    )
    name = models.CharField(max_length=100, null=True)
    roll_id = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100, null=True) 
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True)
    dob = models.CharField(max_length=100, null=True)
    student_class = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True)
    reg_date = models.DateTimeField(auto_now_add=True) 
    updation_date = models.DateTimeField(auto_now=True, null=True)
    status = models.IntegerField(default=1) 

    def __str__(self):
        return self.name


class SubjectCombination(models.Model):
    student_class = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    status = models.IntegerField(default=1)
    creation_date = models.DateTimeField(auto_now_add=True)
    updation_date = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"{self.student_class} - {self.subject}"


class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    student_class = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    marks = models.IntegerField(null=True)
    posting_date = models.DateTimeField(auto_now_add=True)
    updation_date = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"{self.student} - {self.subject} - {self.marks}"


class Notice(models.Model):
    title = models.CharField(max_length=255, null=True)
    details = models.TextField(null=True)
    posting_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
