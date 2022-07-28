from django.shortcuts import render, redirect
from django.views import View
from . import forms
from django.contrib import messages
from .inc import create_code, verify_code
from django.contrib.auth import logout, login
from accounts.models import User


class HomeView(View):
    def get(self, request):
        return render(request, 'base.html')


class UserOTPSendView(View):
    form_class = forms.UserOTPSendForm

    def get(self, request):
        form = self.form_class
        return render(request, 'accounts/otp_send.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            create_code(form.cleaned_data['phone_number'])
            request.session['phone_number'] = form.cleaned_data['phone_number']
            return redirect('accounts:otp_verify')
        return render(request, 'accounts/otp_send.html', {'form': form})


class UserOTPVerifyView(View):
    form_class = forms.UserOTPVerifyForm

    def get(self, request):
        form = self.form_class
        return render(request, 'accounts/otp_verify.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        phone_number = request.session['phone_number']
        if form.is_valid():
            if verify_code(phone_number, form.cleaned_data['code']):
                user = User.objects.get(phone_number=phone_number)
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'کد وارد شده اشتباه است', 'danger')
                return redirect('accounts:otp_verify')
        return render(request, 'accounts/otp_verify.html', {'form': form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')
