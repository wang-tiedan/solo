from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, ProductCategory, Category, ProductModification, Order
from django.db.models import Q, Count, Max, Min, Avg
import plotly.express as px
from plotly.offline import plot
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from shopping.models import Cart, CartItem
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.forms import AuthenticationForm



def product_detail(request):
    query = request.GET.get('query', '')
    min_price = request.GET.get('min_price', None)
    max_price = request.GET.get('max_price', None)
    sort = request.GET.get('sort', 'name') 
    page_number = request.GET.get('page', 1)

    products = Product.objects.all()

    if query:
        products = products.filter(Q(product_id__icontains=query) | Q(name__icontains=query) | Q(sku__icontains=query))

    if min_price and min_price.isdigit():
        products = products.filter(price__gte=min_price)
    if max_price and max_price.isdigit():
        products = products.filter(price__lte=max_price)

    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')

    # paginate products
    paginator = Paginator(products, 50)  
    page_obj = paginator.get_page(page_number)

    # create a line chart
    current_products = page_obj.object_list
    df = list(current_products.values('product_id', 'name', 'price'))

    if df:
        line_fig = px.line(
            df, x="product_id", y="price", title="Product Price Chart",
            labels={"price": "Price", "product_id": "Product ID"},
            text=[product['name'] for product in df]
        )
        line_fig.update_traces(textposition='top center')
        line_plot_div = plot(line_fig, output_type='div', include_plotlyjs=False)
    else:
        line_plot_div = "No data available for plotting."

    # Create a pie chart
    price_ranges = [
        (0, 100), (101, 200), (201, 300), (301, 400), (401, 999999)
    ]
    counts = [
        products.filter(price__gte=range[0], price__lte=range[1]).count()
        for range in price_ranges
    ]
    pie_fig = px.pie(
        names=["0-100", "101-200", "201-300", "301-400", "401+"],
        values=counts,
        title="Product Distribution by Price Range"
    )
    pie_plot_div = plot(pie_fig, output_type='div', include_plotlyjs=False)

    # calculate max, min and average price
    page_max_price = current_products.aggregate(Max('price'))['price__max']
    page_min_price = current_products.aggregate(Min('price'))['price__min']
    page_avg_price = current_products.aggregate(Avg('price'))['price__avg']

    # sanitize the values
    page_max_price = round(page_max_price, 3) if page_max_price is not None else None
    page_min_price = round(page_min_price, 3) if page_min_price is not None else None
    page_avg_price = round(page_avg_price, 3) if page_avg_price is not None else None

    return render(request, 'products/product_detail.html', {
        'page_obj': page_obj,
        'line_plot_div': line_plot_div,
        'pie_plot_div': pie_plot_div,
        'page_max_price': page_max_price,
        'page_min_price': page_min_price,
        'page_avg_price': page_avg_price
    })


def product_category_detail(request, product_id):
    try:
        categories = ProductCategory.objects.filter(product__product_id=product_id)
        return render(request, 'products/product_category_detail.html', {'categories': categories})
    except ProductCategory.DoesNotExist:
      
        raise Http404("Product categories not found for the given product ID.")

def category_detail(request, category_id):
    try:
        category = get_object_or_404(Category, pk=category_id)
        return render(request, 'products/category_detail.html', {'category': category})
    except Category.DoesNotExist:
        
        raise Http404("Category not found for the given category ID.")



@login_required(login_url='user_login') 
@staff_member_required(login_url='user_login')  
def product_modifications(request):
    try:
        """A view to display all product modifications."""
        # Get all product modifications and annotate counts for creators and last modified creators
        modifications = ProductModification.objects.all().order_by('-creation_time')

        # Pagination
        paginator = Paginator(modifications, 50)  # Show 50 modifications per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        creator_counts = ProductModification.objects.values('creator_id').annotate(creator_count=Count('creator_id'))
        last_modified_counts = ProductModification.objects.values('last_modified_by_id').annotate(last_modified_count=Count('last_modified_by_id'))
        
        # Create lists for bar chart data
        creator_ids = [item['creator_id'] for item in creator_counts]
        creator_counts_list = [item['creator_count'] for item in creator_counts]
        last_modified_ids = [item['last_modified_by_id'] for item in last_modified_counts]
        last_modified_counts_list = [item['last_modified_count'] for item in last_modified_counts]

        return render(request, 'products/product_modifications.html', {
            'page_obj': page_obj,
            'creator_ids': creator_ids,
            'creator_counts_list': creator_counts_list,
            'last_modified_ids': last_modified_ids,
            'last_modified_counts_list': last_modified_counts_list
        })
    except EmptyPage:
        
        return render(request, 'error.html', {'error_message': 'Page not found.'})
    except PageNotAnInteger:
        
        return render(request, 'error.html', {'error_message': 'Invalid page number.'})
    except Exception as e:
       
        return render(request, 'error.html', {'error_message': str(e)})

