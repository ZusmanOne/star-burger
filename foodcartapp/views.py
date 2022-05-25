from django.http import JsonResponse
from django.templatetags.static import static
from .models import Order, OrderItem
from .models import Product
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import OrderSerializer, OrderItemSerializer
from django.db import transaction


def banners_list_api(request):
    # FIXME move data to db?
    return JsonResponse([
        {
            'title': 'Burger',
            'src': static('burger.jpg'),
            'text': 'Tasty Burger at your door step',
        },
        {
            'title': 'Spices',
            'src': static('food.jpg'),
            'text': 'All Cuisines',
        },
        {
            'title': 'New York',
            'src': static('tasty.jpg'),
            'text': 'Food is incomplete without a tasty dessert',
        }
    ], safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


@api_view(['GET'])
def product_list_api(request):
    products = Product.objects.select_related('category').available()
    dumped_products = []
    for product in products:
        dumped_product = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'special_status': product.special_status,
            'description': product.description,
            'category': {
                'id': product.category.id,
                'name': product.category.name,
            } if product.category else None,
            'image': product.image.url,
            'restaurant': {
                'id': product.id,
                'name': product.name,
            }
        }
        dumped_products.append(dumped_product)
    return Response(dumped_products)


@transaction.atomic
@api_view(['POST'])
def register_order(request):
    serializer_order = OrderSerializer(data=request.data)
    serializer_order.is_valid(raise_exception=True)
    products = request.data.get('products', [])
    create_order = Order.objects.create(
        firstname=serializer_order.validated_data['firstname'],
        lastname=serializer_order.validated_data['lastname'],
        phonenumber=serializer_order.validated_data['phonenumber'],
        address=serializer_order.validated_data['address']
    )
    create_order_item = []
    for order in products:
        serializer = OrderItemSerializer(data=order)
        serializer.is_valid(raise_exception=True)
        create_order_item.append(
        OrderItem(
            product=serializer.validated_data['product'],
            order=create_order,
            quantity=serializer.validated_data['quantity'],
            price=serializer.validated_data['product'].price * serializer.validated_data['quantity'],

        ))
    OrderItem.objects.bulk_create(create_order_item)
    return Response(OrderSerializer(create_order).data)
