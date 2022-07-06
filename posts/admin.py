from django.contrib import admin

from posts.models import Post, HashTag


admin.site.register(Post)
admin.site.register(HashTag)
