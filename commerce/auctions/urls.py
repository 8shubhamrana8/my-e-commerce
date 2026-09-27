from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("listing/<int:listing_id>", views.view_listing, name="listing_details"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("add_watchlist/<int:id>", views.add_watchlist, name="add_watchlist"),
    path("delete_watchlist/<int:id>", views.delete_watchlist, name="delete_watchlist"),
    path("category", views.list_categories, name="categories"),
    path("category/<int:cat>/", views.category_view, name="category_listing"),
    path("addComment/<int:id>", views.add_comment, name="addComment"),
    path("addBid/<int:id>", views.add_bid, name="addBid"),
    path("close_auction/<int:id>", views.close_auction, name="close_auction"),
]
