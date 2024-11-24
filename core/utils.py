import hashlib
import requests
import imagehash
from PIL import Image
from io import BytesIO
from rest_framework.exceptions import ValidationError

def calculate_image_hashes(image_url):
    """
    Download image from URL and calculate its MD5 and perceptual hash
    """
    try:
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()
        
        # Check content type
        content_type = response.headers.get('content-type', '')
        if not content_type.startswith('image/'):
            raise ValidationError("URL does not point to a valid image")
        
        image = Image.open(BytesIO(response.content))
        md5_hash = hashlib.md5(response.content).hexdigest()
        phash = str(imagehash.average_hash(image))
        
        return md5_hash, phash
        
    except requests.exceptions.RequestException as e:
        raise ValidationError(f"Failed to download image: {str(e)}")
    except Exception as e:
        raise ValidationError(f"Failed to process image: {str(e)}")

def calculate_hash_similarity(hash1, hash2):
    """Calculate similarity between two pHashes"""
    # Convert hexadecimal hashes to binary
    binary1 = bin(int(hash1, 16))[2:].zfill(64)
    binary2 = bin(int(hash2, 16))[2:].zfill(64)
    
    # Calculate Hamming distance
    matching_bits = sum(b1 == b2 for b1, b2 in zip(binary1, binary2))
    return matching_bits / 64.0  # Return similarity percentage
