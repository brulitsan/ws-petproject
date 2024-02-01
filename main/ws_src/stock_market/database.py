from ws_src.stock_market.models import Product


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


def get_quantity(obj):
    product_price = Product.objects.get(id=obj.product_id).price
    return obj.transaction_price / product_price


def validate(attrs):
    product = attrs.get('product')
    attrs['quantity'] = attrs['transaction_price'] / product.price
    return attrs