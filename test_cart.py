import unittest
from cart import ShoppingCart

class TestShoppingCart(unittest.TestCase):
    def setUp(self):
        self.cart = ShoppingCart()

    def test_add_item_normal(self):
        self.cart.add_item("Apple", 2.0, 3)
        self.assertEqual(self.cart.get_total(), 6.0)

    def test_remove_item_normal(self):
        self.cart.add_item("Apple", 2.0, 3)
        self.cart.remove_item("Apple")
        self.assertEqual(self.cart.get_total(), 0.0)

    def test_apply_discount_percent_normal(self):
        self.cart.add_item("Apple", 10.0, 2)
        self.cart.apply_discount("SAVE10")
        self.assertEqual(self.cart.get_total(), 18.0)

    def test_apply_discount_fixed_normal(self):
        self.cart.add_item("Banana", 10.0, 4)
        self.cart.apply_discount("FLAT5")
        self.assertEqual(self.cart.get_total(), 35.0)

    def test_add_item_zero_or_negative_quantity(self):
        with self.assertRaisesRegex(ValueError, "Quantity must be a positive integer."):
            self.cart.add_item("Apple", 2.0, 0)
        with self.assertRaisesRegex(ValueError, "Quantity must be a positive integer."):
            self.cart.add_item("Apple", 2.0, -5)

    def test_add_item_negative_price(self):
        with self.assertRaisesRegex(ValueError, "Price cannot be negative."):
            self.cart.add_item("Apple", -2.0, 1)

    def test_apply_discount_unmet_threshold(self):
        self.cart.add_item("Apple", 10.0, 2)
        with self.assertRaisesRegex(ValueError, "A minimum order of"):
            self.cart.apply_discount("SAVE20")

    def test_remove_item_does_not_exist(self):
        with self.assertRaisesRegex(KeyError, "is not in the cart"):
            self.cart.remove_item("Ghost Item")

    def test_apply_invalid_discount_code(self):
        self.cart.add_item("Apple", 10.0, 2)
        with self.assertRaisesRegex(ValueError, "is not a valid discount code"):
            self.cart.apply_discount("INVALID_CODE")

    def test_clear_cart(self):
        self.cart.add_item("Apple", 10.0, 2)
        self.cart.apply_discount("SAVE10")
        self.cart.clear()
        self.assertEqual(self.cart.get_total(), 0.0)
        # Will fail because get_item_count is not implemented in buggy cart
        with self.assertRaises(NotImplementedError):
            self.cart.get_item_count()

    def test_cumulative_state_add_twice(self):
        self.cart.add_item("Apple", 2.0, 2)
        self.cart.add_item("Apple", 2.0, 3)
        # Will fail because of buggy += logic
        self.assertEqual(self.cart._subtotal(), 10.0) 

    def test_boundary_discount_threshold(self):
        self.cart.add_item("Apple", 15.0, 2)
        self.cart.apply_discount("FLAT5")
        self.assertEqual(self.cart.get_total(), 25.0)

if __name__ == '__main__':
    unittest.main()
