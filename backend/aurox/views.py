from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Properties, SavedProperty, ContactMessage
from django.utils import timezone
import traceback
import logging


DEFAULT_VIRTUAL_TOUR_URL = "https://realsee.ai/nMnngDR5"

logger = logging.getLogger(__name__)


def _clean_param(request, *keys):
    """Return the first       n-empty query parameter from the provided keys."""
    for key in keys:
        value = request.GET.get(key, "")
        if value is not None:
            value = value.strip()
            if value:
                return value
    return ""


def _parse_price_range(price_range):
    """Parse supported price range formats like 1000-2000 and 4000+."""
    if not price_range:
        return None, None

    if price_range.endswith("+"):
        min_part = price_range[:-1].strip()
        if min_part.isdigit():
            return int(min_part), None
        return None, None

    if "-" in price_range:
        min_part, max_part = [p.strip() for p in price_range.split("-", 1)]
        if min_part.isdigit() and max_part.isdigit():
            return int(min_part), int(max_part)

    return None, None


def _apply_property_filters(request, queryset):
    """Apply search, filter, and sorting on a queryset using query params."""
    query = _clean_param(request, "q", "query")
    property_type = _clean_param(request, "type", "property_type", "access_type")
    category = _clean_param(request, "category")
    status = _clean_param(request, "status")
    area = _clean_param(request, "area", "location")
    price_range = _clean_param(request, "price", "price_range")
    sort = _clean_param(request, "sort") or "newest"

    valid_types = {choice[0] for choice in Properties._meta.get_field("type").choices}
    valid_categories = {choice[0] for choice in Properties._meta.get_field("category").choices}
    valid_statuses = {choice[0] for choice in Properties._meta.get_field("status").choices}

    if query:
        queryset = queryset.filter(
            Q(name__icontains=query)
            | Q(description__icontains=query)
            | Q(location__icontains=query)
        )

    if property_type in valid_types:
        queryset = queryset.filter(type=property_type)

    if category in valid_categories:
        queryset = queryset.filter(category=category)

    if status in valid_statuses:
        queryset = queryset.filter(status=status)

    if area:
        normalized_area = area.replace("-", " ")
        queryset = queryset.filter(location__icontains=normalized_area)

    min_price, max_price = _parse_price_range(price_range)
    if min_price is not None:
        queryset = queryset.filter(price__gte=min_price)
    if max_price is not None:
        queryset = queryset.filter(price__lte=max_price)

    sort_map = {
        "newest": "-created_at",
        "oldest": "created_at",
        "price_low": "price",
        "price_high": "-price",
        "rating_high": "-rating",
        "rating_low": "rating",
        "reviews_high": "-reviews",
    }
    queryset = queryset.order_by(sort_map.get(sort, "-created_at"))

    filters = {
        "q": query,
        "type": property_type,
        "category": category,
        "status": status,
        "area": area,
        "price_range": price_range,
        "sort": sort,
    }
    return queryset, filters


def _get_saved_property_ids(user):
    if not user.is_authenticated:
        return []
    return list(
        SavedProperty.objects.filter(user=user, is_paid=False).values_list('property_id', flat=True)
    )


# Create your views here.
def index(request):
    featured_queryset = Properties.objects.filter(is_featured=True).order_by('-created_at')
    saved_property_ids = _get_saved_property_ids(request.user)
    total_featured_count = featured_queryset.count()
    featured_properties = list(featured_queryset[:8])
    content = {
        'featured_properties': featured_properties,
        'featured_marquee_properties': featured_properties,
        'result_count': total_featured_count,
        'is_limited': total_featured_count > 6,
        'default_virtual_tour_url': DEFAULT_VIRTUAL_TOUR_URL,
        'saved_property_ids': saved_property_ids,
        'featured_trust_stats': [
            {'value': '24/7', 'label': 'always available discovery'},
            {'value': '100%', 'label': 'in-house property presentation'},
            {'value': '1 scan', 'label': 'complete virtual walkthrough'}
        ],
    }
    return render(request, 'index.html', content)

def about(request):
    return render(request, 'about.html')

