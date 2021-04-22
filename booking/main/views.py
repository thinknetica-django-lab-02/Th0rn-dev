from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.http.response import HttpResponseRedirect
from django.core.cache import cache

from .models import Room, Tag
from .forms import RoomForm, ProfileFormset, UserForm


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

    def get_context_data(self, **kwargs):
        context = super(RoomDetailView, self).get_context_data(**kwargs)
        room = self.get_object()
        room_key = "room_{}".format(room.id)
        room_views = cache.get(room_key, 0)
        room_views += 1
        cache.set(room_key, room_views, None)
        context["views"] = room_views
        return context


class RoomCreateView(PermissionRequiredMixin, CreateView):
    """Create new Room for Accommodation Facility"""
    model = Room
    form_class = RoomForm
    template_name = "main/room_create_form.html"
    success_url = reverse_lazy('rooms-list')
    login_url = reverse_lazy("index")
    permission_required = ['main.add_room']


class RoomEditView(PermissionRequiredMixin, UpdateView):
    """Update room properties"""
    model = Room
    form_class = RoomForm
    template_name = "main/room_update_form.html"
    success_url = reverse_lazy('rooms-list')
    login_url = reverse_lazy("index")
    permission_required = ['main.change_room']


class ProfileView(LoginRequiredMixin, UpdateView):
    """Profile view"""
    model = User
    form_class = UserForm
    template_name = "main/profile_form.html"
    success_url = reverse_lazy('profile')

    def get_object(self, request):
        """Получение пользователя из request."""
        return request.user

    def get_context_data(self, **kwargs):
        """Добавление в контекст дополнительной формы"""
        context = super().get_context_data(**kwargs)
        context['profile_form'] = ProfileFormset(instance=self.get_object(kwargs['request']))
        return context

    def get(self, request, *args, **kwargs):
        """Метод обрабатывающий GET запрос.
        Переопределяется только из-за self.get_object(request)
        """
        self.object = self.get_object(request)
        return self.render_to_response(self.get_context_data(request=request))

    def form_valid_formset(self, form, formset):
        """Валидация вложенной формы и сохранение обеих форм."""
        if formset.is_valid():
            formset.save(commit=False)
            formset.save()
        else:
            return HttpResponseRedirect(self.get_success_url())
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def post(self, request, *args, **kwargs):
        self.object = self.get_object(request)
        form = self.get_form()
        profile_form = ProfileFormset(self.request.POST, self.request.FILES, instance=self.object)
        if form.is_valid():
            return self.form_valid_formset(form, profile_form)
        else:
            return self.form_invalid(form)


