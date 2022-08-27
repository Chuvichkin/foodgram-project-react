from django.http import HttpResponse
from django.shortcuts import render


# Главная страница
def index(request):
    # Адрес шаблона сохраним в переменную, это не обязательно, но удобно
    template = 'foodgram/index.html'
    # Строку, которую надо вывести на страницу, тоже сохраним в переменную
    title = 'Мой ушлепский проект'
    # Словарь с данными принято называть context
    context = {
        # В словарь можно передать переменную
        'title': title,
        # А можно сразу записать значение в словарь. Но обычно так не делают
        'text': 'Главная страница моего ушлепского проекта',
    }
    # Третьим параметром передаём словарь context
    return render(request, template, context)


# Страница с информацией об одном сорте мороженого;
# view-функция принимает параметр pk из path()
def ice_cream_detail(request, pk):
    return HttpResponse(f'Мороженое номер {pk}')
