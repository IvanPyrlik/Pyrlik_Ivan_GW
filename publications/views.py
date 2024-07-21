from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from publications.forms import PublicationForm
from publications.models import Publication


class PublicationsListView(ListView):
    """
    Список публикаций.
    """
    model = Publication

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_active=True)
        return queryset


class PublicationCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """
    Cоздание публикации.
    """
    model = Publication
    form_class = PublicationForm
    success_url = reverse_lazy('publications:list')
    permission_required = "publications.add_publication"

    def get_form_kwargs(self):
        kwargs = super(PublicationCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class PublicationsDetailView(DetailView):
    """
    Детали публикации.
    """
    model = Publication

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(pk=self.kwargs.get('pk'))
        return queryset

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        publication_item = Publication.objects.get(pk=self.kwargs.get('pk'))
        context_data['publication'] = publication_item
        context_data['object_list'] = Publication.objects.filter(id=self.kwargs.get('pk'))
        return context_data


class PublicationsUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """
    Изменение публикации.
    """
    model = Publication
    form_class = PublicationForm
    permission_required = "publications.change_publication"

    def get_success_url(self):
        return reverse_lazy('publications:detail', kwargs={'pk': self.object.pk})

    def get_form_kwargs(self):
        kwargs = super(PublicationsUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class PublicationsDeleteView(LoginRequiredMixin, DeleteView):
    """
    Удаление публикации.
    """
    model = Publication
    success_url = reverse_lazy('publications:list')
    permission_required = "publications.delete_publication"


@login_required
def get_user_public(request):
    """
    Получение публикаций пользователя.
    """
    publications_list = Publication.objects.filter(owner_id=request.user.pk)
    publications_count = Publication.objects.filter(owner_id=request.user.pk).count()
    publications_count_active = Publication.objects.filter(
        owner_id=request.user.pk,
        is_active=True
    ).count()
    publications_count_paid = Publication.objects.filter(
        owner_id=request.user.pk,
        paid_publication=True
    ).count()

    context_data = {
        'publications_count': publications_count,
        'publications_count_active': publications_count_active,
        'publications_count_paid': publications_count_paid,
        'publications_list': publications_list
    }

    return render(request, 'publications/user_public.html', context_data)
