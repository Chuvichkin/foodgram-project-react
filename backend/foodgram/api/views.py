from django.http import HttpResponse


# Страница со списком мороженого
def pecipes(request):
    return HttpResponse('ЭТО РЕЦЕПТЫ!!!')


# Страница с информацией об одном сорте мороженого;
# view-функция принимает параметр pk из path()
def ice_cream_detail(request, pk):
    return HttpResponse(f'Мороженое номер {pk}') 
