from django import template
from ..models import Post

register = template.Library()

@register.simple_tag
# This function name will be used as the tag name
# You could register it with a different name using "@register.simple_tag(name='my_tag')"
def total_posts():
    """ This function retrieves the number of posts created in the blog """
    return Post.published.Count()
