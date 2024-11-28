from .models import News
def latest_news(request ):
    latest_news = News.published.all().order_by('-published_time')[:7]
    context = {
        'latest_news': latest_news
    }

    return context