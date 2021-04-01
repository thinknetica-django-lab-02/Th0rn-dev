from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Room


def index(request):
    turn_on_block = True
    context = {
        "turn_on_block": turn_on_block,
    }
    return render(request, "main/index.html", context=context)


class RoomsList(ListView):
    """Rooms views from generics"""
    model = Room
    template_name = "main/rooms_list.html"
    context_object_name = "rooms"


class RoomDetail(DetailView):
    """Room detail"""
    model = Room
    context_object_name = "room"
    queryset = Room.objects.all()
