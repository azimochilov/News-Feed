from django.urls import path
from .views import (news_list,news_detail,homePageView,ContactPageView,notFoundPageView, HomePageView,SportPageView,
                    PoliticalPageView,TechnologicalPageView,NewsDeleteView,NewsUpdateView,NewsCreateView,admin_page,SearchResultsList)

urlpatterns = [
    path('news/', news_list, name='news_list'),
    path('news/<int:id>/', news_detail, name='news_detail_page'),
    path('',HomePageView.as_view(), name='home_page'),
    path('contact-us/',ContactPageView.as_view(), name='contact_page'),
    path('not-found/',notFoundPageView, name='not_found_page'),
    path('sports/',SportPageView.as_view(), name='sports_page'),
    path('politicals/',PoliticalPageView.as_view(), name='politicals_page'),
    path('technology',TechnologicalPageView.as_view(), name='technological_page'),
    path('news/<int:id>/edit/',  NewsUpdateView.as_view(), name='news_update'),
    path('news/<int:id>/delete/', NewsDeleteView.as_view(), name='news_delete'),
    path('news/create/', NewsCreateView.as_view(), name='news_create'),
    path('adminpage/', admin_page, name='admin_page'),
    path('searchresult/', SearchResultsList.as_view(), name='search_results')
]