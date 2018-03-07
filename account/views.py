from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import REDIRECT_FIELD_NAME, authenticate
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.utils.http import is_safe_url
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView, RedirectView
from .models import Account

from .forms import UserAuthenticationForm, UserRegisterForm


class LoginView(FormView):
    """
    Provides the ability to login as a user with a username and password
    """
    success_url = '/post/list'
    form_class = UserAuthenticationForm
    redirect_field_name = REDIRECT_FIELD_NAME
    template_name = "account/login.html"

    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/post/list')
        
        # Sets a test cookie to make sure the user has cookies enabled
        request.session.set_test_cookie()

        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        auth_login(self.request, form.get_user())

        # If the test cookie worked, go ahead and
        # delete it since its no longer needed
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()

        return super(LoginView, self).form_valid(form)

    def get_success_url(self):
        redirect_to = self.request.GET.get(self.redirect_field_name)
        if not is_safe_url(url=redirect_to, host=self.request.get_host()):
            redirect_to = self.success_url
        return redirect_to

class LogoutView(RedirectView):
    """
    Provides users the ability to logout
    """
    url = '/account/login/'

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)

class RegisterView(FormView):
    """
    Provides the ability to a visitor to register as new user 
    with an username, an email and a password
    """
    success_url = '/post/list'
    form_class = UserRegisterForm
    redirect_field_name = REDIRECT_FIELD_NAME
    template_name = "account/register.html"

    @method_decorator(sensitive_post_parameters('password1'))
    @method_decorator(sensitive_post_parameters('password2'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/post/list')

        # Sets a test cookie to make sure the user has cookies enabled
        request.session.set_test_cookie()

        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()

        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')

        user = authenticate(username=username, password=raw_password)
        auth_login(self.request, user)

        # If the test cookie worked, go ahead and
        # delete it since its no longer needed
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()

        return super(RegisterView, self).form_valid(form)

    def get_success_url(self):
        redirect_to = self.request.GET.get(self.redirect_field_name)
        if not is_safe_url(url=redirect_to, host=self.request.get_host()):
            redirect_to = self.success_url
        return redirect_to

def profile(request, account_slug):
    account = get_object_or_404(Account, slug=account_slug)

    # TODO: I don't remember if I can safely pass account as 
    # an parameter to the render.

    if account.avatar:
        account_image = account.avatar.preview
    else:
        account_image = None

    account_data = {
        'username' : account.username,
        'avatar_image' : account_image,
        'date_joined' : account.date_joined,
        'post_count' : account.get_posts().count()
    }

    return render(request, 'account/profile.html', { 'account_data' : account_data })
