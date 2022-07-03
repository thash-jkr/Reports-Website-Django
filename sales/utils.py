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

def get_key(res):
    key = None
    if res == "#1":
        key = "transaction_id"
    elif res == "#2":
        key = "created"
    return key

def get_chart(type, data, results_by,**kwargs):
    plt.switch_backend("AGG")
    fig = plt.figure(figsize=(10, 4))
    key = get_key(results_by)
    df = data.groupby(key, as_index=False)["total_price"].agg("sum")

    if type == "#1":
        # plt.bar(df[key], df["total_price"])
        sns.barplot(data=df, x=key, y="total_price")
    elif type == "#2":
        plt.pie(data=df, x="total_price", labels=df[key].values)
    elif type == "#3":
        plt.plot(df[key], df["total_price"])
    else:
        print("Error error erroR")

    plt.tight_layout()
    chart = get_graph()
    return chart