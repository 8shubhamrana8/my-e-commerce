from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django import forms

from .models import User, Listing, Bid, Comment


def index(request):
    active_listings = Listing.objects.filter(isActive=True)
    return render(request, "auctions/index.html", {"listings" : active_listings})



def category_view(request, cat):

    category_id = None

    for value, label in Listing.categories.choices:
        if value == cat:
            category_id = value
            break 

    if category_id is not None:
        active_listings = Listing.objects.filter(isActive=True, category=category_id)
        display_name = label 
    else:
        active_listings = Listing.objects.none()
        display_name = "Unknown Category"

    return render(request, "auctions/index.html", {
        "listings": active_listings,
        "category_name": display_name,
        "categories": Listing.categories.choices
    })


def list_categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Listing.categories.choices
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


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = [ 'category', 'title', 'description', 'price', 'image_url']

        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter listing title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe your item...'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'placeholder': 'Price'}),
            'image_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Image Url'}),
        }



@login_required
def create_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.placed_by = request.user
            listing.save()
            return redirect(reverse("index"))
        
    else:
        form = ListingForm()

    return render(request, "auctions/create_listing.html", {"form" : form})


@login_required
def watchlist(request):
    watchlist = request.user.watchlist.all()
    return render(request, "auctions/watchlist.html", {"listings" : watchlist})


def view_listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    return render(request, "auctions/listing_details.html", {"listing" : listing})



@login_required
def add_comment(request, id):
    currentuser = request.user
    listingData = Listing.objects.get(pk=id)
    message = request.POST['newComment']
    newComment = Comment(
        author = currentuser,
        listing = listingData,
        comment = message
    )
    newComment.save()
    return HttpResponseRedirect(reverse("listing_details", args=(id, )))



@login_required
def add_watchlist(request, id):
    currentuser = request.user
    listingData = Listing.objects.get(pk=id)
    listingData.watchers.add(currentuser)
    listingData.save()
    return HttpResponseRedirect(reverse("index"))



@login_required
def delete_watchlist(request, id):
    currentuser = request.user
    listingData = Listing.objects.get(pk=id)
    listingData.watchers.remove(currentuser)
    return HttpResponseRedirect(reverse("index"))



@login_required
def close_auction(request, id):
    listingData = Listing.objects.get(pk=id)
    listingData.isActive = False
    listingData.save()
    top_bid = listingData.bids.order_by('-amount').first()
    if top_bid:
        won_by = top_bid.user
        
        message = f"Auction closed. Won by {won_by.username}!"
    else:
        message = "Auction closed with no winning bids."

    return render(request, "auctions/listing_details.html", {
        "listing": listingData,
        "message": message,
        "class": "alert alert-info"
    })
    


@login_required    
def add_bid(request, id):
    newBid = request.POST["newBid"]
    listingData = Listing.objects.get(pk=id)
    if int(newBid) > listingData.highestBid:
        updatedBid = Bid(user = request.user, amount = int(newBid), listing = listingData)
        updatedBid.save()
        return render(request, "auctions/listing_details.html", {
            "listing" : listingData,
            "message" : "Bid updated successfully!!",
            "class" : "alert alert-success"
            })
    else:
        return render(request, "auctions/listing_details.html", {
            "listing" : listingData,
            "message" : "Bid updated failed!!",
            "class" : "alert alert-danger"
            })