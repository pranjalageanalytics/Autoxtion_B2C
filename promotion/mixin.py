from django.contrib.auth.views import redirect_to_login
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


class AuthRequiredMixin(object):
    #login_url = "/registration/login/"
    
    @method_decorator(login_required(login_url="/registration/login/"))
    def dispatch(self, *args, **kwargs):
        return super(AuthRequiredMixin, self).dispatch(*args, **kwargs)