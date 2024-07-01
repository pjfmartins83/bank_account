from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import CustomUserCreationForm, TransactionForm
from .models import BankAccount


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        BankAccount.objects.create(owner=self.object, balance=0)
        return response


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        bank_account = BankAccount.objects.get(owner=user)
        context["username"] = user.username
        context["balance"] = bank_account.balance
        return context


class DepositView(LoginRequiredMixin, FormView):
    template_name = "deposit.html"
    form_class = TransactionForm
    success_url = reverse_lazy("dashboard")

    def form_valid(self, form):
        amount = form.cleaned_data["amount"]
        bank_account = BankAccount.objects.get(owner=self.request.user)
        bank_account.deposit(amount)
        return super().form_valid(form)


class WithdrawView(LoginRequiredMixin, FormView):
    template_name = "withdraw.html"
    form_class = TransactionForm
    success_url = reverse_lazy("dashboard")

    def form_valid(self, form):
        amount = form.cleaned_data["amount"]
        bank_account = BankAccount.objects.get(owner=self.request.user)
        if bank_account.withdraw(amount):
            return super().form_valid(form)
        else:
            form.add_error(None, "Insufficient funds")
            return self.form_invalid(form)
