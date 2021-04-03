from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Room, Tag


def index(request):
    turn_on_block = True
    context = {
        "turn_on_block": turn_on_block,
    }
    return render(request, "main/index.html", context=context)


class RoomsListView(ListView):
    """Rooms views from generics"""
    model = Room
    template_name = "main/rooms_list.html"
    context_object_name = "rooms"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(RoomsListView, self).get_context_data(**kwargs)
        context["tags_list"] = Tag.objects.all()
        tag = self.request.GET.get("tag")
        if tag:
            context["tag_url"] = "tag={}&".format(tag)
        return context

    def get_queryset(self):
        queryset = super(RoomsListView, self).get_queryset()
        tag = self.request.GET.get("tag")
        if tag is not None:
            return queryset.filter(tags__tag_name=tag)
        return queryset


class RoomDetailView(DetailView):
    """Room detail"""
    model = Room
    context_object_name = "room"
    queryset = Room.objects.all()
