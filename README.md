# Havemont / Aurox

Havemont is a Django-based real estate platform for browsing and managing property listings with a polished, media-first presentation. It supports property discovery, detail pages, bookmarks, authentication, contact and subscription forms, and an admin dashboard for staff users.

The project is centered in the `backend/` directory. Media files are handled through Cloudinary, static assets are served with WhiteNoise, and the UI is built with Django templates and Tailwind CDN styling.

## Features

- Property listing pages with search, filtering, sorting, and category support.
- Detailed property pages with multiple images, ratings, pricing, and virtual tour links.
- User signup, login, logout, and saved-property bookmarks.
- Contact form and email subscription capture.
- Admin-only dashboard for managing property inventory and reviewing platform stats.
- Cloudinary-backed image storage with support for legacy/local media migration scripts.

## Tech Stack

- Python 3.11+
- Django 6.0
- PostgreSQL
- Cloudinary for media storage
- WhiteNoise for static file serving
- `django-decouple` and `dj-database-url` for environment-based configuration

## Project Layout

```text
aurox/
├── backend/
│   ├── manage.py
│   ├── myproject/
│   ├── aurox/
│   ├── templates/
│   ├── static/
│   ├── requirements.txt
│   └── build.sh
└── frontend/
```

Key app files:

- `backend/aurox/models.py` defines properties, saved properties, contact messages, and subscribers.
- `backend/aurox/views.py` contains the homepage, listings, property details, bookmarks, auth, contact, and dashboard logic.
- `backend/aurox/urls.py` maps the public routes.
- `backend/myproject/settings.py` configures environment variables, database access, static files, and Cloudinary storage.

## Prerequisites

- Python 3.11 or later
- PostgreSQL
- Cloudinary account and API credentials

## Environment Variables

Create a `.env` file in `backend/` with values like these:

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgresql://user:password@localhost:5432/aurox_db

CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret

CSRF_TRUSTED_ORIGINS=http://localhost:8000
```

If you are deploying to Render or another hosted platform, set `DATABASE_URL` and `RENDER_EXTERNAL_HOSTNAME` there as well.

## Local Setup

From the `backend/` directory:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Then open `http://127.0.0.1:8000/` in your browser.

## Database and Static Files

- Run migrations after pulling schema changes: `python manage.py migrate`.
- Collect static files for production builds: `python manage.py collectstatic`.
- The build script `backend/build.sh` performs both dependency installation and production setup steps.

## Useful Management and Utility Scripts

The backend includes a few helper scripts for working with images and Cloudinary:

- `backend/migrate_images.py` re-saves property images so they move through the configured storage backend.
- `backend/migrate_to_cloudinary.py` uploads local property images to Cloudinary and stores remote URLs.
- `backend/inspect_images.py` inspects image fields on property records.
- `backend/test_cloudinary.py` checks Cloudinary configuration and upload flow.
- `backend/test_upload_and_check.py` runs a direct upload test.

## Main Routes

- `/` - homepage
- `/properties/` - searchable and filterable property listings
- `/propertydetail/<id>/` - property detail view
- `/bookmarks/` - saved properties for logged-in users
- `/contact/` - contact form
- `/about/` - about page
- `/services/` - services page
- `/login/`, `/signup/`, `/logout/` - authentication
- `/dashboard/` - staff/admin dashboard

## Admin

Create a superuser, then visit `/admin/` to manage:

- Properties
- Saved properties
- Contact messages
- Subscribers

## Deployment Notes

- `DEBUG` should be `False` in production.
- Set a strong `SECRET_KEY`.
- Provide a production `DATABASE_URL`.
- Configure Cloudinary credentials before uploading media.
- Ensure static files are collected during build or release.

## License

No explicit license is provided in this repository.