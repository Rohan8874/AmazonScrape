from django.shortcuts import render
from .scraper import Scraper
from .models import ProductURL
import pandas as pd

def scrape_product(request):
    product_details = None

    if request.method == 'POST':
        url = request.POST.get('url')
        scraper = Scraper(url)
        product_details = scraper.scrape()

        if product_details and url:
            try:
                product_url, created = ProductURL.objects.get_or_create(
                    url=url,
                    defaults={
                        'title': product_details['title'],
                        'price': product_details['price'],
                        'hero_image_url': product_details['hero_image_url']
                    }
                )
                
                if created:
                    data = [url, product_details['title'], product_details['price'], product_details['hero_image_url']]
                    scraper.save_to_csv(data)
            except Exception as e:
                print(f"Error saving URL: {e}")

    return render(request, 'products/product.html', {
        'product_details': product_details,
    })

def search_product(request):
    search_result = None
    if request.method == 'POST':
        search_url = request.POST.get('search_url')
        search_result = get_product_data_from_db(search_url)
    return render(request, 'products/search.html', {'search_result': search_result})

def get_product_data_from_db(url):
    try:
        product = ProductURL.objects.get(url=url)
        return {
            'Title': product.title,
            'Price': product.price,
            'Hero Image URL': product.hero_image_url
        }
    except ProductURL.DoesNotExist:
        return None