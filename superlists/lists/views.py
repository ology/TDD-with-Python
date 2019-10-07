from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from lists.models import Item, List

def home_page(request):
    return render(request, 'home.html')

def view_list(request, list_id):
    my_list = List.objects.get(id=list_id)
    return render(request, 'list.html', {'list': my_list})

def new_list(request):
    my_list = List.objects.create()
    item = Item.objects.create(text=request.POST['item_text'], list=my_list)

    try:
        item.full_clean()
    except ValidationError:
        error = 'Empty list item not allowed'
        return render(request, 'home.html', {'error': error})

    return redirect(f'/lists/{my_list.id}/')

def add_item(request, list_id):
    my_list = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], list=my_list)
    return redirect(f'/lists/{my_list.id}/')
