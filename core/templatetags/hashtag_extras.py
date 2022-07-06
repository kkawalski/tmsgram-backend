import re

from django import template
from django.urls import reverse
from django.utils.html import escape
from django.utils.safestring import mark_safe

from posts.models import HashTag

register = template.Library()

def create_hashtag_link(hashtag):
    if HashTag.objects.filter(text=hashtag.split("#")[-1]):
        url = reverse("search") + f"?search={hashtag.split('#')[-1]}"
        return '<a href="{}">{}</a>'.format(url, hashtag)
    return hashtag


@register.filter()
def hashtag_links(value):
    return mark_safe(re.sub(
        r"(#+[a-zA-Z0-9(_)]{1,})", 
        lambda x: create_hashtag_link(x.group(1)),
        escape(value)
    ))
