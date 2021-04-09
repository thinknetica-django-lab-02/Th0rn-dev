from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Room, Tag
from .forms import RoomForm, ProfileFormset


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
            return queryset.filter(tags__tag_name=tag).order_by("id")
        return queryset


class RoomDetailView(DetailView):
    """Room detail"""
    model = Room
    context_object_name = "room"
    queryset = Room.objects.all()


class RoomCreateView(LoginRequiredMixin, CreateView):
    """Create new Room for Accommodation Facility"""
    model = Room
    form_class = RoomForm
    template_name = "main/room_create_form.html"
    success_url = reverse_lazy('rooms-list')
    login_url = reverse_lazy("index")


class RoomEditView(LoginRequiredMixin, UpdateView):
    """Update room properties"""
    model = Room
    form_class = RoomForm
    template_name = "main/room_update_form.html"
    success_url = reverse_lazy('rooms-list')
    login_url = reverse_lazy("index")


class ProfileView(LoginRequiredMixin, UpdateView):
    """Profile view"""
    formset_class = ProfileFormset
    template_name = "main/profile_form.html"
    success_url = reverse_lazy('profile')
    login_url = '/admin/login/?next=/accounts/profile/'
    fields = ['first_name', 'last_name', 'email']

    def get_object(self, queryset=None):
        return self.request.user
