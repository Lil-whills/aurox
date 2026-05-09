#!/usr/bin/env python
"""Test Cloudinary configuration and upload functionality."""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.conf import settings
from decouple import AutoConfig
import cloudinary.uploader

# Test 1: Check if env vars are loaded
print("=" * 60)
print("TEST 1: Environment Variables")
print("=" * 60)

_decouple = AutoConfig(search_path='.')
cloud_name = _decouple('CLOUDINARY_CLOUD_NAME', default='NOT_FOUND')
api_key = _decouple('CLOUDINARY_API_KEY', default='NOT_FOUND')
api_secret = _decouple('CLOUDINARY_API_SECRET', default='NOT_FOUND')[:10] + '***'  # Hide secret

print(f"CLOUDINARY_CLOUD_NAME: {cloud_name}")
print(f"CLOUDINARY_API_KEY: {api_key}")
print(f"CLOUDINARY_API_SECRET: {api_secret}...")

# Test 2: Check Django settings
print("\n" + "=" * 60)
print("TEST 2: Django Settings")
print("=" * 60)

print(f"DEFAULT_FILE_STORAGE: {settings.DEFAULT_FILE_STORAGE}")
print(f"CLOUDINARY_STORAGE: {settings.CLOUDINARY_STORAGE}")
print(f"DEBUG: {settings.DEBUG}")

# Test 3: Try uploading a test file
print("\n" + "=" * 60)
print("TEST 3: Cloudinary Upload Test")
print("=" * 60)

try:
    import cloudinary
    cloudinary.config(
        cloud_name=settings.CLOUDINARY_STORAGE['CLOUD_NAME'],
        api_key=settings.CLOUDINARY_STORAGE['API_KEY'],
        api_secret=settings.CLOUDINARY_STORAGE['API_SECRET'],
    )
    
    # Check if test image exists
    test_image_path = 'media/property_images/house10.jpg'
    if os.path.exists(test_image_path):
        print(f"Uploading test image: {test_image_path}")
        result = cloudinary.uploader.upload(test_image_path, folder='test')
        print(f"✅ Upload successful!")
        print(f"   URL: {result.get('url')}")
        print(f"   Public ID: {result.get('public_id')}")
    else:
        print(f"❌ Test image not found: {test_image_path}")
        print("   Try uploading a property via admin instead.")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("DONE")
print("=" * 60)