def contact(request):
    context = {}
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        phone = request.POST.get('phone', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip() or 'Contact Form'
        message = request.POST.get('message', '').strip()

        full_message = f"""
Name: {name}

Phone: {phone}

Email: {email}

Subject: {subject}

Message:
{message}
"""

        # persist message record (no SMTP or external email services on free plan)
        contact_record = ContactMessage.objects.create(
            name=name,
            phone=phone,
            email=email,
            subject=subject,
            message=message,
        )

        try:
            logger.info("Contact inquiry saved: %s <%s> %s", name, email, phone)
            contact_record.sent = True
            contact_record.sent_at = timezone.now()
            contact_record.save(update_fields=['sent', 'sent_at'])
            messages.success(request, 'Thank you. Our team will contact you shortly.')
            return redirect('contact')
        except Exception as e:
            logger.exception('Failed to update contact_record status')
            tb = traceback.format_exc()
            messages.error(request, 'Failed to save your message. Please try again later.')
            try:
                contact_record.error = str(e) + "\n\n" + tb
                contact_record.save(update_fields=['error'])
            except Exception:
                logger.exception('Failed to save contact_record error')

            context.update({
                'name': name,
                'phone': phone,
                'email': email,
                'subject': subject,
                'message': message
            })
    return render(request, 'contact.html', context)

def services(request):
    return render(request, 'services.html')


@login_required(login_url='login')
def save_bookmark(request, property_id):
    property_obj = get_object_or_404(Properties, id=property_id)
    bookmark, created = SavedProperty.objects.get_or_create(
        user=request.user,
        property=property_obj,
        defaults={'is_paid': False},
    )

    if not created and bookmark.is_paid:
        bookmark.is_paid = False
        bookmark.save(update_fields=['is_paid'])

    messages.success(request, f'{property_obj.name} has been saved to your bookmarks.')
    return redirect('bookmarks')


@login_required(login_url='login')
def bookmarks(request):
    saved_bookmarks = (
        SavedProperty.objects.filter(user=request.user, is_paid=False)
        .select_related('property')
        .order_by('-saved_at')
    )
    content = {
        'saved_bookmarks': saved_bookmarks,
        'saved_count': saved_bookmarks.count(),
        'saved_property_ids': list(saved_bookmarks.values_list('property_id', flat=True)),
        'default_virtual_tour_url': DEFAULT_VIRTUAL_TOUR_URL,
    }
    return render(request, 'bookmark.html', content)


def login_view(request):
    if request.user.is_authenticated:
        return redirect("index")

    if request.method == "POST":
        credential = request.POST.get("username_or_email", "").strip()
        password = request.POST.get("password", "")

        if not credential or not password:
            messages.error(request, "Please enter your email/username and password.")
            return render(request, "login.html")

        username = credential
        if "@" in credential:
            matched_user = User.objects.filter(email__iexact=credential).first()
            if matched_user:
                username = matched_user.username

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful.")
            return redirect("index")

        messages.error(request, "Invalid username/email or password.")

    return render(request, 'login.html')


def signup_view(request):
    if request.user.is_authenticated:
        return redirect("index")

    if request.method == "POST":
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")

        if not email or not password or not confirm_password:
            messages.error(request, "Email and password fields are required.")
            return render(request, "signup.html")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, "signup.html")

        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters.")
            return render(request, "signup.html")

        if User.objects.filter(email__iexact=email).exists():
            messages.error(request, "An account with this email already exists.")
            return render(request, "signup.html")

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        login(request, user)
        messages.success(request, "Account created successfully.")
        return redirect("index")

    return render(request, 'signup.html')

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "You have been logged out.")
    return redirect("index")

def properties(request):
    base_queryset = Properties.objects.all()
    all_properties, filters = _apply_property_filters(request, base_queryset)
    saved_property_ids = _get_saved_property_ids(request.user)
    content = {
        'all_properties': all_properties,
        'filters': filters,
        'result_count': all_properties.count(),
        'default_virtual_tour_url': DEFAULT_VIRTUAL_TOUR_URL,
        'saved_property_ids': saved_property_ids,
    }
    return render(request, 'properties.html', content)

def propertydetail(request, property_id):
    property_obj = get_object_or_404(Properties, id=property_id)
    content = {
        'property': property_obj,
        'default_virtual_tour_url': DEFAULT_VIRTUAL_TOUR_URL,
        'saved_property_ids': _get_saved_property_ids(request.user),
    }
    return render(request, 'propertydetail.html', content)

def dashboard(request):
    # Only allow admin/staff users to access the dashboard
    if not (request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser)):
        messages.error(request, "Access denied. Admins only.")
        return redirect("index")

    # Admins see all properties
    base_queryset = Properties.objects.all()

    # Apply filters
    all_properties, filters = _apply_property_filters(request, base_queryset)

    # Calculate summary statistics
    total_properties = Properties.objects.count()
    featured_properties = Properties.objects.filter(is_featured=True).count()
    available_properties = Properties.objects.filter(status='available').count()
    sold_properties = Properties.objects.filter(status='sold').count()

    content = {
        'properties': all_properties,
        'filters': filters,
        'result_count': all_properties.count(),
        'total_properties': total_properties,
        'featured_count': featured_properties,
        'available_count': available_properties,
        'sold_count': sold_properties,
        'is_admin': True,
    }
    return render(request, 'dashboard.html', content)