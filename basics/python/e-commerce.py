from abc import ABC, abstractmethod
from datetime import datetime
from typing import ClassVar


class Product:
    """Product class represents a product in the e-commerce system."""

    def __init__(self, name: str, price: float, category: str, stock_quantity: int = 0) -> None:
        self._name = name
        self._price = price
        self._stock_quantity = stock_quantity
        self._category = category

    @property
    def price(self) -> float:
        return self._price if self._price > 0 else 0.0

    @price.setter
    def price(self, value: float) -> None:
        if value < 0:
            raise ValueError("Price cannot be negative")
        self._price = value

    @property
    def name(self) -> str:
        return self._name

    @property
    def category(self) -> str:
        return self._category

    @property
    def stock_quantity(self) -> int:
        return self._stock_quantity

    def __str__(self) -> str:
        return f"{self._name} - ${self._price} - {self._stock_quantity} in stock - {self._category}"

    def __repr__(self) -> str:
        return f"Product('{self._name}', {self._price}, {self._stock_quantity}, '{self._category}')"

    def reduce_stock(self, quantity: int) -> None:
        """Reduce stock quantity for the product."""
        if quantity > self._stock_quantity:
            raise ValueError("Not enough stock")
        self._stock_quantity -= quantity

    def increase_stock(self, quantity: int) -> None:
        """Increase stock quantity for the product."""
        if quantity < 0:
            raise ValueError("Quantity cannot be negative")
        self._stock_quantity += quantity

    def __eq__(self, other: object) -> bool:
        """Check if two products are equal."""
        if not isinstance(other, Product):
            return False
        return self._name == other._name and self._price == other._price

    def __hash__(self) -> int:
        """Hash the product."""
        return hash((self._name, self._price))

    @staticmethod
    def validate_price(price: float) -> bool:
        """Validate that price is non-negative."""
        return price >= 0

    @classmethod
    def from_dict(cls, data: dict) -> 'Product':
        """Create a Product from a dictionary."""
        return cls(
            name=data['name'],
            price=data['price'],
            category=data['category'],
            stock_quantity=data.get('stock_quantity', 0)
        )


