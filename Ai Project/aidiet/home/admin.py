from django.contrib import admin

# Register your models here.
from home.models import Registration
from home.models import UserBookData

admin.site.register(Registration)
admin.site.register(UserBookData)
