from django.contrib import messages
from .models import Category, Product, UserCreateForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404
from app.models import Product, ContactForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from django.contrib.auth.models import User


# Create your views here.# Create your views here.
# Build Catalog Views
def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    page = Paginator(products, 4)
    page_number = request.GET.get('page')
    try:
        page_obj = page.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = page.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = page.page(page.num_pages)
    return render(request, "app/home.html",{'products':products,'categories':categories, 'page_obj': page_obj})

def product_list(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    categoryID = request.GET.get('category')
    if categoryID:
        product = Product.objects.filter(id=categoryID)
    else:
        product = Product.objects.all()
    return render(request, 'app/product_list.html',{
                                                    'products':products,
                                                    'categories':categories,
                                                    'categoryID':categoryID})

def product_details(request, slug):
    product = Product.objects.get(slug=slug)
    return render(request, 'app/product_details.html',{'product':product}) 

def about(request):
    return render(request, 'app/about.html')

def testimonial(request):
    return render(request, 'app/test.html')

def contact(request):
    return render(request, 'app/contact.html')

def blog(request):
    return render(request, 'app/blog.html')

def checkout(request):
    product = Product.objects
    context={
        'product':product,
    }
    return render(request, 'app/checkout.html',context)

def transaction_success(request):
    return render(request, 'app/success.html')


def signup(request):
    if request.method == "POST":
        form = UserCreateForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user = authenticate(
                username = form.cleaned_data['username'],
                password = form.cleaned_data['password1']
            )
            login(request, new_user)
            return render(request, 'app/home.html')
    else:
        form = UserCreateForm()
    
    context = {
        'form':form
    }
    return render(request, 'registration/signup.html',context)

def user_profile(request):
    user = User.objects.get(id = request.user.id)
    context={
        'user':user
    }
    return render(request, 'profile_update.html', context)


def update_profile(request):
        if request.method =="POST":
            fname = request.POST.get('fname')
            lname = request.POST.get('lname')
            # email = request.POST.get('email')
            # username =request.POST.get('username')
            password = request.POST.get('password')

            try:
                user = User.objects.get(id=request.user.id)
                user.first_name = fname
                user.last_name = lname

                if password != None and password !="":
                    user.set_password(password)
                user.save()
                messages.success(request, "Details has been updated")
                return redirect('user_profile')

            except:
                messages.error(request, "Profile updation failed.") 
            return render(request, 'profile_update.html') 
        return render(request, 'profile_update.html')

# cart view here
@login_required(login_url="/accounts/login/")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/accounts/login")
def cart_detail(request):
    return render(request, 'Cart/cart_detail.html')


def contactForm(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']

        new_messages = ContactForm.objects.create(name=name,email=email,subject=subject,message=message)
        new_messages.save()
        messages.success(request, "Your messages has been successfully send! we will connect with asap..Thank you")
        return redirect("contact")

