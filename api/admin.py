from django.contrib import admin
from .models import User, Ingredient, Remedy

admin.site.register(User)
admin.site.register(Ingredient)
admin.site.register(Remedy)