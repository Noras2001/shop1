from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required

class RegisterView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'user/register.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user:login')  # O a donde prefieras
        return render(request, 'user/register.html', {'form': form})



@login_required
def profile_view(request):
    return render(request, 'user/profile.html', {})

