from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    category = models.CharField(max_length=100)
    image = models.URLField()
    def __str__(self):
        return f"CATEGORY_ID : {self.id}, CATEGORY : {self.category}, IMAGE : {self.image}"


class Listing(models.Model):
    picture = models.ImageField(upload_to="auctions", blank=True, null=True)
    pictureurl = models.URLField(blank=True, null=True)
    title = models.CharField(max_length=100)
    price = models.FloatField()
    currentbid = models.FloatField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="type")
    description = models.CharField(max_length=2000)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listedby")
    STATUS = (
        ('OPEN', "OPEN"),
        ('CLOSE', "CLOSED")
    )
    status = models.CharField(max_length=5, choices=STATUS, default='OPEN')
    buyer = models.ForeignKey(User, blank=True, on_delete=models.CASCADE, related_name="boughtby", null=True)
    listingtime = models.DateTimeField(auto_now_add=True)
    closedtime = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    def __str__(self):
        return f"LISTING_ID : {self.id}, PICTURE : {self.picture}, PIC_URL : {self.pictureurl}, TITLE : {self.title}, PRICE : {self.price}, CURRENT_BID : {self.currentbid}, LIST_CATEGORY - {self.category}, DESCRIPTION : {self.description}, SELLER : {self.seller}, STATUS : {self.status}, LIST_TIME : {self.listingtime}, CLOSE_TIME - {self.closedtime}"


class Bid(models.Model):
    bid = models.FloatField()
    note = models.CharField(max_length=250, blank=True, null=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bidon")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidby")
    bidtime = models.DateTimeField(auto_now_add=True)
    feedowner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidlistowner", blank=True, null=True)
    feedback = models.CharField(max_length=250, blank=True, null=True)
    feedtime = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"BID_ID : {self.id}, BID : {self.bid}, NOTE : {self.note}, LISTING : {self.listing}, BIDDER : {self.bidder}, BID_TIME : {self.bidtime}, FEED_OWNER : {self.feedowner}, FEEDBACK : {self.feedback}"


class Comment(models.Model):
    title = models.CharField(max_length=100)
    comment = models.CharField(max_length=1000)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="commenton")
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commentby")
    commenttime = models.DateTimeField(auto_now_add=True)
    feedowner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commentlistowner", blank=True, null=True)
    feedback = models.CharField(max_length=1000, blank=True, null=True)
    feedtime = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"COMMENT_ID : {self.id}, COMMENT : {self.comment}, LISTING : {self.listing}, COMMENTER : {self.commenter}, COMMENT_TIME : {self.commenttime}, FEED_OWNER : {self.feedowner}, FEEDBACK : {self.feedback}"


class Watchlist(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="list")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watcher")
    def __str__(self):
        return f"WATCH_ID : {self.id}, LISTING : {self.listing}, WATCHER : {self.user}"

