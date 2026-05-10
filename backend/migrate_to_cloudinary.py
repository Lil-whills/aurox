#!/usr/bin/env python
"""Upload local Property images to Cloudinary and save remote URLs to new model fields.

Run from backend/: `python migrate_to_cloudinary.py`
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from cloudinary import uploader
from aurox.models import Properties


def upload_file(path):
    try:
        res = uploader.upload(path)
        return res.get('secure_url') or res.get('url')
    except Exception as e:
        print(f"    Upload error for {path}: {e}")
        return None


def migrate():
    qs = Properties.objects.all()
    print(f"Found {qs.count()} properties")
    for p in qs:
        changed = False
        print(f"Processing Property {p.id}: {p.name}")
        for idx, field_name in enumerate(('image1','image2','image3'), start=1):
            local_field = getattr(p, field_name)
            remote_field = f'image{idx}_remote_url'
            current_remote = getattr(p, remote_field)

            if current_remote:
                print(f"  {field_name}: already has remote URL")
                continue

            if not local_field:
                print(f"  {field_name}: empty")
                continue

            # If field.url is remote already, store it
            try:
                url = local_field.url
            except Exception:
                url = ''

            if url.startswith('http') and 'res.cloudinary.com' in url:
                print(f"  {field_name}: already on Cloudinary: {url}")
                setattr(p, remote_field, url)
                changed = True
                continue

            # If we have a local path, upload via cloudinary.uploader
            file_path = getattr(local_field, 'path', None)
            if not file_path or not os.path.exists(file_path):
                print(f"  {field_name}: local file not found: {file_path}")
                continue

            print(f"  {field_name}: uploading {file_path} to Cloudinary...")
            uploaded_url = upload_file(file_path)
            if uploaded_url:
                setattr(p, remote_field, uploaded_url)
                changed = True
                print(f"    uploaded -> {uploaded_url}")

        if changed:
            p.save()
            print(f"  Saved changes for Property {p.id}")


if __name__ == '__main__':
    migrate()
