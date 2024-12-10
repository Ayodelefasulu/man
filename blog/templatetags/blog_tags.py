from django import template
from ..models import Post

register = template.Library()

@register.simple_tag
# This function name will be used as the tag name
# You could register it with a different name using "@register.simple_tag(name='my_tag')"
def total_posts():
    """ This function retrieves the number of posts created in the blog """
    return Post.published.count()


# This is the template that will be returned
@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5): # The counts specifies the number of posts to display
    latest_posts = Post.published.order_by('-publish')[:count]
    return ('latest_posts': latest_posts)

