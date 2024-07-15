from django.urls import path
from .views import (
    SignUpView,
    DashboardView,
    DepositView,
    WithdrawView,
    CustomLoginView,
    TransactionListView,
)

urlpatterns = [
        path('login/', CustomLoginView.as_view(), name='login'),
        path("signup/", SignUpView.as_view(), name="signup"),
        path("dashboard/", DashboardView.as_view(), name="dashboard"),
        path("deposit/", DepositView.as_view(), name="deposit"),
        path("withdraw/", WithdrawView.as_view(), name="withdraw"),
        path('transactions/', TransactionListView.as_view(), name='transaction_list'),
]
