from django.db import models

class ImageHash(models.Model):
    image_url = models.URLField()
    md5_hash = models.CharField(max_length=32)
    phash = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Image Hash"
        verbose_name_plural = "Image Hashes"

    def __str__(self):
        return f"Image: {self.image_url} (MD5: {self.md5_hash})"
