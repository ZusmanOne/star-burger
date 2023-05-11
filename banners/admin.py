from django.contrib import admin
from .models import Banner

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
# Register your models here.
