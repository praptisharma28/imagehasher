from rest_framework import generics, status
from rest_framework.response import Response
from .models import ImageHash
from .serializers import ImageHashSerializer
from .utils import calculate_image_hashes

class ImageHashListCreateView(generics.ListCreateAPIView):
    queryset = ImageHash.objects.all()
    serializer_class = ImageHashSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            # Calculate hashes
            md5_hash, phash = calculate_image_hashes(serializer.validated_data['image_url'])
            
            # Save to database
            instance = serializer.save(
                md5_hash=md5_hash,
                phash=phash
            )
            
            # Return response with hashes
            return Response({
                "status": "success",
                "data": {
                    "id": instance.id,
                    "image_url": instance.image_url,
                    "md5_hash": instance.md5_hash,
                    "phash": instance.phash,
                    "created_at": instance.created_at,
                    "updated_at": instance.updated_at
                }
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({
                "status": "error",
                "detail": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

class ImageHashDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ImageHash.objects.all()
    serializer_class = ImageHashSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        return Response({
            "status": "success",
            "data": {
                "id": instance.id,
                "image_url": instance.image_url,
                "md5_hash": instance.md5_hash,
                "phash": instance.phash,
                "created_at": instance.created_at,
                "updated_at": instance.updated_at
            }
        })

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        try:
            # Recalculate hashes for new URL
            md5_hash, phash = calculate_image_hashes(serializer.validated_data['image_url'])
            
            # Save updated data
            instance = serializer.save(
                md5_hash=md5_hash,
                phash=phash
            )
            
            return Response({
                "status": "success",
                "data": {
                    "id": instance.id,
                    "image_url": instance.image_url,
                    "md5_hash": instance.md5_hash,
                    "phash": instance.phash,
                    "created_at": instance.created_at,
                    "updated_at": instance.updated_at
                }
            })
        except Exception as e:
            return Response({
                "status": "error",
                "detail": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({
            "status": "success",
            "detail": "Image hash deleted successfully"
        }, status=status.HTTP_200_OK)
