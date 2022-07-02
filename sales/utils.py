import uuid, base64
import matplotlib.pyplot as plt
import seaborn as sns

from profiles.models import Profile
from customers.models import Customer

from io import BytesIO

def generate_code():
    code = str(uuid.uuid4()).replace("-", "")[:12].upper()
    return code

def get_salesman(id):
    return Profile.objects.get(id=id)

def get_customer(id):
    return Customer.objects.get(id=id)

def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode("utf-8")
    buffer.close()
    return graph

def get_chart(type, data, **kwargs):
    plt.switch_backend("AGG")
    fig = plt.figure(figsize=(10, 4))

    if type == "#1":
        print("Bar chart")
        # plt.bar(data["transaction_id"], data["price"])
        sns.barplot(data=data, x="transaction_id", y="price")
    elif type == "#2":
        print("Pie chart")
        labels = kwargs.get("labels")
        plt.pie(data=data, x="price", labels=labels)
    elif type == "#3":
        print("Line chart")
        plt.plot(data["transaction_id"], data["price"])
    else:
        print("Error error erroR")

    plt.tight_layout()
    chart = get_graph()
    return chart