from django.db import models
from django.conf import settings
# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser

class Prefix(models.Model):
    prefix = models.CharField(max_length=5)
    effective_date = models.DateField(null = True)
    ineffective_date = models.DateField(null = True)

class Gender(models.Model):
    gender = models.CharField(max_length=10)
    effective_date = models.DateField(null = True)
    ineffective_date = models.DateField(null = True)

class MaritalStatus(models.Model):
    marital_status = models.CharField(max_length=10)
    effective_date = models.DateField(null = True)
    ineffective_date = models.DateField(null = True)

class Qualification(models.Model):
    qualification = models.CharField(max_length=25)
    effective_date = models.DateField(null = True)
    ineffective_date = models.DateField(null = True)

class Profession(models.Model):
    profession = models.CharField(max_length=25)
    effective_date = models.DateField(null = True)
    ineffective_date = models.DateField(null = True)

class Role(models.Model):
    role = models.CharField(max_length=30)
    effective_date = models.DateField(null = True)
    ineffective_date = models.DateField(null = True)

class Product(models.Model):
    product = models.CharField(max_length=25)
    effective_date = models.DateField(null = True)
    ineffective_date = models.DateField(null = True)

class SubProduct(models.Model):
    sub_product = models.CharField(max_length=25)
    effective_date = models.DateField(null = True)
    ineffective_date = models.DateField(null = True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

class CustomerType(models.Model):
    cust_type = models.CharField(max_length=25)
    effective_date = models.DateField(null = True)
    ineffective_date = models.DateField(null = True)

class DesignationType(models.Model):
    desg_type = models.CharField(max_length=25)
    effective_date = models.DateField(null = True)
    ineffective_date = models.DateField(null = True)

class CompanyType(models.Model):
    company_type = models.CharField(max_length=30)
    effective_date = models.DateField(null = True)
    ineffective_date = models.DateField(null = True)

class SalaryType(models.Model):
    salary_type = models.CharField(max_length=25)
    effective_date = models.DateField(null = True)
    ineffective_date = models.DateField(null = True)

class ResidenceType(models.Model):
    residence_type = models.CharField(max_length=25)
    effective_date = models.DateField(null = True)
    ineffective_date = models.DateField(null = True)

class BankName(models.Model):
    bank_name = models.CharField(max_length=25)
    effective_date = models.DateField(null = True)
    ineffective_date = models.DateField(null = True)

class LeadSource(models.Model):
    lead_source = models.CharField(max_length=25)
    effective_date = models.DateField(null = True)
    ineffective_date = models.DateField(null = True)

class Degree(models.Model):
    degree = models.CharField(max_length=25)
    effective_date = models.DateField(null = True)
    ineffective_date = models.DateField(null = True)

class Nationality(models.Model):
    nationality = models.CharField(max_length=25)
    effective_date = models.DateField(null = True)
    ineffective_date = models.DateField(null = True)    

class State(models.Model):
    state = models.CharField(max_length=25)
    effective_date = models.DateField(null = True)
    ineffective_date = models.DateField(null = True)

class City(models.Model):
    city_name = models.CharField(max_length=25)
    effective_date = models.DateField(null = True)
    ineffective_date = models.DateField(null = True)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

class ApplicantType(models.Model):
    applicant_type = models.CharField(max_length=25)
    effective_date = models.DateField(null = True)
    ineffective_date = models.DateField(null = True)

class PropertyIn(models.Model):
    property_in = models.CharField(max_length=25)
    effective_date = models.DateField(null = True)
    ineffective_date = models.DateField(null = True)

class Status(models.Model):
    status = models.CharField(max_length=55)
    effective_date = models.DateField(null = True)
    ineffective_date = models.DateField(null = True)

class NatureOfBusiness(models.Model):
    nature_business = models.CharField(max_length=25)
    effective_date = models.DateField(null = True)
    ineffective_date = models.DateField(null = True)

class AYYear(models.Model):
    ay_year = models.CharField(max_length=7)
    effective_date = models.DateField(null = True)
    ineffective_date = models.DateField(null = True)

class AgreementType(models.Model):
    agreement_type = models.CharField(max_length=25)
    effective_date = models.DateField(null = True)
    ineffective_date = models.DateField(null = True)

class StageOfConstruction(models.Model):
    stage = models.CharField(max_length=25)
    effective_date = models.DateField(null = True)
    ineffective_date = models.DateField(null = True)

class RejectionType(models.Model):
    rejection_type = models.CharField(max_length=45)
    rejection_reason = models.CharField(max_length=60)
    effective_date = models.DateField(null = True)
    ineffective_date = models.DateField(null = True)
# Create your models here.
