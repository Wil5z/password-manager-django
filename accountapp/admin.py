from django.contrib import admin
from .models import Savedpasswords


# Register your models here.


class SavedpasswordsAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("domain",)}

admin.site.register(Savedpasswords,SavedpasswordsAdmin)
