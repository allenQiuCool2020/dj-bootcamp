from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, Http404, HttpResponseRedirect
from .models import Product
from .forms import ProductModelForm

# Create your views here.
# def bad_view(request, *args, **kwargs):
#     my_request_data = dict(request.GET)
#     new_product = my_request_data.get("new_product")
#     if new_product[0].lower() == "true":
#         print("new_product")
#     return HttpResponse("don't do this")

def search_view(request, *args, **kwargs):
    # print(args, kwargs)
    # return HttpResponse("<h1>Helloworld<h1/>")
    query = request.GET.get('q')
    qs = Product.objects.filter(title__icontains=query[0])
    # print(qs, query)
    context = {
        "name": "Allen",
        "query": query
    }
    return render(request, "home.html", context)

# def product_create_view(request, *args, **kwargs):
#     print(request.POST)
#     print(request.GET)
#     if request.method == "POST":
#         post_data = request.POST or None
#         if post_data != None:
#             my_form = ProductForm(request.POST)
#             if my_form.is_valid():
#                 print(my_form.cleaned_data.get("title"))
#                 title_form_input = my_form.cleaned_data.get("title")
#                 Product.objects.create(title=title_form_input)

#                 print("post_data", post_data)
#     context = {

#     }
#     return render(request, "forms.html", context)
@staff_member_required
def product_create_view(request, *args, **kwargs):
    form = ProductModelForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        # print(form.cleaned_data)
        # data = form.cleaned_data
        # Product.objects.create(**data)
        # print("request.post", request.POST)
        form = ProductModelForm()
        # return HttpResponseRedirect("/success")
    context = {
        "form": form
    }
    return render(request, "forms.html", context)

def product_detail(request, pk):
    try:
        obj = Product.objects.get(id=pk)
    except Product.DoesNotExist:
        raise Http404
    context = {
        "object": obj
    }
    print(request.path)
    # return HttpResponse(f"Product id {obj.id}")
    return render(request, "products/detail.html", context)

def product_api_detail(request, pk):
    try:
        obj = Product.objects.get(id=pk)
    except Product.DoesNotExist:
        return JsonResponse({"message": "not found"})
    return JsonResponse({"id": obj.id})

def product_list_view(request, *args, **kwargs):
    qs = Product.objects.all()
    context = {
        "object_list": qs
    }
    return render(request, "products/list.html", context)
