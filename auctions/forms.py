from django import forms
from .models import *



class ListingForm(forms.Form):
  picture = forms.ImageField(required=False, help_text="----- OR -----")
  pictureurl = forms.URLField(required=False, widget=forms.URLInput())
  title = forms.CharField(required=True, widget=forms.TextInput())
  price = forms.FloatField(required=True, widget=forms.NumberInput())
  category = forms.ChoiceField(choices=[(cat.category, cat.category) for cat in Category.objects.all()])
  description = forms.CharField(required=True, widget=forms.Textarea(attrs={
    "height" : "32px",
    "width" : "100px"
  }))
  

class BidForm(forms.Form):
  bid = forms.FloatField(required=True, widget=forms.NumberInput())
  optionalnote = forms.CharField(required=False, widget=forms.TextInput())



class CommentForm(forms.Form):
  title = forms.CharField(required=False, widget=forms.TextInput())
  comment = forms.CharField(required=True, widget=forms.Textarea(attrs={
    "height" : "32px"
  }))

class BidFeed(forms.Form):
  feedback = forms.CharField(required=True, widget=forms.TextInput())

class CommentFeed(forms.Form):
  feedback = forms.CharField(required=True, widget=forms.Textarea())

class ListFilter(forms.Form):
  category = forms.ChoiceField(choices=[(cat.category, cat.category) for cat in Category.objects.all()])
  STATUS = (
    ("OPEN","OPEN"),
    ("CLOSE", "CLOSED")
  )
  list_status = forms.ChoiceField(choices=STATUS, required=False)
  start_bid = forms.FloatField(required=False, widget=forms.NumberInput())
  current_bid = forms.FloatField(required=False, widget=forms.NumberInput())


