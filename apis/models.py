from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime 

class Term(models.Model):
    name = models.CharField(max_length=255)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    year = models.DateField(null=True)
    
    def __str__(self):
        return f"{self.name} {self.year.strftime('%Y')}"
    
    def __detail__(self):
        tmp = datetime.strptime('9999-12-31','%Y-%m-%d')
        return {    'id' : self.id,
                    'name' : self.name ,
                    'year' : self.year.strftime('%Y') if self.year else 9999,
                    'start_date' : self.start_date if self.start_date else tmp,
                    'end_date' : self.end_date if self.end_date else tmp,
                }
    def  get_term_year(self):
        return self.year.strftime('%Y') if self.year else 9999

class Professor(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email_id = models.EmailField(max_length=254)
    phone_no = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.first_name} {self.last_name}" 
    
    def __detail__(self):
        return {    'id' : self.id ,
                    'first_name' : self.first_name ,
                    'last_name' : self.last_name ,
                    'email_id' : self.email_id ,
                    'phone_no' : self.phone_no ,
                }

class Subject(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    prof_name = models.ForeignKey(Professor, on_delete=models.SET_NULL,null=True)
    term = models.ForeignKey(Term, on_delete=models.SET_NULL,null=True)
    credits= models.IntegerField(null=True) 

    def __str__(self):
        return f"{self.code} {self.name}, {self.term}"
    
    def __for_xlx__(self):
        return f"{self.code} {self.name} : {self.term}"
    
    def __detail__(self):
        return {    'id' : self.id ,
                    'name' : self.name ,
                    'code' : self.code ,
                    'prof_id' : self.prof_name.id ,
                    'prof_name' : self.prof_name.__str__() ,
                    'term_id' : self.term.id ,
                    'term_name' : self.term.__str__() ,
                    'credits' : self.credits ,
                }
    def __comm_detail__(self):
        return {
                    'name' : self.name ,
                    'code' : self.code ,
                    'term_id' : self.term.id ,
                    'term_name' : self.term.__str__() ,
                    'credits' : self.credits ,
                }
    

class UserData(models.Model):
    # user_id 
    # user = models.ForeignKey(User, blank=True, on_delete=models.CASCADE)
    # id = models.IntegerField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='us_d', default='0000000')
    first_name = models.CharField(max_length=255)  # can be removed 
    last_name = models.CharField(max_length=255) # can be removed 
    start_term = models.ForeignKey(Term, related_name='start_t_user', on_delete=models.SET_NULL,null=True)
    expected_end_term = models.ForeignKey(Term, related_name='end_t_user', on_delete=models.SET_NULL,null=True)
    enrolled_subjects = models.ManyToManyField(Subject)
    # planned_subjects = models.ManyToManyField(Subject)

    # Add more fields as needed

    def __str__(self):
        return f"{self.first_name} {self.last_name}, {self.start_term}"
    
    def __detail__(self):
        return {    'id' : self.user.id ,
                    'first_name' : self.first_name ,
                    'last_name'  : self.last_name ,
                    'email_id'   : self.user.email,
                    'start_term_id' : self.start_term.id,
                    'start_term' : self.start_term.__str__()
                }

class Subscribed(models.Model):
    user = models.ForeignKey(UserData, related_name='subscribed_user', on_delete=models.SET_NULL,null=True)
    subject = models.ForeignKey(Subject, related_name='subscribed_subject', on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return f"{self.user.__str__()} -> {self.subject.__str__()}" 

    def __detail__(self):
        return {
            "user" : self.user.__detail__(),
            "subject" : self.subject.__detail__()
        }