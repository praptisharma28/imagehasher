from rest_framework import serializers
from .models import ImageHash

class ImageHashSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageHash
        fields = ['id', 'image_url', 'md5_hash', 'phash', 'created_at', 'updated_at']
        read_only_fields = ['md5_hash', 'phash', 'created_at', 'updated_at']

    def validate_image_url(self, value):
        if not value.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            raise serializers.ValidationError("URL must point to an image file")
        return value
