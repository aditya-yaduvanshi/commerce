from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createlist", views.createlist, name="createlist"),
    path("watchlist/<str:username>", views.watchlist, name="watchlist"),
    path("watchlist/<str:username>/<int:listid>/<str:action>", views.watchaction, name="watchlist"),
    path("listing", views.postlist, name="listing"),
    path("listing/<int:listid>", views.listing, name="listing"),
    path("listing/<int:listid>", views.listing, name="listing"),
    path("listing/<int:listid>/<str:username>/<str:action>", views.BidComment, name="listing"),
    path("listing/<int:listid>/<str:username>/<str:action>/<int:bidcomid>", views.BidComment, name="listing"),
    path("listing/<str:seller>/<int:listid>/<str:action>", views.closelisting, name="listing"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:category>", views.categories, name="categories"),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)