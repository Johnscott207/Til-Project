from django.contrib import admin
from followers.models import Follower


class FollowerAdmin(admin.ModelAdmin):
    pass

admin.site.register(Follower,FollowerAdmin)