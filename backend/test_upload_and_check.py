import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from cloudinary import uploader
from django.core.files.storage import default_storage

p = 'media/property_images/house10.jpg'
print('exists', os.path.exists(p))
res = uploader.upload(p, folder='property_images_migrate')
print('upload res url', res.get('url'))
print('public_id', res.get('public_id'))
print('default_storage.url(public_id)=', default_storage.url(res.get('public_id')))
