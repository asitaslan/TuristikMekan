from django.contrib import admin

# Register your models here.
from mekan.models import Mekan, Category, Images


class MekanImageInLine(admin.TabularInline):
    model = Images
    extra = 5

class CategoryAdmin(admin.ModelAdmin):
    list_display= ['title', 'status']
    list_filter = ['status']

class MekanAdmin(admin.ModelAdmin):
    list_display= ['title', 'category',  'image_tag', 'status']
    readonly_fields = ('image_tag',)
    list_filter = ['status', 'category']
    inlines = [MekanImageInLine]

class ImagesAdmin(admin.ModelAdmin):
    list_display = ['title', 'mekan', 'image']

admin.site.register(Mekan, MekanAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Images,ImagesAdmin)
