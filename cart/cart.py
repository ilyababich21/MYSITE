from decimal import Decimal
from django.conf import settings
from shop.models import Product


class Cart(object):

    def __init__(self, request):
        """
        ыНИЦИАЛИЗЕйшон корзина

        """

        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        """
        add product or update count
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.price)}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        # update session cart

        self.session[settings.CART_SESSION_ID] = self.cart

        """ check session is update"""
        self.session.modified = True

    def remove(self, product):
        # drop product

        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        # select from database

        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product
        for elem in self.cart.values():
            elem['price'] = Decimal(elem['price'])
            elem['total_price'] = elem['price'] * elem['quantity']
            yield elem

    def __len__(self):

        """
        count all products in cart
        """

        return sum(elem['quantity'] for elem in self.cart.values())

    def get_total_price(self):

        """
        obshya price
        """

        return sum(Decimal(elem['price']) * elem['quantity'] for elem in
                   self.cart.values())

    def clear(self):
        '''
        drop cart from session
        '''

        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
