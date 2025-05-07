from django.shortcuts import render, redirect
from .forms import StateForm
from .models import State

def create_state(request):
    if request.method == 'POST':
        form = StateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('state_list')  # Redirect to the list of states after saving
    else:
        form = StateForm()
    return render(request, 'properties/create_state.html', {'form': form})
def state_list(request):
    states = State.objects.all()
    return render(request, 'properties/state_list.html', {'states': states})
from django.shortcuts import render, redirect
from .models import State, District
from django.http import JsonResponse

def add_district(request):
    states = State.objects.all()

    if request.method == "POST":
        state_id = request.POST.get("state")
        district_name = request.POST.get("district")
        if state_id and district_name:
            state = State.objects.get(id=state_id)
            District.objects.create(name=district_name, state=state)
            return redirect('add_district')

    return render(request, 'add_district.html', {'states': states})
def get_districts(request, state_id):
    districts = District.objects.filter(state_id=state_id).values("id", "name")
    return JsonResponse(list(districts), safe=False)

from django.shortcuts import render, redirect
from .models import State, District, Taluk

def add_taluk(request):
    states = State.objects.all()
    districts = District.objects.all()

    if request.method == "POST":
        district_id = request.POST.get("district")
        taluk_name = request.POST.get("taluk")
        if district_id and taluk_name:
            district = District.objects.get(id=district_id)
            Taluk.objects.create(name=taluk_name, district=district)
            return redirect('add_taluk')

    return render(request, 'add_taluk.html', {'states': states, 'districts': districts})
from django.http import JsonResponse

def get_districts(request, state_id):
    districts = District.objects.filter(state_id=state_id).values("id", "name")
    return JsonResponse(list(districts), safe=False)
from django.shortcuts import render, redirect
from .models import State, District, Taluk, RevenueVillage

def add_revenue_village(request):
    states = State.objects.all()

    if request.method == "POST":
        taluk_id = request.POST.get("taluk")
        village_name = request.POST.get("village")
        if taluk_id and village_name:
            taluk = Taluk.objects.get(id=taluk_id)
            RevenueVillage.objects.create(name=village_name, taluk=taluk)
            return redirect('add_revenue_village')

    return render(request, 'add_revenue_village.html', {'states': states})
from django.http import JsonResponse

def get_districts(request, state_id):
    districts = District.objects.filter(state_id=state_id).values("id", "name")
    return JsonResponse(list(districts), safe=False)

def get_taluks(request, district_id):
    taluks = Taluk.objects.filter(district_id=district_id).values("id", "name")
    return JsonResponse(list(taluks), safe=False)

from django.shortcuts import render, redirect
from .models import State, District, Taluk, RevenueVillage, Plot

def add_plot(request):
    states = State.objects.all()

    if request.method == "POST":
        village_id = request.POST.get("revenue_village")
        owner = request.POST.get("owner")
        survey_no = request.POST.get("survey_no")
        sub_division = request.POST.get("sub_division")
        plot_number = request.POST.get("plot_number")
        dimensions = request.POST.get("dimensions")
        facing = request.POST.get("facing")
        pricing_range = request.POST.get("pricing_range")

        if village_id:
            village = RevenueVillage.objects.get(id=village_id)
            Plot.objects.create(
                revenue_village=village,
                owner=owner,
                survey_no=survey_no,
                sub_division=sub_division,
                plot_number=plot_number,
                dimensions=dimensions,
                facing=facing,
                pricing_range=pricing_range,
            )
            return redirect('add_plot')

    return render(request, 'add_plot.html', {'states': states})
def get_revenue_villages(request, taluk_id):
    villages = RevenueVillage.objects.filter(taluk_id=taluk_id).values("id", "name")
    return JsonResponse(list(villages), safe=False)
def home_page(request):
    return render(request, 'home.html', {})
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import UserRegistrationForm

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)  # Log the user in after successful registration
            return redirect('login')  # Redirect to the home page or any other page
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})
from django.contrib.auth.decorators import login_required
# properties/views.py
# properties/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import LoginForm  # Ensure this is correctly imported

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # Authenticate user
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "You have successfully logged in.")
                return redirect('user_dashboard')  # Redirect to the dashboard
            else:
                messages.error(request, "Invalid credentials. Please try again.")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'profile.html')
# properties/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required  # This ensures only logged-in users can access the dashboard
def user_dashboard(request):
    return render(request, 'dashboard.html')
# properties/views.py
from django.contrib.auth import logout
from django.shortcuts import redirect

def user_logout(request):
    logout(request)
    return redirect('home')  # Redirect to the home page after logging out
# properties/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Plot

