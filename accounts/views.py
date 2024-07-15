from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, FormView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib import messages
from .forms import CustomUserCreationForm, TransactionForm
from .models import BankAccount, Transaction


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True

    def form_invalid(self, form):
        messages.error(self.request, "Invalid Username or Password.")
        return super().form_invalid(form)


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        BankAccount.objects.create(owner=self.object, balance=0)
        messages.success(self.request, "Sign up successful! You can now log in.")
        return response


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        try:
            bank_account = BankAccount.objects.get(owner=user)
        except BankAccount.DoesNotExist:
            bank_account = BankAccount.objects.create(owner=user, balance=0)
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
        messages.success(self.request, f"Successfully deposited {amount}!")
        return super().form_valid(form)


class WithdrawView(LoginRequiredMixin, FormView):
    template_name = "withdraw.html"
    form_class = TransactionForm
    success_url = reverse_lazy("dashboard")

    def form_valid(self, form):
        amount = form.cleaned_data["amount"]
        bank_account = BankAccount.objects.get(owner=self.request.user)
        if bank_account.withdraw(amount):
            messages.success(self.request, f"Successfully withdrew {amount}!")
            return super().form_valid(form)
        else:
            form.add_error(None, "Insufficient funds")
            return self.form_invalid(form)


class TransactionListView(LoginRequiredMixin, ListView):
    template_name = "transaction_list.html"
    context_object_name = "transactions"

    def get_queryset(self):
        user = self.request.user
        bank_account = BankAccount.objects.get(owner=user)
        return Transaction.objects.filter(account=bank_account)
