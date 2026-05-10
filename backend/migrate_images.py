#!/usr/bin/env python
"""Re-save Property image fields so they are uploaded to configured storage."""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.core.files import File
from aurox.models import Properties

def migrate():
    qs = Properties.objects.all()
    count = qs.count()
    print(f"Found {count} properties. Processing...")
    for p in qs:
        changed = False
        print(f"Processing Property {p.id}: {p.name}")
        for field_name in ('image1','image2','image3'):
            f = getattr(p, field_name)
            if not f:
                print(f"  {field_name}: empty")
                continue
            # If the URL already looks like a cloudinary URL, skip
            try:
                url = f.url
            except Exception:
                url = ''
            if url.startswith('http') and 'res.cloudinary.com' in url:
                print(f"  {field_name}: already on Cloudinary ({url})")
                continue

            file_path = f.path if hasattr(f, 'path') else None
            if not file_path or not os.path.exists(file_path):
                print(f"  {field_name}: local file not found: {file_path}")
                continue

            print(f"  {field_name}: uploading {file_path} to storage...")
            with open(file_path, 'rb') as fh:
                django_file = File(fh)
                # Save using the same name to the configured storage
                getattr(p, field_name).save(os.path.basename(f.name), django_file, save=False)
                changed = True

        if changed:
            p.save()
            print(f"  Saved Property {p.id} -> images migrated.")
        else:
            print(f"  No changes for Property {p.id}.")

if __name__ == '__main__':
    migrate()
