from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import CustomUser, Leads

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Leads)