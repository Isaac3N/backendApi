from django.urls import path
from .views import ExpenseDetailAPIView, ExpenseListAPIView, TotalExpenseStats


urlpatterns = [
    path('', ExpenseListAPIView.as_view()),
    path('<int:id>/', ExpenseDetailAPIView.as_view()),
    path("total-expense/", TotalExpenseStats.as_view(),
         name="total-expense-stats"),
]
