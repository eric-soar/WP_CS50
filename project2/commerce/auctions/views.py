from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import CreateListingForm
from django.contrib import messages

from .models import User, Listing, Bid, Comment


def index(request):
    listings = Listing.objects.all()
    listing_names = [listing.name for listing in listings]

    return render(request, "auctions/index.html", {
        "listings": listings
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    message = None
    bidder = False
    listing_owner = False

    if request.method == "POST":
        action = request.POST.get("action", None)
        if action == "Add to watchlist":
            request.user.watched_listings.add(listing)
            message = "Successfully added to the watchlist!"
        elif action == "Place bid":
            amount = float(request.POST.get("amount", None))
            if amount <= listing.price:
                message = "ERROR: The bid should be greater than the current bid!"
            else:
                bid = Bid(
                    bidder=request.user,
                    amount=amount,
                    listing=listing
                )

                bid.save()
                message = "Bid created!"

                listing.price = amount
                listing.save()
        elif action == "Close bid":
            last_bid = listing.listing_bids.order_by('amount').last()
            listing.active = False
            listing.winner = last_bid.bidder if last_bid else "No winner"
            listing.save()

    last_bid = listing.listing_bids.order_by('amount').last()
    if last_bid and last_bid.bidder == request.user.username:
        bidder = True
    bidnum = listing.listing_bids.count()

    if request.user.username == listing.listed_by:
        listing_owner = True

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "message": message,
        "number_bids": bidnum,
        "bidder": bidder,
        "listing_owner": listing_owner,
    })


def create_listing(request):
    message = None

    if request.method == "POST":
        form = CreateListingForm(request.POST, request.FILES)

        if form.is_valid():

            listing = Listing(
                active=True,
                name=form.cleaned_data['name'],
                description=form.cleaned_data['description'],
                price=form.cleaned_data['price'],
                image=form.cleaned_data['image'],
                listed_by=request.user,
                category="Non",
            )

            listing.save()  # Save the listing to the database
            message = "Listing created!"
        else:
            messages.error(request, "Error creating the listing. Please check the form.")
    else:
        form = CreateListingForm()

    return render(request, "auctions/create_listing.html", {
        "message": message,
        "form": form
    })

def watchlist(request):

    if request.method == "POST":
        list_rem = request.POST.get('listing_id')
        request.user.watched_listings.remove(list_rem)

    wl_listings = request.user.watched_listings.all()
    return render(request, "auctions/watchlist.html", {
        "user_name": request.user.username,
        "watchlist": wl_listings
    })