@login_required
def user_dashboard(request):
    price_range_min = request.GET.get('price_range_min', '')  # Min price for filtering
    price_range_max = request.GET.get('price_range_max', '')  # Max price for filtering
    facing = request.GET.get('facing', '')
    dimensions = request.GET.get('dimensions', '')

    # Initialize the queryset
    plots = Plot.objects.all()

    # Filter based on price range if specified
    if price_range_min:
        try:
            price_range_min = int(price_range_min)  # Ensure the price range is treated as an integer
            plots = plots.filter(price_range__gte=price_range_min)  # Greater than or equal to min price
        except ValueError:
            pass  # Ignore invalid price range input

    if price_range_max:
        try:
            price_range_max = int(price_range_max)  # Ensure the price range is treated as an integer
            plots = plots.filter(price_range__lte=price_range_max)  # Less than or equal to max price
        except ValueError:
            pass  # Ignore invalid price range input

    # Filter based on facing direction (case-insensitive)
    if facing:
        plots = plots.filter(facing__iexact=facing)

    # Filter based on dimensions (partial match)
    if dimensions:
        plots = plots.filter(dimensions__icontains=dimensions)

    context = {
        'plots': plots,
        'price_range_min': price_range_min,
        'price_range_max': price_range_max,
        'facing': facing,
        'dimensions': dimensions,
    }
    return render(request, 'dashboard.html', context)
@login_required
def single_image_view(request,pk):
    row = Plot.objects.filter(id=pk)
    return render(request, 'single_image_view.html', {'row':row})


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .utils import send_interest_email
from .models import Plot  # Assuming you have a Plot model

@csrf_exempt  # Exempt CSRF for AJAX requests
def send_interest_email_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_email = data.get('email')
            plot_id = data.get('plot_id')
            
            # Fetch plot details by ID
            plot = Plot.objects.get(id=plot_id)
            plot_number = plot.plot_number  # Replace this with your actual plot number field
            
            # Send email to the user
            send_interest_email(user_email, plot_number)
            
            return JsonResponse({"success": True, "message": "Email sent successfully!"})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})
    return JsonResponse({"success": False, "message": "Invalid request method"})
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import CartItem, Plot
from django.contrib.auth.decorators import login_required

@login_required
def add_to_cart(request, plot_id):
    try:
        plot = Plot.objects.get(id=plot_id)
        # Check if the plot is already in the cart for the current user
        existing_item = CartItem.objects.filter(user=request.user, plot=plot).first()
        if existing_item:
            return JsonResponse({'error': 'This plot is already in your cart.'})

        # Create a new cart item
        cart_item = CartItem.objects.create(user=request.user, plot=plot)
        return JsonResponse({'success': 'Plot added to cart successfully!'})
    except Plot.DoesNotExist:
        return JsonResponse({'error': 'Plot does not exist.'})

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import CartItem, Plot

@login_required
def view_cart(request):
    # Get the user's cart items
    cart_items = CartItem.objects.filter(user=request.user)


    # Calculate the total price of the cart
    total_price = sum(float(item.plot.price_range) for item in cart_items if item.plot.price_range.isdigit())

    context = {
        'cart_items': cart_items,
        'total_price': total_price
    }

    return render(request, 'view_cart.html', context)

from django.shortcuts import redirect

@login_required
def remove_from_cart(request, cart_item_id):
    try:
        cart_item = CartItem.objects.get(id=cart_item_id, user=request.user)
        cart_item.delete()
        return redirect('view_cart')  # Redirect back to the cart page
    except CartItem.DoesNotExist:
        return redirect('view_cart')  # Handle the case where item is not found

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import CartItem, Plot
from django.http import JsonResponse

@login_required
def checkout(request):
    # Retrieve cart items for the logged-in user
    cart_items = CartItem.objects.filter(user=request.user)

    # Calculate the total price
    total_price = sum(
        float(item.plot.price_range or 0) for item in cart_items if isinstance(item.plot.price_range, (int, float, str))
    )

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }

    return render(request, 'checkout.html', context)

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import CartItem, Order, OrderItem
from django.utils import timezone

@login_required
def process_checkout(request):
    if request.method == "POST":
        # Get the address and payment method from the form
        address = request.POST.get('address')
        payment_method = request.POST.get('payment_method')

        # Retrieve cart items for the logged-in user
        cart_items = CartItem.objects.filter(user=request.user)

        # Calculate the total price
        total_price = sum(
            float(item.plot.price_range or 0) for item in cart_items if isinstance(item.plot.price_range, (int, float, str))
        )

        # Create an Order object
        order = Order.objects.create(
            user=request.user,
            total_price=total_price,
            created_at=timezone.now()  # Optionally add the current time for when the order was created
        )

        # Create OrderItem objects for each cart item
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                plot=cart_item.plot,
                price=cart_item.plot.price_range  # Assuming the price is stored in the plot's price_range field
            )

        # Clear the user's cart after placing the order
        cart_items.delete()

        # Redirect to the order confirmation page
        return redirect('order_confirmation')  # Replace 'order_confirmation' with the actual name of the confirmation page

    return redirect('view_cart')  # If method is not POST, redirect back to the cart


@login_required
def order_confirmation(request):
    return render(request, 'order_confirmation.html')



from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem

@login_required
def my_orders(request):
    """Display the list of orders for the logged-in user."""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')  # Fetch orders for the logged-in user
    return render(request, 'my_orders.html', {'orders': orders})


@login_required
def order_details(request, order_id):
    """Display the details of a specific order."""
    order = get_object_or_404(Order, id=order_id, user=request.user)  # Ensure the order belongs to the logged-in user
    order_items = order.items.all()  # Fetch related OrderItem objects
    return render(request, 'order_details.html', {'order': order, 'order_items': order_items})
from django.shortcuts import render
from .models import Plot

def plot_list(request):
    plots = Plot.objects.all()  # Fetch all Plot objects from the database
    return render(request, 'home.html', {'plots': plots})
