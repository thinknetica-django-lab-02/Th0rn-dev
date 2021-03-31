from django.shortcuts import render

# Create your views here.


def index(request):
    turn_on_block = True
    context = {
        "turn_on_block": turn_on_block,
    }
    return render(request, "main/index.html", context=context)
