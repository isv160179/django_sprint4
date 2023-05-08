from django.core.paginator import Paginator

POST_ON_PAGE = 10


def paginator(request, object_list):
    paginator_obj = Paginator(object_list, POST_ON_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator_obj.get_page(page_number)
    return page_obj
