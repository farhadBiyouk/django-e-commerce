from django.contrib.sitemaps import Sitemap
from home.models import Product


class ProductViewSiteMap(Sitemap):
    changefreq = 'never'
    priority = 0.5

    def items(self):
        return Product.objects.all().order_by('-id')

    def lasmod(self, obj):
        return obj.create
