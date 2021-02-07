from django.contrib import admin

from .models import post,likes,Comment,blog

admin.site.register(post)
admin.site.register(blog)
admin.site.register(likes)
admin.site.register(Comment)


