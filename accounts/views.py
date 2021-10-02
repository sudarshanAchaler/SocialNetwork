from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

# Create your views here.
class CustomLoginView(SuccessMessageMixin, LoginView):
    template_name='accounts/login.html'
    fields=['username', 'password']
    redirect_authenticated_user=True
    success_message = 'Login Successful.'

    def get_success_url(self):
        return reverse_lazy('core:home')



class RegisterPage(SuccessMessageMixin, FormView):
    template_name='accounts/register.html'
    form_class= UserCreationForm
    success_url=reverse_lazy('core:home')
    success_message = 'Account created successfully.'

    def form_valid(self, form):
        user=form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage,self).form_valid(form)

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('core:home')
        return super().get(request, *args, **kwargs)


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('core:home')
        else:
            messages.error(request, 'Please correct the above error.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/changePassword.html', {'form': form} ) 