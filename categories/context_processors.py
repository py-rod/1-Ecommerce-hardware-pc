from categories.models import Categories


def menu_links(request):
    categories = Categories.objects.filter(is_active=True).order_by("id")
    return dict(categories=categories)