class Customer:
    """Customer class represents a customer in the e-commerce system."""

    def __init__(self, customer_id: str, name: str, email: str, shipping_address: str) -> None:
        self._customer_id = customer_id
        self._name = name
        self._email = email
        self._shipping_address = shipping_address

    @property
    def customer_id(self) -> str:
        return self._customer_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str) -> None:
        if "@" not in value or "." not in value:
            raise ValueError("Invalid email format")
        self._email = value

    @property
    def shipping_address(self) -> str:
        return self._shipping_address

    def __str__(self) -> str:
        return f"{self._name} - {self._email} - {self._shipping_address}"

    def __repr__(self) -> str:
        return f"Customer('{self._customer_id}', '{self._name}', '{self._email}', '{self._shipping_address}')"

    def update_address(self, new_address: str) -> None:
        """Update the customer's shipping address."""
        if not new_address:
            raise ValueError("Address cannot be empty")
        self._shipping_address = new_address

    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format."""
        return "@" in email and "." in email

    @classmethod
    def from_dict(cls, data: dict) -> 'Customer':
        """Create a Customer from a dictionary."""
        return cls(
            customer_id=data['customer_id'],
            name=data['name'],
            email=data['email'],
            shipping_address=data['shipping_address']
        )


class OrderItem:
    """OrderItem class represents an item in an order."""

    def __init__(self, product: Product, quantity: int, subtotal: float = 0.0) -> None:
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        self._product = product
        self._quantity = quantity
        self._subtotal = subtotal

    @property
    def product(self) -> Product:
        return self._product

    @property
    def quantity(self) -> int:
        return self._quantity

    def calculate_subtotal(self) -> float:
        """Calculate the subtotal for the order item."""
        return self._product.price * self._quantity

    def __str__(self) -> str:
        return f"{self._product.name} - {self._quantity} - ${self.calculate_subtotal()}"

    def __repr__(self) -> str:
        return f"OrderItem({self._product.name}, {self._quantity}, ${self.calculate_subtotal()})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, OrderItem):
            return False
        return self._product == other._product and self._quantity == other._quantity


class Order:
    """Order class represents an order in the e-commerce system."""

    VALID_STATUSES: ClassVar[list[str]] = ["pending",
                                           "confirmed", "shipped", "delivered", "cancelled"]

    def __init__(self, order_id: str, customer: Customer, items: list[OrderItem] | None = None, status: str = "pending", created_at: str | None = None) -> None:
        self._order_id = order_id
        self._customer = customer
        self._items = items if items is not None else []
        self._status = status
        self._created_at = created_at if created_at is not None else datetime.now().isoformat()

    @property
    def order_id(self) -> str:
        return self._order_id

    @property
    def customer(self) -> Customer:
        return self._customer

    @property
    def items(self) -> list[OrderItem]:
        return self._items

    @property
    def status(self) -> str:
        return self._status

    @property
    def created_at(self) -> str:
        return self._created_at

    def add_item(self, item: OrderItem) -> None:
        """Add an item to the order."""
        if item in self._items:
            raise ValueError("Item already in order")
        if item._quantity > item._product.stock_quantity:
            raise ValueError(f"Not enough stock for {item._product.name}")
        self._items.append(item)

    def remove_item(self, item: OrderItem) -> None:
        """Remove an item from the order."""
        if item not in self._items:
            raise ValueError("Item not in order")
        self._items.remove(item)

    def calculate_total(self) -> float:
        """Calculate the total for the order."""
        return sum(item.calculate_subtotal() for item in self._items)

    def update_status(self, status: str) -> None:
        """Update the status of the order."""
        if status not in self.VALID_STATUSES:
            raise ValueError(
                f"Invalid status. Must be one of: {self.VALID_STATUSES}")
        self._status = status

    def __str__(self) -> str:
        return f"Order {self._order_id} - {self._customer} - {self._status} - ${self.calculate_total()}"

    def __repr__(self) -> str:
        return f"Order('{self._order_id}', {self._customer}, {len(self._items)} items, '{self._status}')"

    @classmethod
    def from_dict(cls, data: dict, customer: Customer) -> 'Order':
        """Create an Order from a dictionary."""
        return cls(
            order_id=data['order_id'],
            customer=customer,
            status=data.get('status', 'pending')
        )


class DigitalProduct(Product):
    """DigitalProduct class represents a digital product with no stock constraints."""

    def __init__(self, name: str, price: float, category: str, download_url: str = "") -> None:
        super().__init__(name, price, category, stock_quantity=999999)  # Unlimited stock
        self._download_url = download_url

    @property
    def download_url(self) -> str:
        return self._download_url

    def reduce_stock(self, quantity: int) -> None:
        """Digital products don't track stock."""
        pass  # No-op for digital products

    def increase_stock(self, quantity: int) -> None:
        """Digital products don't track stock."""
        pass  # No-op for digital products

    def __str__(self) -> str:
        return f"{self._name} - ${self._price} - Digital - {self._category}"

    def __repr__(self) -> str:
        return f"DigitalProduct('{self._name}', {self._price}, '{self._category}')"


class PaymentMethod(ABC):
    """PaymentMethod abstract class for payment processing."""

    def __init__(self, method: str) -> None:
        self._method = method

    @property
    def method(self) -> str:
        return self._method

    @abstractmethod
    def process_payment(self, amount: float) -> bool:
        """Process payment and return success status."""
        pass

    def __str__(self) -> str:
        return f"{self._method}"

    def __repr__(self) -> str:
        return f"PaymentMethod('{self._method}')"


class CreditCard(PaymentMethod):
    """CreditCard payment method implementation."""

    def __init__(self, card_number: str, expiry_date: str, cvv: str) -> None:
        super().__init__("Credit Card")
        self._card_number = card_number
        self._expiry_date = expiry_date
        self._cvv = cvv

    def process_payment(self, amount: float) -> bool:
        """Process the credit card payment."""
        print(f"Processing credit card payment of ${amount}")
        return True  # Simulate successful payment

    def __repr__(self) -> str:
        return f"CreditCard('****-****-****-{self._card_number[-4:]}', '{self._expiry_date}')"


