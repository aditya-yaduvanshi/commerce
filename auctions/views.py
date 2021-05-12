from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Max
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import *
from .forms import *
from django.utils.timezone import now


def index(request, watch_status='', listing='', active_status=''):
    watchlist = Watchlist.objects.all()
    watchuser = [wl.user for wl in watchlist]
    lists = [wl.listing for wl in watchlist]
    return render(request, "auctions/index.html",{
        "listings" : Listing.objects.all(),
        "watchuser" : watchuser,
        "watchlist" : lists,
        "watch_status" : watch_status,
        "res_list" : listing,
        "active_status" : active_status,
    })


def categories(request, category=''):
    watchlist = Watchlist.objects.all()
    watchuser = [wl.user for wl in watchlist]
    lists = [wl.listing for wl in watchlist]
    if category != '':
        cat = Category.objects.get(category=category)
        Lists = Listing.objects.filter(category=cat.id)
        return render(request, "auctions/categories.html",{
            "listings" : Lists,
            "watchuser" : watchuser,
            "watchlist" : lists,
        })
    else: 
        return render(request, "auctions/categories.html",{
            "categories" : Category.objects.all(),
            "watchuser" : watchuser,
            "watchlist" : lists,
        })


def search(request, watch_status='', listing=''):
    if request.method == "GET":
        query = request.GET["query"]
        searchresults = []
        Listings = Listing.objects.all()
        results_count = 0
        if query != "":
            for listing in Listings:
                if (query.lower() in (listing.title.lower() or listing.category.lower())) or (query.lower() in (listing.description.lower() or listing.status.lower())):
                    searchresults.append(listing)
                    results_count = results_count + 1        
        watchlist = Watchlist.objects.all()
        watchuser = [wl.user for wl in watchlist]
        lists = [wl.listing for wl in watchlist]
        return render(request, "auctions/search.html",{
            "listings" : Listing.objects.all(),
            "watchuser" : watchuser,
            "watchlist" : lists,
            "watch_status" : watch_status,
            "res_list" : listing,
            "searchresults" : searchresults,
            "query" : query,
            "results_count" : results_count,
        })


def watchlist(request, username, watch_status='', listtitle=''):
    user = User.objects.get(username=username)
    return render(request, "auctions/watchlist.html",{
        "watchlist" : Watchlist.objects.filter(user=user),
        "watch_status" : listtitle + "  " + watch_status,
    }) 


def watchaction(request, username, listid, action):
    user = User.objects.get(username=username)
    LISTING = Listing.objects.get(pk=listid)
    prev_url = request.META.get("HTTP_REFERER")
    status = None
    if action == "add":
        watch = Watchlist(listing=LISTING, user=user)
        watch.save()
        status = "Added"
    elif action == "remove":
        watch = Watchlist.objects.filter(listing=LISTING,user=user)
        watch.delete()
        status = "Removed"
    else:
        status = "Failed"
    if "listing" in prev_url:
        return listing(request, listid=LISTING.id, watch_status=status)
    elif "watchlist" in prev_url:
        return watchlist(request, username=username, watch_status=status, listtitle=LISTING.title)
    else:
        return index(request, watch_status=status, listing=LISTING)


@login_required(login_url='login')
def createlist(request):
    return render(request, "auctions/createlist.html",{
        "listform" : ListingForm(),
    })


def postlist(request):
    if request.method == "POST":
        listform = ListingForm(request.POST)
        if listform.is_valid():
            pic = listform.cleaned_data["picture"]
            picurl = listform.cleaned_data["pictureurl"]
            title = listform.cleaned_data["title"]
            price = listform.cleaned_data["price"]
            cate = listform.cleaned_data["category"]
            desc = listform.cleaned_data["description"]
            us = request.POST["hiddenuser"]
            user = User.objects.get(username=us)
            category = Category.objects.get(category=cate)
            LISTING = Listing(picture=pic, pictureurl=picurl, title=title, price=price, currentbid=price, category=category, description=desc, seller=user)
            LISTING.save()
            return listing(request, listid=LISTING.id, list_status="Your listing is posted successfully!")
        else: 
            return render(request, "auctions/createlist.html",{
                "listform" : listform,
                "message" : "Please correct invalid entries than try again."
            })
    else:
        return render(request, "auctions/createlist.html",{
                "listform" : ListingForm(),
                "message" : "Invalid method request!"
            })



