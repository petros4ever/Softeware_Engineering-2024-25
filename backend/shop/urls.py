from django.urls import path
from .views import home_page

urlpatterns = [
    path('', home_page, name='home'),
]

# shop/urls.py
from django.urls import path
from .views import home_page, search_book, add_to_cart, view_cart, checkout

urlpatterns = [
    path('', home_page, name='home'),
    path('search/', search_book, name='search_book'),
    path('add-to-cart/<int:book_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', view_cart, name='view_cart'),  # <-- New route for the cart
    path('checkout/', checkout, name='checkout'),

]
