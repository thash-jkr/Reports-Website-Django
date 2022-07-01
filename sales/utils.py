import uuid

from profiles.models import Profile
from customers.models import Customer

def generate_code():
    code = str(uuid.uuid4()).replace("-", "")[:12].upper()
    return code

def get_salesman(id):
    return Profile.objects.get(id=id)

def get_customer(id):
    return Customer.objects.get(id=id)