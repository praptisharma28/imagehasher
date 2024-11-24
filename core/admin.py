from django.contrib import admin
from .models import ImageHash

@admin.register(ImageHash)
class ImageHashAdmin(admin.ModelAdmin):
    list_display = ['image_url', 'md5_hash', 'phash', 'created_at', 'updated_at']
    search_fields = ['image_url', 'md5_hash', 'phash']
    readonly_fields = ['md5_hash', 'phash', 'created_at', 'updated_at']
