from django.contrib import admin
from .models import Listing, Bid, Comment

# Register your models here.

class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "price")

class BidAdmin(admin.ModelAdmin):
    list_display = ("id", "bidder", "amount")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "comment")

admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)