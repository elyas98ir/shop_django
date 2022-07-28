from django.shortcuts import render
from django.views import View
from django.views.generic import UpdateView, ListView, DetailView
from accounts.models import User
from orders.models import Order, Payment
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin


class HomeView(View):
    def get(self, request):
        return render(request, 'panel/home.html')


class ProfileView(SuccessMessageMixin, UpdateView):
    fields = ('first_name', 'last_name', 'email', 'image')
    template_name = 'panel/users/profile.html'
    success_url = reverse_lazy('panel:profile')
    success_message = 'اطلاعات پروفایل با موفقیت ویرایش شد.'

    def get_object(self):
        return self.request.user


class OrderListView(ListView):
    template_name = 'panel/users/order_list.html'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderDetailView(DetailView):
    template_name = 'panel/users/order_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_price = self.get_object().get_total_cost(without_discount=True)
        total_cost = self.get_object().get_total_cost(without_discount=False)
        context["total_price"] = total_price
        context["total_cost"] = total_cost
        context["total_discount"] = total_price - total_cost
        return context

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class PaymentListView(ListView):
    template_name = 'panel/users/payment_list.html'

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)
