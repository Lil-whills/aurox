from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import Properties


DEFAULT_VIRTUAL_TOUR_URL = "https://realsee.ai/nMnngDR5"


def _clean_param(request, *keys):
    """Return the first non-empty query parameter from the provided keys."""
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


# Create your views here.
def index(request):
    base_queryset = Properties.objects.filter(is_featured=True)
    featured_properties, filters = _apply_property_filters(request, base_queryset)
    content = {
        'featured_properties': featured_properties,
        'filters': filters,
        'result_count': featured_properties.count(),
        'default_virtual_tour_url': DEFAULT_VIRTUAL_TOUR_URL,
    }
    return render(request, 'index.html', content)

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def services(request):
    return render(request, 'services.html')

def properties(request):
    base_queryset = Properties.objects.all()
    all_properties, filters = _apply_property_filters(request, base_queryset)
    content = {
        'all_properties': all_properties,
        'filters': filters,
        'result_count': all_properties.count(),
        'default_virtual_tour_url': DEFAULT_VIRTUAL_TOUR_URL,
    }
    return render(request, 'properties.html', content)

def propertydetail(request, property_id):
    property_obj = get_object_or_404(Properties, id=property_id)
    content = {
        'property': property_obj,
        'default_virtual_tour_url': DEFAULT_VIRTUAL_TOUR_URL,
    }
    return render(request, 'propertydetail.html', content)