from .models import Section


def sections_processor(request):
    """Добавляет разделы и недавние статьи в контекст всех шаблонов"""
    sections = Section.objects.filter(is_active=True).filter(parent__isnull=True).prefetch_related('children')
    ctx = {'nav_sections': sections}
    if request.user.is_authenticated:
        from .models import RecentlyViewed, Bookmark
        ctx['recently_viewed'] = RecentlyViewed.objects.filter(user=request.user)[:10]
        ctx['bookmarks'] = Bookmark.objects.filter(user=request.user)[:10]
    return ctx