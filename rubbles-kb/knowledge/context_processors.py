from .models import Section, Notification, Article


from django.db.models import Prefetch

def sections_processor(request):
    """Добавляет разделы, недавние статьи, закладки и уведомления в контекст всех шаблонов"""
    articles_prefetch = Prefetch('articles', queryset=Article.objects.filter(status='published').order_by('-updated_at'))
    sections = Section.objects.filter(is_active=True).filter(parent__isnull=True).prefetch_related('children').prefetch_related(articles_prefetch)
    
    ctx = {
        'nav_sections': sections,
    }
    
    if request.user.is_authenticated:
        from .models import RecentlyViewed, Bookmark
        ctx['recently_viewed'] = RecentlyViewed.objects.filter(user=request.user)[:10]
        ctx['bookmarks'] = Bookmark.objects.filter(user=request.user)[:10]
        ctx['unread_notifications'] = Notification.objects.filter(user=request.user, is_read=False)
        ctx['unread_count'] = ctx['unread_notifications'].count()
    
    return ctx