from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.contrib.auth.models import User

from catalog.models import Category, Product

User = get_user_model()

class ProductModelTest(TestCase):

    def setUp(self):
        self.seller = User.objects.create_user(username="testuser", password="testpass")
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            seller=self.seller,
            count=10,
            price=99.99,
            category=self.category,
            description="Test description",
            name="Test Product",
        )

    def test_default_values(self):
        new_product = Product.objects.create(
            seller=self.seller,
            price=50.00,
            category=self.category,
            name="Default Product",
        )
        self.assertEqual(new_product.count, 1)
        self.assertEqual(new_product.description, None)
        self.assertTrue("default_product.jpg" in new_product.image.url)

    def test_product_str_representation(self):
        self.assertEqual(str(self.product), "Test Product")

    def test_field_constraints(self):
        with self.assertRaises(ValidationError):
            product = Product(
                seller=self.seller,
                count=-5,
                price=-10.00,
                category=self.category,
                name="Invalid Product",
            )
            product.full_clean()
