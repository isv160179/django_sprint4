from django.conf import settings
from django.core.paginator import Paginator


def paginator(request, object_list):
    paginator_obj = Paginator(object_list, settings.POST_ON_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator_obj.get_page(page_number)
    return page_obj
