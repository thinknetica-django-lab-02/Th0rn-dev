from django.shortcuts import render

# Create your views here.


def index(request):
    turn_on_block = True
    user = request.user
    context = {
        "turn_on_block": turn_on_block,
        "user": user
    }
    return render(request, "main/index.html", context=context)
