from .models import Section, Notification, Article


def sections_processor(request):
    """Добавляет разделы, недавние статьи, закладки и уведомления в контекст всех шаблонов"""
    sections = Section.objects.filter(is_active=True).filter(parent__isnull=True).prefetch_related('children')
    
    ctx = {
        'nav_sections': sections,
        'nav_articles': Article.objects.filter(status='published').order_by('-updated_at')[:5],
    }
    
    if request.user.is_authenticated:
        from .models import RecentlyViewed, Bookmark
        ctx['recently_viewed'] = RecentlyViewed.objects.filter(user=request.user)[:10]
        ctx['bookmarks'] = Bookmark.objects.filter(user=request.user)[:10]
        ctx['unread_notifications'] = Notification.objects.filter(user=request.user, is_read=False)
        ctx['unread_count'] = ctx['unread_notifications'].count()
    
    return ctx