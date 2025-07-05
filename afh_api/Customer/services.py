from .models import Customer

def create_customer(name, email, phone, post,  representative):
    """
    Create a new customer with the given name, email, and phone number.
    """
    customer = Customer(name=name, email=email, phone=phone, post=post, representative=representative)
    customer.save()
    return customer

def update_customer(id, name=None, email=None, phone=None, post=None,  representative = None):
    """
    Update an existing customer with the given ID.
    If a field is None, it will not be updated.
    """
    try:
        customer = Customer.objects.get(id=id)
        if name is not None:
            customer.name = name
        if email is not None:
            customer.email = email
        if phone is not None:
            customer.phone = phone
        if post is not None:
            customer.post = post
        if  representative is not None:
            customer.representative =  representative
        customer.save()
        return customer
    except Customer.DoesNotExist:
        return None
    
def delete_customer(id):
    """
    Delete a customer with the given ID.
    Returns True if the customer was deleted, False if it did not exist.
    """
    try:
        customer = Customer.objects.get(id=id)
        customer.delete()
        return True
    except Customer.DoesNotExist:
        return False
    
def get_customers():
    """
    Retrieve all customers.
    Returns a list of Customer objects.
    """
    return Customer.objects.all()

def get_customer_by_id(id):
    """
    Retrieve a customer by ID.
    Returns the Customer object if found, None otherwise.
    """
    try:
        return Customer.objects.get(id=id)
    except Customer.DoesNotExist:
        return None