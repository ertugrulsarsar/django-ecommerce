from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

class BaseListView(ListView):
    template_name = None
    context_object_name = 'objects'
    paginate_by = 10

class BaseDetailView(DetailView):
    template_name = None
    context_object_name = 'object'

class BaseCreateView(LoginRequiredMixin, CreateView):
    template_name = None
    success_url = None

class BaseUpdateView(LoginRequiredMixin, UpdateView):
    template_name = None
    success_url = None

class BaseDeleteView(LoginRequiredMixin, DeleteView):
    template_name = None
    success_url = None 