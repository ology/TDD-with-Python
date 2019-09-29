from django.shortcuts import render
from lists.models import Item

def home_page(request):
    if request.method == 'POST':
        item_text = request.POST['item_text']
        Item.objects.create(text=item_text)
    else:
        item_text = ''

    return render(request, 'home.html', {
        'new_item_text': item_text, }
    )