class PayPal(PaymentMethod):
    """PayPal payment method implementation."""

    def __init__(self, email: str) -> None:
        super().__init__("PayPal")
        self._email = email

    def process_payment(self, amount: float) -> bool:
        """Process the PayPal payment."""
        print(f"Processing PayPal payment of ${amount} from {self._email}")
        return True  # Simulate successful payment

    def __repr__(self) -> str:
        return f"PayPal('{self._email}')"


class BankTransfer(PaymentMethod):
    """BankTransfer payment method implementation."""

    def __init__(self, bank_name: str, account_number: str) -> None:
        super().__init__("Bank Transfer")
        self._bank_name = bank_name
        self._account_number = account_number

    def process_payment(self, amount: float) -> bool:
        """Process the bank transfer payment."""
        print(
            f"Processing bank transfer payment of ${amount} from {self._bank_name}")
        return True  # Simulate successful payment

    def __repr__(self) -> str:
        return f"BankTransfer('{self._bank_name}', '****-{self._account_number[-4:]}')"


if __name__ == "__main__":
    print("=== E-Commerce System Demo ===\n")

    # Create some products
    product1 = Product("Laptop", 1000.0, "Electronics", 10)
    product2 = Product("Book", 20.0, "Education", 100)
    digital_product = DigitalProduct(
        "Python Course", 50.0, "Education", "https://example.com/download")

    print("Products:")
    print(f"  {product1}")
    print(f"  {product2}")
    print(f"  {digital_product}\n")

    # Create a customer
    customer = Customer("1", "John Doe", "john.doe@example.com", "123 Main St")
    print(f"Customer: {customer}\n")

    # Create an order
    order = Order("ORD-001", customer)

    # Add items to the order
    order.add_item(OrderItem(product1, 1))
    order.add_item(OrderItem(product2, 5))
    order.add_item(OrderItem(digital_product, 2))

    print(f"Order created: {order}")
    print(f"Order items:")
    for item in order.items:
        print(f"  {item}")
    print(f"Total: ${order.calculate_total()}\n")

    # Test different payment methods
    print("=== Testing Payment Methods ===")
    payments = [
        CreditCard("1234567890123456", "12/25", "123"),
        PayPal("john.doe@example.com"),
        BankTransfer("Chase", "9876543210")
    ]

    for payment in payments:
        print(f"Payment method: {payment}")
        success = payment.process_payment(order.calculate_total())
        print(f"Payment successful: {success}\n")

    # Update order status
    order.update_status("confirmed")
    print(f"Order status updated: {order.status}")

    # Test stock management
    print("\n=== Testing Stock Management ===")
    print(f"Laptop stock before: {product1.stock_quantity}")
    product1.reduce_stock(1)
    print(f"Laptop stock after order: {product1.stock_quantity}")

    # Test digital product stock (should not change)
    print(f"Digital product stock: {digital_product.stock_quantity}")
    digital_product.reduce_stock(10)
    print(
        f"Digital product stock after 'reduction': {digital_product.stock_quantity} (unchanged)\n")

    # Test class methods
    print("=== Testing Class Methods ===")
    product_dict = {
        'name': 'Mouse',
        'price': 25.0,
        'category': 'Electronics',
        'stock_quantity': 50
    }
    product3 = Product.from_dict(product_dict)
    print(f"Product from dict: {product3}")

    # Test static methods
    print(f"Price validation (100.0): {Product.validate_price(100.0)}")
    print(f"Price validation (-10.0): {Product.validate_price(-10.0)}")
    print(
        f"Email validation ('test@test.com'): {Customer.validate_email('test@test.com')}")
    print(
        f"Email validation ('invalid'): {Customer.validate_email('invalid')}\n")

    # Test error handling
    print("=== Testing Error Handling ===")
    try:
        product1.price = -10
    except ValueError as e:
        print(f"Price validation error: {e}")

    try:
        customer.email = "invalid-email"
    except ValueError as e:
        print(f"Email validation error: {e}")

    try:
        order.update_status("invalid-status")
    except ValueError as e:
        print(f"Status validation error: {e}")

    try:
        OrderItem(product1, 0)
    except ValueError as e:
        print(f"Quantity validation error: {e}")

    print("\n=== Demo Complete ===")
