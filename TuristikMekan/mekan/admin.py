from django.contrib import admin

# Register your models here.
from mptt.admin import DraggableMPTTAdmin

from mekan.models import Mekan, Category, Images


class MekanImageInLine(admin.TabularInline):
    model = Images
    extra = 5

class CategoryAdmin(admin.ModelAdmin):
    list_display= ['title', 'status']
    list_filter = ['status']

class CategoryAdmin2(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ('tree_actions', 'indented_title',
                    'related_mekans_count', 'related_mekans_cumulative_count')
    list_display_links = ('indented_title',)
    prepopulated_fields = {'slug': ('title',)}

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category.objects.add_related_count(
            qs,
            Mekan,
            'category',
            'mekans_cumulative_count',
            cumulative=True)

        # Add non cumulative product count
        qs = Category.objects.add_related_count(qs,
                                                Mekan,
                                                'category',
                                                'mekans_count',
                                                cumulative=False)
        return qs

    def related_mekans_count(self, instance):
        return instance.mekans_count

    related_mekans_count.short_description = 'Related mekans (for this specific category)'

    def related_mekans_cumulative_count(self, instance):
        return instance.mekans_cumulative_count

    related_mekans_cumulative_count.short_description = 'Related mekans (in tree)'

class MekanAdmin(admin.ModelAdmin):
    list_display= ['title', 'category',  'image_tag', 'status']
    readonly_fields = ('image_tag',)
    list_filter = ['status', 'category']
    inlines = [MekanImageInLine]

class ImagesAdmin(admin.ModelAdmin):
    list_display = ['title', 'mekan', 'image']

admin.site.register(Mekan, MekanAdmin)
admin.site.register(Category, CategoryAdmin2)
admin.site.register(Images,ImagesAdmin)
