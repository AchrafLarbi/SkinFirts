

from django.contrib import admin

from .models import Doctor, FavoriteDoctor, Review

# Register your models here.

admin.site.register(Doctor)
admin.site.register(Review)
admin.site.register(FavoriteDoctor)