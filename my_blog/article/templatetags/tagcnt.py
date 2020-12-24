from django import template
from ..models import ArticleColumn
from ..models import ArticlePost

register = template.Library()

@register.filter
def tagcnt(tag):
    article_list = ArticlePost.objects.all()
    if tag and tag != 'None':
        article_list = article_list.filter(tags__name__in=[tag])
    return article_list.count()