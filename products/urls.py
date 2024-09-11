from django.urls import path
from .views import scrape_product, search_product

urlpatterns = [
    path('scrape/', scrape_product, name='scrape_product'),
    path('search/', search_product, name='search_product'),
]