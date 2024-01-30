from .models import Product


def update_or_create_product(id, category, lastPrice, highPrice, lowPrice):
    return Product.objects.update_or_create(
        id=id,
        defaults={
            'name': category,
            'price': lastPrice,
            'max_price': highPrice,
            'min_price': lowPrice,
        }
    )
