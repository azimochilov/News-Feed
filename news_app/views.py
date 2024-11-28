from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountMixin

from news.custom_permissions import OnlyLoggedSuperUser
from .forms import ContactForm, CommentForm
from django.views.generic import TemplateView,ListView,CreateView,UpdateView,DeleteView
def news_list(request):
    news_list = News.objects.all()
    #news_list = News.obkects.filter(status=News.status.Published
    context = {
        'news_list':news_list
    }
    return render(request,"news/news_list.html", context = context)

from .models import News,Category


def news_detail(request,id):
    news = get_object_or_404(News, id=id)
    # news = get_object_or_404(News, id=id,status=News.status.Published)

    context = {}
    #hitCountLogic
    hit_count = get_hitcount_model().objects.get_for_object(news)
    hits = hit_count.hits
    hitcontext = context['hitcount'] = {'pk': hit_count.pk}
    hit_count_response = HitCountMixin.hit_count(request, hit_count)
    if hit_count_response.hit_counted:
        hits = hits + 1
        hitcontext['hit_counted'] = hit_count_response.hit_counted
        hitcontext['hit_message'] = hit_count_response.hit_message
        hitcontext['total_hits'] = hits

    comments = news.comments.filter(active=True)
    comment_count = comments.count()
    new_comment = None

    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.news = news
            new_comment.user = request.user
            new_comment.save()
            comment_form = CommentForm()

    else:
        comment_form = CommentForm()

    context = {
        "news":news,
        "comments":comments,
        "new_comment":new_comment,
        "comment_form":comment_form,
        "comment_count":comment_count
    }
    return render(request,"news/news_details.html", context = context)

def homePageView(request):

    news_list = News.published.all().order_by('-published_time')[:5]
    categories = Category.objects.all()
    last_one = News.published.filter(category__name='sport').order_by('-published_time')[0]
    sport_news = News.published.all().filter(category__name='sport').order_by('-published_time')[1:5]

    context = {
        'news_list' : news_list,
        'categories' : categories,
        'last_one' : last_one,
        'sport_news' : sport_news

    }

    return render(request, 'news/home.html', context = context)


def notFoundPageView(request):

    context = {

    }
    return render(request,'news/404.html', context = context)




class ContactPageView(TemplateView):
    template_name = "news/contact.html"

    def get(self, request, *args, **kwargs):
        form = ContactForm()
        context = {
            "form": form
        }
        return render(request, 'news/contact.html', context=context)

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("Thank you for contacting us!")

        context = {
            "form": form
        }
        return render(request, 'news/contact.html', context=context)

class HomePageView(ListView):
    model = News
    template_name = 'news/home.html'
    context_object_name = 'news'
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['news_list'] = News.published.all().order_by('-published_time')[:5]
        context['last_one'] = News.published.filter(category__name='sport').order_by('-published_time')[0]
        context['sport_news'] = News.published.all().filter(category__name='sport').order_by('-published_time')[1:5]
        context['political_news'] = News.published.all().filter(category__name='politics').order_by('-published_time')[:5]
        context['technological_news'] = News.published.all().filter(category__name='technology').order_by('-published_time')[:5]
        return context

class SportPageView(ListView):
    model = News
    template_name = 'news/sport.html'
    context_object_name = 'sport_news'
    def get_queryset(self):
        news = self.model.published.all().filter(category__name='sport')
        return news

class PoliticalPageView(ListView):
    model = News
    template_name = 'news/politic.html'
    context_object_name = 'political_news'
    def get_queryset(self):
        news = self.model.published.all().filter(category__name='politics')
        return news

class TechnologicalPageView(ListView):
    model = News
    template_name = 'news/technology.html'
    context_object_name = 'technological_news'
    def get_queryset(self):
        news = self.model.published.all().filter(category__name='technology')
        return news

class NewsUpdateView(OnlyLoggedSuperUser,UpdateView):
    model = News
    fields = ['title','body','image','category','status',]
    template_name = 'crud/news_edit.html'
    pk_url_kwarg = 'id'

class NewsDeleteView(OnlyLoggedSuperUser,DeleteView):
    model = News
    template_name = 'crud/news_delete.html'
    success_url = reverse_lazy('home_page')
    pk_url_kwarg = 'id'

class NewsCreateView(OnlyLoggedSuperUser,CreateView):
    model = News
    template_name = 'crud/news_create.html'
    fields = ['title','body','body','image','category','status',]

@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_page(request):
    admin_users = User.objects.filter(is_superuser=True)
    context = {
        'admin_users' : admin_users,
    }

    return render(request, 'pages/admin_page.html', context)



class SearchResultsList(ListView):
    model = News
    template_name = 'news/search_result.html'
    context_object_name = 'all_result_news'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return News.objects.filter(
            Q(title__icontains=query) | Q(body__icontains=query)
        )