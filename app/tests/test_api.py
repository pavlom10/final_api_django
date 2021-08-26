import pytest
from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from rest_framework import status
from model_bakery import baker
from users.models import User, UserRoleChoices
from products.models import ProductInfo, Product, Category
from shops.models import Shop
from orders.models import OrderItem, Order, OrderStatusChoices, Contact

pytestmark = [
    pytest.mark.django_db
]


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def product_factory():
    def factory(**kwargs):
        category = baker.make('Category')
        product = baker.make('Product', category=category)
        shop = baker.make('Shop')
        return baker.make('ProductInfo', shop=shop, product=product, **kwargs)
    return factory


def test_user_register(api_client):
    url = reverse('auth_register')
    user_payload = {
        'username': 'newuser',
        'password': '12345abc!',
        'password2': '12345abc!',
        'email': 'newuser@test.com',
        'first_name': 'Name',
        'last_name': 'Postman',
        'company': 'Some company',
        'position': 'Manager',
    }

    resp = api_client.post(url, user_payload)
    assert resp.status_code == status.HTTP_201_CREATED


def test_add_shop(api_client):
    url = reverse('shops-list')
    shop_payload = {
        'name': 'Some shop',
        'url': 'http://shop.com',
    }

    resp = api_client.post(url, shop_payload)
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    user = User.objects.create(username='user1', password='bar', role=UserRoleChoices.SHOP)
    api_client.force_authenticate(user)

    resp = api_client.post(url, shop_payload)
    assert resp.status_code == status.HTTP_201_CREATED

    url = reverse('partner_state')
    resp = api_client.post(url, {'state': 'off'})
    assert resp.status_code == status.HTTP_200_OK


def test_add_contacts(api_client):
    user = User.objects.create(username='user1', password='bar', role=UserRoleChoices.BUYER)
    api_client.force_authenticate(user)

    url = reverse('contacts-list')
    contacts_payload = {
        'phone': '+75555555',
        'city': 'SPb',
        'street': 'Fontanka',
        'house': '90',
        'building': 'A',
        'apartment': '10',
    }

    resp = api_client.post(url, contacts_payload)
    assert resp.status_code == status.HTTP_201_CREATED


def test_get_products(api_client, product_factory):
    product1 = product_factory()
    product2 = product_factory()
    assert product1.id

    url = reverse('products')
    resp = api_client.get(url)
    resp_json = resp.json()
    assert len(resp_json) == 2


def test_add_to_cart(api_client, product_factory):
    user = User.objects.create(username='user1', password='bar', role=UserRoleChoices.BUYER)
    api_client.force_authenticate(user)

    product = product_factory()

    url = reverse('cart')
    cart_payload = {
        'product_id': product.id,
        'quantity': '10',
    }

    resp = api_client.post(url, cart_payload)
    assert resp.status_code == status.HTTP_200_OK


def test_send_order(api_client, product_factory):
    user = User.objects.create(username='user1', password='bar', role=UserRoleChoices.BUYER)
    api_client.force_authenticate(user)

    product = product_factory()
    contact = Contact.objects.create(user=user, phone='+75555555')
    assert contact.id

    order = Order.objects.create(user=user, state=OrderStatusChoices.CART)
    order_item = OrderItem.objects.create(order=order, product_info=product, quantity=10)
    assert order.id
    order_id = order.id

    url = reverse('partner_orders')
    resp = api_client.post(url, {'id': order.id, 'contact': contact.id})
    assert resp.status_code == status.HTTP_200_OK

    order = Order.objects.get(pk=order_id)
    assert order.state == OrderStatusChoices.NEW

