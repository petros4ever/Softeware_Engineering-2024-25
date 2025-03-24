from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def home_page(request):
    return HttpResponse("<h1>Welcome to our Ebook Store!</h1><p>Start shopping now!</p>")


# shop/views.py
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Book  # Ensure you have a Book model defined in shop/models.py
from .utils import has_internet_connection


def home_page(request):
    """
    Step 1: When the e-shop is opened, check if there's an internet connection.
    If no connection, show a "No Connection" page.
    Otherwise, display the homepage with available books and a search form.
    """
    if not has_internet_connection():
        # Render a template for no connection (we'll create this template next)
        return render(request, 'shop/no_connection.html')

    # Get all books (this simulates our e-shop inventory)
    books = Book.objects.all()
    return render(request, 'shop/home.html', {'books': books})


def search_book(request):
    """
    Step 2: Allow the customer to search for a book.
    It reads a GET parameter 'q' and filters books by title.
    """
    query = request.GET.get('q', '')
    # Search books by title (case-insensitive)
    books = Book.objects.filter(title__icontains=query)
    return render(request, 'shop/search_results.html', {'books': books, 'query': query})


def add_to_cart(request, book_id):
    """
    Step 3: When the user confirms a purchase (clicks "Add to Cart"),
    add the book (by its id) to the session-based cart.
    """
    book = get_object_or_404(Book, pk=book_id)
    # Retrieve the cart from the session; if not present, create an empty list
    cart = request.session.get('cart', [])
    if book.id not in cart:
        cart.append(book.id)
        request.session['cart'] = cart  # Save back to session
    # Redirect back to the homepage (or you could show a cart summary)
    return redirect('home')


# shop/views.py

def view_cart(request):
    # Get the list of book IDs in the cart from the session
    cart = request.session.get('cart', [])
    # Query the Book model for those IDs
    books_in_cart = Book.objects.filter(id__in=cart)

    return render(request, 'shop/cart.html', {
        'books_in_cart': books_in_cart
    })


from django.views.decorators.csrf import csrf_exempt  # if you need to skip CSRF for testing

@csrf_exempt
def checkout(request):
    """
    Step 5: Display or confirm payment details.
    - On GET: show a payment form.
    - On POST: process payment details and move to step 6.
    """
    if request.method == 'GET':
        # Show the payment form
        return render(request, 'shop/payment_form.html')

    elif request.method == 'POST':
        # Step 6: "Communicate" with bank or payment gateway
        card_number = request.POST.get('card_number')
        expiration = request.POST.get('expiration')
        cvv = request.POST.get('cvv')

        # (We'll just simulate success for now)
        success = simulate_payment_gateway(card_number, expiration, cvv)

        if success:
            # Clear the cart, then show success page
            request.session['cart'] = []
            return render(request, 'shop/payment_success.html')
        else:
            # Show an error or redirect back with a message
            return render(request, 'shop/payment_form.html', {
                'error': 'Payment failed! Please check your details.'
            })

def simulate_payment_gateway(card_number, expiration, cvv):
    """
    A fake function simulating communication with a bank or payment gateway.
    In reality, you'd integrate with Stripe/PayPal/etc.
    """
    # We'll just accept any non-empty values as "valid"
    if card_number and expiration and cvv:
        return True
    return False

