import csv
import pandas as pd

from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, TemplateView
from django.utils.dateparse import parse_date

from profiles.models import Profile
from .models import Sale, Position, CSV
from products.models import Product
from customers.models import Customer
from .forms import SalesSearchForm
from reports.forms import ReportForm
from .utils import get_customer, get_salesman, get_graph, get_chart

# Create your views here.
def home(request):
    sales_df = None
    positions_df = None
    merged_df = None
    df = None
    chart = None
    no_data = None
    search_form = SalesSearchForm(request.POST or None)
    report_form = ReportForm()

    if request.method == "POST":
        date_from = request.POST.get("date_from")
        date_to = request.POST.get("date_to")
        chart_type = request.POST.get("chart_type")
        results_by = request.POST.get("results_by")
        sales_qs = Sale.objects.filter(created__date__lte=date_to, created__date__gte=date_from)

        if len(sales_qs) > 0:
            sales_df = pd.DataFrame(sales_qs.values())
            sales_df["customer_id"] = sales_df["customer_id"].apply(get_customer)
            sales_df["salesman_id"] = sales_df["salesman_id"].apply(get_salesman)
            sales_df.rename({"customer_id": "customer", "salesman_id": "salesman", "id": "sales_id"}, axis=1, inplace=True)
            sales_df["created"] = sales_df["created"].apply(lambda x: x.strftime("%Y-%m-%d"))
            sales_df["updated"] = sales_df["updated"].apply(lambda x: x.strftime("%Y-%m-%d"))
            positions_data = []

            for sale in sales_qs:
                for pos in sale.get_positions():
                    obj = {
                        "position_id": pos.id,
                        "product": pos.product.name,
                        "quantity": pos.quantity,
                        "price": pos.price,
                        "sales_id": pos.get_sales_id()
                    }
                    positions_data.append(obj)

            positions_df = pd.DataFrame(positions_data)
            merged_df = pd.merge(sales_df, positions_df, on="sales_id")
            df = merged_df.groupby("transaction_id", as_index=False)["price"].agg("sum")
            chart = get_chart(chart_type, sales_df, results_by)

            positions_df = positions_df.to_html()
            sales_df = sales_df.to_html()
            merged_df = merged_df.to_html()
            df = df.to_html()
            
        else:
            no_data = "No data available in the given time intervel"

    hello = "Hello World!"
    context = {
        "hello": hello,
        "search_form": search_form,
        "report_form": report_form,
        "sales_df": sales_df,
        "positions_df": positions_df,
        "merged_df": merged_df,
        "df": df,
        "chart": chart,
        "no_data": no_data
    }
    return render(request, "sales/home.html", context)


class SalesListView(ListView):
    model = Sale
    template_name = "sales/main.html"
    context_object_name = "objects"


class SalesDetailView(DetailView):
    model = Sale
    template_name = "sales/detail.html"


class UploadTemplateView(TemplateView):
    template_name = "sales/from_file.html"


def csv_upload_view(request):
    if request.method == "POST":
        csv_file = request.FILES.get("file")
        obj = CSV.objects.create(file_name = csv_file)

        with open(obj.file_name.path, "r") as f:
            reader = csv.reader(f)
            reader.__next__()
            for row in reader:
                transaction_id = row[1]
                product = row[2]
                quantity = row[3]
                customer = row[4]
                created = parse_date(row[5])

                try:
                    product_obj = Product.objects.get(name__iexact=product)
                except Product.DoesNotExist:
                    product_obj = None
                
                if product_obj:
                    customer_obj, _ = Customer.objects.get_or_create(name=customer)
                    salesman_obj = Profile.objects.get(user=request.user)
                    position_obj = Position.objects.create(product=product_obj, quantity=quantity, created=created)
                    
                    sale_obj, _ = Sale.objects.get_or_create(
                        transaction_id=transaction_id,
                        customer = customer_obj,
                        salesman = salesman_obj,
                        created = created
                    )
                    sale_obj.positions.add(position_obj)
                    sale_obj.save()

    return HttpResponse()
