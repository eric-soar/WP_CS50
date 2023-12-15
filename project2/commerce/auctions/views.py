from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
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


def create_listing(request):
    message = None

    if request.method == "POST":
        form = CreateListingForm(request.POST, request.FILES)

        if form.is_valid():

            listing = Listing(
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