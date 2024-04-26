from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from shopping.models import Product, Category, Cart, CartItem

class ProductViewTests(TestCase):

    def setUp(self):
        # Creating test user
        self.user = User.objects.create_user(username='testuser', password='12345')
        
        # Creating a product
        self.product = Product.objects.create(
            product_id='P001',
            name='Test Product',
            price=150.00,
            description='A test product',
            sku='SKU001'
        )

        # Creating a category
        self.category = Category.objects.create(name='Test Category')

        # User login
        self.client.login(username='testuser', password='12345')

    def test_product_detail_view(self):
        # Access the product detail page
        response = self.client.get(reverse('product-detail'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Product')

    def test_category_detail_view(self):
        # Access a specific category detail page
        response = self.client.get(reverse('category-detail', args=[self.category.category_id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Category')

    def test_add_to_cart_view(self):
        # Test adding a product to the cart
        response = self.client.get(reverse('add_to_cart', args=[self.product.product_id]))
        expected_response = {'success': True, 'cartItemCount': 1, 'cartTotalQuantity': 1}
        self.assertJSONEqual(str(response.content, encoding='utf8'), expected_response)

    def test_view_cart(self):
        # Test viewing the cart
        self.test_add_to_cart_view()  # First add an item to ensure cart is not empty
        response = self.client.get(reverse('view_cart'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Product')

    def test_remove_from_cart_view(self):
        # Test removing an item from the cart
        self.test_add_to_cart_view()  # First add an item
        cart_item = CartItem.objects.filter(product=self.product, cart__user=self.user).first()
        response = self.client.post(reverse('remove_from_cart', args=[cart_item.id]))
        self.assertEqual(response.status_code, 302)  # Should redirect to the cart view

    # def test_checkout_view(self):
    #     # Test the checkout view
    #     self.test_add_to_cart_view()  # First add an item
    #     response = self.client.get(reverse('checkout'))
    #     print(response.content)  # Add this line to debug
    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, 'Checkout')

class UserAuthenticationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_user_login(self):
        # Test login functionality
        response = self.client.post(reverse('user_login'), {'username': 'testuser', 'password': '12345'})
        self.assertEqual(response.status_code, 302)  # Check for redirect after successful login

    def test_user_logout(self):
        # Ensure the user is logged in first
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('user_logout'))
        self.assertEqual(response.status_code, 302)  # Check for redirect after logout

# Add more tests as needed for other views and functionalities.
