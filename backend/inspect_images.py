#!/usr/bin/env python
"""Inspect stored image URLs and storage backend for Properties."""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from aurox.models import Properties

def inspect_property(p):
    print(f"Property {p.id}: {p.name}")
    for field in ('image1', 'image2', 'image3'):
        f = getattr(p, field)
        if not f:
            print(f"  {field}: <empty>")
            continue
        try:
            storage_name = type(f.storage).__name__
            url = f.url
            name = f.name
            print(f"  {field}: name={name} url={url} storage={storage_name}")
        except Exception as e:
            print(f"  {field}: error retrieving info: {e}")

def main():
    qs = Properties.objects.all()
    if not qs.exists():
        print("No Properties found in DB.")
        return
    for p in qs:
        inspect_property(p)
        print('-' * 40)

if __name__ == '__main__':
    main()
