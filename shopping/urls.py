from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from .views import admin_logout, add_to_cart, remove_from_cart, clear_cart

urlpatterns = [
    path('product_detail/', views.product_detail, name='product-detail'),  
    path('product/<str:product_id>/categories/', views.product_category_detail, name='product-category-detail'),
    path('category/<int:category_id>/', views.category_detail, name='category-detail'),
    path('modifications/', views.product_modifications, name='product-modifications'),
    path('creator/<int:creator_id>/products/', views.creator_products, name='creator-products'),
    path('last_modified_by_creator/<int:creator_id>/', views.last_modified_by_creator, name='last-modified-by-creator'),
    # path('login/', views.user_login, name='login'), 
    path('login/', views.user_login, name='user_login'),  
    path('product_detail/', views.product_detail, name='product-detail'),
    path('admin-logout/', admin_logout, name='admin_logout'),
    path('view_cart/', views.view_cart, name='view_cart'),

 
    path('add-to-cart/<str:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('clear_cart/', clear_cart, name='clear_cart'),  # Define the URL pattern for clear_cart
    path('update-cart-item/', views.update_cart_item, name='update_cart_item'),  # Define the URL pattern for update_cart_item
    path('checkout/', views.checkout, name='checkout'),
    path('payment/', views.process_payment, name='process_payment'),
    path('useer-out/', views.user_logout, name='user_logout'),
    path('success/', views.payment_success, name='some_success_page'),
    path('order_list/', views.order_list, name='order_list'),

]