# def product_modifications(request):
#    """A view to display all product modifications."""
#    modifications = ProductModification.objects.all().order_by('-creation_time')
#    return render(request, 'products/product_modifications.html', {'modifications': modifications})

def creator_products(request, creator_id):
    modifications = ProductModification.objects.filter(creator_id=creator_id)
    product_ids = modifications.values_list('product', flat=True).distinct()
    products = Product.objects.filter(product_id__in=product_ids).prefetch_related('productcategory_set')
    context = {
        'products': products,
        'creator_id': creator_id
    }

    return render(request, 'products/creator_products.html', context)


def last_modified_by_creator(request, creator_id):
    modifications = ProductModification.objects.filter(last_modified_by_id=creator_id).order_by('-last_modified_time')
    context = {
        'modifications': modifications,
        'creator_id': creator_id  
    }
    return render(request, 'products/last_modified_by_creator.html', context)


@csrf_protect
def user_login(request):
    error_message = None
    next_url = request.POST.get('next', '/')  

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect(next_url) 
            else:
                error_message = 'Invalid username or password.'
        else:
            error_message = 'Invalid form submission.'
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form, 'error_message': error_message})




def admin_logout(request):
    next_url = request.POST.get('next', reverse('product-detail'))
    logout(request)  
    response = HttpResponseRedirect(reverse('user_login') + '?next=' + next_url)
    return response

def user_logout(request):
    next_url = request.POST.get('next', reverse('product-detail'))
    logout(request)  
    response = HttpResponseRedirect(reverse('user_login') + '?next=' + next_url)
    return response

def some_view(request):
    product_id = ...  
    login_url = f"/login/?next=/product/{product_id}/&back=/product/{product_id}/"
    return redirect(login_url)

def view_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        items = cart.items.all()
        total_price = sum(item.product.price * item.quantity for item in items) 
        return render(request, 'products/view_cart.html', {
            'items': items, 
            'total_price': total_price  
        })
    else:
        return redirect('user_login')
    

def add_to_cart(request, product_id):
    if not request.user.is_authenticated:
        
        return JsonResponse({'success': False, 'error': 'User not logged in'}, status=403)

    product = get_object_or_404(Product, product_id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if created:
        cart_item.quantity = 1
    else:
        cart_item.quantity += 1
    
    cart_item.save()

    cart_item_count = cart.items.count()
    cart_total_quantity = sum(item.quantity for item in cart.items.all())
    
    return JsonResponse({
        'success': True, 
        'cartItemCount': cart_item_count, 
        'cartTotalQuantity': cart_total_quantity
    })



def clear_cart(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    
    # Clear the user's cart
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart.items.all().delete()
    
    return JsonResponse({'success': True})



def remove_from_cart(request, item_id):
    if request.user.is_authenticated:
        item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        item.delete()
        return redirect('view_cart')
    else:
        return redirect('user_login')
    
    

@require_POST
def update_cart_item(request):
    item_id = request.POST.get('item_id')
    change = int(request.POST.get('change'))
    if request.user.is_authenticated:
        item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        
        # define
        new_quantity = item.quantity + change
        
        # save the new quantity
        if new_quantity > 0:
            item.quantity = new_quantity
            item.save()
            new_total_price = item.quantity * item.product.price
        else:
            item.delete()
            new_quantity = 0
            new_total_price = 0
        
        # calculate total price
        cart = Cart.objects.get(user=request.user)
        total_price = sum(cart_item.product.price * cart_item.quantity for cart_item in cart.items.all())
        
        # back to cart page
        return JsonResponse({
            'success': True,
            'new_quantity': new_quantity,
            'new_total_price': new_total_price,
            'total_price': total_price
        })
    else:
        return JsonResponse({'success': False}, status=403)



@login_required(login_url='user_login')  # make sure user is authenticated before accessing this view
def checkout(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()
    
    # calculate total price
    for item in items:
        item.total_price = item.product.price * item.quantity  
    
    total_price = sum(item.total_price for item in items)  # calculate total price
    
    context = {
        'user': request.user,
        'items': items,
        'total_price': total_price
    }
    return render(request, 'checkout.html', context)

def process_payment(request):
    if request.method == 'POST':
        try:
            
            user = request.user
            



def payment_success(request):
    return render(request, 'payment_success.html')


@login_required(login_url='user_login')
def order_list(request):
    if not request.user.is_staff:  # Checks if the user is not an admin
        return redirect('product-detail')

    # Fetch all orders (admin sees all orders)
    orders = Order.objects.all().order_by('-created_at')

    is_empty = False
    if orders.count() == 0:
        is_empty = True

    paginator = Paginator(orders, 20)  # Show 10 merchandise per page.

    page_number = request.GET.get('page')
    orders = paginator.get_page(page_number)

    # Pass the orders to the template
    return render(request, 'order_list.html', {'orders': orders, 'is_empty': is_empty})