def listing(request, listid, watch_status='', list_status='', action_status='', method_status='', feedstatus='', close_status=''):
    watchlist = Watchlist.objects.all()
    watchuser = [wl.user for wl in watchlist]
    lists = [wl.listing for wl in watchlist]
    List = Listing.objects.get(pk=listid)
    return render(request, "auctions/listing.html",{
        "listing" : List,
        "bids" : Bid.objects.filter(listing=List),
        "comments" : Comment.objects.filter(listing=List),
        "bidform" : BidForm(),
        "commentform" : CommentForm(),
        "bidfeed" : BidFeed(),
        "commentfeed" : CommentFeed(),
        "watch_status" : watch_status,
        "list_status" : list_status,
        "watchuser" : watchuser,
        "watchlist" : lists,
        "action_status" : action_status,
        "method_status" : method_status,
        "feedstatus" : feedstatus,
        "close_status" : close_status,
    })




def BidComment(request, listid, username, action, bidcomid=''):
    if request.method == "POST":
        LISTING = Listing.objects.get(pk=listid)
        user = User.objects.get(username=username)
        action_status = None
        feedstatus = None
        if action == "bidnow":
            bidform = BidForm(request.POST)
            if bidform.is_valid():
                bid = bidform.cleaned_data["bid"]
                note = bidform.cleaned_data["optionalnote"]
                BID = Bid(bid=bid, note=note, listing=LISTING, bidder=user)
                BID.save()
                LISTING.currentbid = bid
                LISTING.save()
                action_status = "Bid posted successfully!"
        elif action == "commentnow":
            commentform = CommentForm(request.POST)
            if commentform.is_valid():
                comment = commentform.cleaned_data["comment"]
                title = commentform.cleaned_data["title"]
                COMMENT = Comment(comment=comment, title=title, listing=LISTING, commenter=user)
                COMMENT.save()
                action_status = "Comment posted successfully!"
        elif action == "bidreply":
            bidfeed = BidFeed(request.POST)
            if bidfeed.is_valid():
                feedback = bidfeed.cleaned_data["feedback"]
                BID = Bid.objects.get(pk=bidcomid, listing=LISTING)
                BID.feedback = feedback
                BID.feedowner = user
                BID.save()
                feedstatus = "Bid"
        elif action == "commentreply":
            commentfeed = CommentFeed(request.POST)
            if commentfeed.is_valid():
                feedback = commentfeed.cleaned_data["feedback"]
                COMMENT = Comment.objects.get(pk=bidcomid, listing=LISTING)
                COMMENT.feedback = feedback
                COMMENT.feedowner = user
                COMMENT.save()
                feedstatus = "Comment"
        else:
            return listing(request, listid=listid, action_status="Invalid action request!")
        
        return listing(request, listid=listid, action_status=action_status, feedstatus=feedstatus)
    else:
        return listing(request, listid=listid, method_status="Invalid Method Request!")



def closelisting(request, seller, listid, action):
    LIST = Listing.objects.get(pk=listid)
    if action == "close":
        LIST.status = "CLOSE"
        LIST.closedtime = now()
        bids = Bid.objects.filter(listing=LIST)
        maxbid = bids.aggregate(Max('bid'))
        maxbiduser = Bid.objects.get(listing=LIST, bid=maxbid["bid__max"])
        LIST.buyer = maxbiduser.bidder
        LIST.save()
        close_status = "Listing Closed Successfully!"
        return listing(request, listid=listid, close_status=close_status)
    else:
        return listing(request, listid=listid, close_status="Invalid Request!")



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
