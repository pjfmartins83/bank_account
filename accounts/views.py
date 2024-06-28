from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CustomUserCreationForm
from .models import BankAccount


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        BankAccount.objects.create(owner=self.object, balance=0)
        return response
