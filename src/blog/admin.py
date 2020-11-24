from django.contrib import admin

from .models import post,likes,Comment

admin.site.register(post)
admin.site.register(likes)
admin.site.register(Comment)

