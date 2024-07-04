from django.contrib import admin
from .models import Tour, TourPhoto
# Register your models here.



class TourPhotoInline(admin.TabularInline):
    model = TourPhoto
    extra = 1

class TourAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'keyword', 'location', 'price', 'date', 'time']
    inlines = [TourPhotoInline]

admin.site.register(Tour, TourAdmin)
admin.site.register(TourPhoto)