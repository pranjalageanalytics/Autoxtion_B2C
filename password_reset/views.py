import datetime
from CRM.models import *
from CRM.forms import *
from Registration.forms import *
from Registration.views import *
from django.conf import settings
from Registration.forms import UpdateProfileForm, ChangePasswordForm
from django.template import RequestContext
from django.core import signing
from django.core.mail import send_mail
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect, render_to_response, HttpResponse
from django.template import loader
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.debug import sensitive_post_parameters
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, get_user_model, login as auth_login,
    logout as auth_logout, update_session_auth_hash,
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import (
    AuthenticationForm,PasswordResetForm, SetPasswordForm,
)
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect, QueryDict
from django.shortcuts import resolve_url
from django.template.response import TemplateResponse
#from django.urls import reverse
from django.utils.deprecation import RemovedInDjango20Warning
from django.utils.encoding import force_text
from django.utils.http import is_safe_url, urlsafe_base64_decode
from django.utils.six.moves.urllib.parse import urlparse, urlunparse
from django.utils.translation import ugettext as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from password_reset.forms import PasswordChangeForm
from django.contrib.auth.models import User, Group
from Registration.views import login
from django.contrib.auth import authenticate
from Registration.models import UserProfile
from django.contrib.auth import login as auth_login
from django.template import Context

try:
    from django.contrib.sites.shortcuts import get_current_site
except ImportError:
    from django.contrib.sites.models import get_current_site

from .forms import PasswordRecoveryForm, PasswordResetForm
from .signals import user_recovers_password
from .utils import get_user_model, get_username

from django.template.loader import render_to_string, get_template
from Timeline.models import *
import logging
logger = logging.getLogger('promotion')
logger.addHandler(logging.NullHandler())


class SaltMixin(object):
    salt = 'password_recovery'
    url_salt = 'password_recovery_url'


def loads_with_timestamp(value, salt):
    """Returns the unsigned value along with its timestamp, the time when it
    got dumped."""
    try:
        signing.loads(value, salt=salt, max_age=-999999)
    except signing.SignatureExpired as e:
        age = float(str(e).split('Signature age ')[1].split(' >')[0])
        timestamp = timezone.now()
        return timestamp, signing.loads(value, salt=salt)


class RecoverDone(SaltMixin, generic.TemplateView):
    logger.debug("start of recovery done view")
    template_name = 'password_reset/reset_sent.html'

    def get_context_data(self, **kwargs):
        ctx = super(RecoverDone, self).get_context_data(**kwargs)
        try:
            ctx['timestamp'], ctx['email'] = loads_with_timestamp(
                self.kwargs['signature'], salt=self.url_salt,
            )
        except signing.BadSignature:
            raise Http404
        return ctx
recover_done = RecoverDone.as_view()


class Recover(SaltMixin, generic.FormView):
    logger.debug("start of recover view")
    case_sensitive = True
    form_class = PasswordRecoveryForm
    template_name = 'password_reset/recovery_form.html'
    success_url_name = 'password_reset:password_reset_sent'
    email_template_name = 'password_reset/recovery_email.txt'
    email_subject_template_name = 'password_reset/recovery_email_subject.txt'
    search_fields = ['username', 'email']

    def get_success_url(self):
        return reverse(self.success_url_name, args=[self.mail_signature])

    def get_context_data(self, **kwargs):
        kwargs['url'] = self.request.get_full_path()
        return super(Recover, self).get_context_data(**kwargs)

    def get_form_kwargs(self):
        kwargs = super(Recover, self).get_form_kwargs()
        kwargs.update({
            'case_sensitive': self.case_sensitive,
            'search_fields': self.search_fields,
        })
        return kwargs

    def get_site(self):
        return get_current_site(self.request)

    def send_notification(self):
        context = {
            'site': self.get_site(),
            'user': self.user,
            'username': get_username(self.user),
            'token': signing.dumps(self.user.pk, salt=self.salt),
            'secure': self.request.is_secure(),
        }
        h=self.get_site()
        
        data = {}
        template = get_template('password_reset/password_recovery_email.html')
        html  = template.render(Context(data))
        
        subject='AutoXtion Password Recovery'
        html_content = render_to_string('password_reset/password_recovery_email.html', context)
        to=[self.user.email]
        from_email=settings.EMAIL_HOST_USER
        send_mail(subject,"",from_email,to,fail_silently=True, html_message=html_content)
                

    def form_valid(self, form):
        self.user = form.cleaned_data['user']
        self.send_notification()
        if (
            len(self.search_fields) == 1 and
            self.search_fields[0] == 'username'
        ):
            # if we only search by username, don't disclose the user email
            # since it may now be public information.
            email = self.user.username
        else:
            email = self.user.email
        self.mail_signature = signing.dumps(email, salt=self.url_salt)
        return super(Recover, self).form_valid(form)
recover = Recover.as_view()


class Reset(SaltMixin, generic.FormView):
    logger.debug("start of reset view")
    form_class = PasswordResetForm
    token_expires = None
    template_name = 'password_reset/reset.html'
    success_url = reverse_lazy('password_reset:password_reset_done')

    def get_token_expires(self):
        duration = getattr(settings, 'PASSWORD_RESET_TOKEN_EXPIRES',
                           self.token_expires)
        if duration is None:
            duration = 3600 * 48  # Two days
        return duration

    @method_decorator(sensitive_post_parameters('password1', 'password2'))
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs
        self.user = None

        try:
            pk = signing.loads(kwargs['token'],
                               max_age=self.get_token_expires(),
                               salt=self.salt)
        except signing.BadSignature:
            return self.invalid()

        self.user = get_object_or_404(get_user_model(), pk=pk)
        return super(Reset, self).dispatch(request, *args, **kwargs)

    def invalid(self):
        return self.render_to_response(self.get_context_data(invalid=True))

    def get_form_kwargs(self):
        kwargs = super(Reset, self).get_form_kwargs()
        kwargs['user'] = self.user
        return kwargs

    def get_context_data(self, **kwargs):
        ctx = super(Reset, self).get_context_data(**kwargs)
        if 'invalid' not in ctx:
            ctx.update({
                'username': get_username(self.user),
                'token': self.kwargs['token'],
            })
        return ctx

    def form_valid(self, form):
        form.save()
        user_recovers_password.send(
            sender=get_user_model(),
            user=form.user,
            request=self.request
        )
        return redirect(self.get_success_url())
reset = Reset.as_view()


class ResetDone(generic.TemplateView):
    logger.debug("start of reset done view")
    template_name = 'password_reset/recovery_done.html'

reset_done = ResetDone.as_view()

# @login_required(login_url="/registration/login/")
# def password_change(request,user_id):
    # logger.debug("start of password change view")
    # try:
        # server1 = get_object_or_404(User, pk=user_id)
        # group=Group.objects.get(user=server1)
        # if group.name=="Member":
            # logger.debug("user is member")
            # server2 = get_object_or_404(UserProfile, user=server1)
            # print("-------------server emg_no",server2.Emg_no)
            # update_profile = UpdateProfileForm(initial={'first_name':server1.first_name,'last_name':server1.last_name, 'phone_no':server2.phone_no,'area_code':server2.area_code,'Emg_no':server2.Emg_no, 'shop_name':server2.shop_name, 'shop_address':server2.shop_address, 'country':server2.country, 'city':server2.city, 'website':server2.website})
        # else:
            # logger.debug("user is customer")
           
            # lead_u=lead_user.objects.get(user=server1)
            # server2=Lead.objects.get(pk=lead_u.customer.pk)
            # update_profile = LeadForm(instance=server2)
        # if request.method == "POST":
            # logger.debug(" password change post method")
        
            # form = PasswordChangeForm(request.POST)
            # if form.is_valid():
                # logger.debug("password change form is valid")
                # user1 = authenticate(username =server1, password=form.cleaned_data['oldPassword'])
                # if user1 is not None:
                   # logger.debug("password change form is valid")
                   
                   # user1.password=form.cleaned_data['new_password']
                   # user1.set_password(user1.password)
                   # user1.save()
                   # auth_login(request, user1)
                   # print("in second if------------------------------------")
                   # if group.name == "Customer":
                       # var3=lead_user.objects.get(user=server1)
                       # var1 = Lead.objects.get(pk=var3.customer.pk)
                       # address= UserProfile.objects.get(user=var1.member)
                   
                   # if group.name == "Lead":
                       # var3=lead_user.objects.get(user=server1)
                       # var1 = Lead.objects.get(pk=var3.customer.pk)
                       # address= UserProfile.objects.get(user=var1.member)
                   
                   # if group.name=="Member":
                       # variables = RequestContext(request,
                                       # {'group':group, 'update_profile':update_profile, 'updatepassword':ChangePasswordForm,'context1': "Your Password has been updated"})
                       # return render_to_response('registration/updateDetails.html', variables)
                   # else:
                       # variables = RequestContext(request,
                                       # {'address':address,'group':group, 'update_profile':update_profile, 'updatepassword':ChangePasswordForm,'context1': "Your Password has been updated"})
                       # return render(request, 'registration/updateDetailsCustomer.html', variables)
                # else:
                   
                    # variables = RequestContext(request,
                                       # {'group': group,'update_profile':update_profile, 'updatepassword':ChangePasswordForm,'errorpassword': "Invalid Password"})
                    # if group.name=="Member":
                       # return render(request, 'registration/updateDetails.html', variables)
                    # else:
                       # return render(request, 'registration/updateDetailsCustomer.html', variables)
                    
                    
            # else:
                
                # variables = RequestContext(request,
                                       # {'group':group,'update_profile':update_profile, 'updatepassword':ChangePasswordForm,})
                # if group.name=="Member":
                       # return render(request, 'registration/updateDetails.html', variables)
                # else:
                       # return render(request, 'registration/updateDetailsCustomer.html', variables)
        # else:
                
                
                # variables = RequestContext(request,
                                       # {'group':group,'update_profile':update_profile, 'updatepassword':ChangePasswordForm})
                # if group.name=="Member":
                       # return render(request,'registration/updateDetails.html', variables)
                # else:
                       # return render(request, 'registration/updateDetailsCustomer.html', variables)
                   
    # except Exception as e:
        # print(e)
        # render(request,'password_reset/404.html')




@login_required(login_url="/registration/login/")
def password_change(request,user_id):
        logger.debug("start of password change view")
#     try:
        server1 = get_object_or_404(User, pk=user_id)
        group=Group.objects.get(user=server1)
        if group.name=="Member":
            logger.debug("user is member")
            server2 = get_object_or_404(UserProfile, user=server1)
            print("-------------server emg_no",server2.Emg_no)
            update_profile = UpdateProfileForm(initial={'first_name':server1.first_name,'last_name':server1.last_name, 'phone_no':server2.phone_no,'area_code':server2.area_code,'Emg_no':server2.Emg_no, 'shop_name':server2.shop_name, 'shop_address':server2.shop_address, 'country':server2.country, 'city':server2.city, 'website':server2.website})
        elif group.name=="Company":
              
            cust=CustCompany.objects.get(email=server1.email)
            val=getProfileCompletedCount(cust.pk,group.name)
            print("$$$$$$$$1",cust)
            company=CustForm(instance=cust)
            userimage1 = company_imageForm()
            #print("!!@@@@@@@@@@",userimage1)
            timeline_li=Timeline.objects.filter(user=request.user).order_by('-id')[:5]
            userimage1 = company_imageForm(request.FILES)
            #return render(request,'registration/company_profile.html',{'val':val,'group':group,'company':company,'userimage1':userimage1,'updatepassword':ChangePasswordForm,'timeline_li':timeline_li,'context2': "Please enter all valid details"})  

        else:
            logger.debug("user is customer")
           
            lead_u=lead_user.objects.get(user=server1)
            server2=Lead.objects.get(pk=lead_u.customer.pk)
            update_profile = LeadForm(instance=server2)
        if request.method == "POST":
            logger.debug(" password change post method")
        
            form = PasswordChangeForm(request.POST)
            if form.is_valid():
                logger.debug("password change form is valid")
                user1 = authenticate(username =server1, password=form.cleaned_data['oldPassword'])
                if user1 is not None:
                   logger.debug("password change form is valid")
                   
                   user1.password=form.cleaned_data['new_password']
                   user1.set_password(user1.password)
                   user1.save()
                   auth_login(request, user1)
                   print("in second if------------------------------------")
                   if group.name == "Customer":
                       var3=lead_user.objects.get(user=server1)
                       var1 = Lead.objects.get(pk=var3.customer.pk)
                       address= UserProfile.objects.get(user=var1.member)
                   
                   if group.name == "Lead": 
                       var3=lead_user.objects.get(user=server1)
                       var1 = Lead.objects.get(pk=var3.customer.pk)
                       address= UserProfile.objects.get(user=var1.member)
                   
                   if group.name=="Member":
                       timeline_li=Timeline.objects.filter(user=request.user).order_by('-id')[:5]
                       image1=UserProfile.objects.get(user_id=request.user)
                       print("password updated")
                       variables = RequestContext(request,
                                       {'timeline_li':timeline_li,'image1':image1,'group':group, 'update_profile':update_profile, 'updatepassword':ChangePasswordForm,'context1': "Your Password has been updated"})
                       return render_to_response('registration/member_profile.html', variables)
                   elif group.name=="Company":
                          
                        cust=CustCompany.objects.get(email=server1)
                        val=getProfileCompletedCount(cust.pk,group.name)
                        print("$$$$$$$$2",cust)
                        company=CustForm(instance=cust)
                        userimage1 = company_imageForm()
                        #print("!!@@@@@@@@@@",userimage1)
                        timeline_li=Timeline.objects.filter(user=request.user).order_by('-id')[:5]
                        userimage1 = company_imageForm(request.FILES)
                        return render(request,'registration/company_profile.html',{'val':val,'group':group,'company':company,'image2':cust,'userimage1':userimage1,'updatepassword':ChangePasswordForm,'timeline_li':timeline_li,'context1': "Your Password has been updated"})  

                   else:
                       timeline_li=Timeline.objects.filter(user=request.user).order_by('-id')[:5]
                       image2=Lead.objects.get(pk=lead_u.customer.pk)
                       variables = RequestContext(request,
                                       {'group':group,'timeline_li':timeline_li,'image2':image2,'address':address,'group':group, 'update_profile':update_profile, 'updatepassword':ChangePasswordForm,'context1': "Your Password has been updated"})
                       return render(request, 'registration/customer_profile.html', variables)
                else:
                   
                    
                    if group.name=="Member":
                       timeline_li=Timeline.objects.filter(user=request.user).order_by('-id')[:5]
                       image1=UserProfile.objects.get(user_id=request.user)
                       variables = RequestContext(request,
                                       {'timeline_li':timeline_li,'image1':image1,'group': group,'update_profile':update_profile, 'updatepassword':ChangePasswordForm,'errorpassword': "Invalid Password"})
                       return render(request, 'registration/member_profile.html', variables)

                    elif group.name=="Company":
                          
                        cust=CustCompany.objects.get(email=server1)
                        val=getProfileCompletedCount(cust.pk,group.name)
                        print("$$$$$$$$3",cust)
                        company=CustForm(instance=cust)
                        userimage1 = company_imageForm()
                        #print("!!@@@@@@@@@@",userimage1)
                        timeline_li=Timeline.objects.filter(user=request.user).order_by('-id')[:5]
                        userimage1 = company_imageForm(request.FILES)
                        return render(request,'registration/company_profile.html',{'val':val,'group':group,'company':company,'image2':cust,'userimage1':userimage1,'updatepassword':ChangePasswordForm,'timeline_li':timeline_li,'context2': "Please enter all valid details"})  

                    else:
                       timeline_li=Timeline.objects.filter(user=request.user).order_by('-id')[:5]
                       image2=Lead.objects.get(pk=lead_u.customer.pk)
                       variables = RequestContext(request,
                                       {'group':group,'image2':image2,'timeline_li':timeline_li,'group': group,'update_profile':update_profile, 'updatepassword':ChangePasswordForm,'errorpassword': "Invalid Password"})
                       return render(request, 'registration/customer_profile.html', variables)
                    
                    
            else:
                if group.name=="Member":
                       timeline_li=Timeline.objects.filter(user=request.user).order_by('-id')[:5]
                       image1=UserProfile.objects.get(user_id=request.user)
                       variables = RequestContext(request,
                                       {'timeline_li':timeline_li,'image1':image1,'group':group,'update_profile':update_profile, 'updatepassword':ChangePasswordForm,})
                       return render(request, 'registration/member_profile.html', variables)
		elif group.name=="Company":
                      
                    cust=CustCompany.objects.get(email=server1)
                    val=getProfileCompletedCount(cust.pk,group.name)
                    print("$$$$$$$$4",cust)
                    company=CustForm(instance=cust)
                    userimage1 = company_imageForm()
                    #print("!!@@@@@@@@@@",userimage1)
                    timeline_li=Timeline.objects.filter(user=request.user).order_by('-id')[:5]
                    userimage1 = company_imageForm(request.FILES)
                    return render(request,'registration/company_profile.html',{'val':val,'group':group,'company':company,'image2':cust,'userimage1':userimage1,'updatepassword':ChangePasswordForm,'timeline_li':timeline_li,'context2': "Please enter all valid details"})  
           
                else:
                       timeline_li=Timeline.objects.filter(user=request.user).order_by('-id')[:5]
                       image2=Lead.objects.get(pk=lead_u.customer.pk)
                       variables = RequestContext(request,
                                       {'image2':image2,'timeline_li':timeline_li,'group':group,'update_profile':update_profile, 'updatepassword':ChangePasswordForm,})
                       return render(request, 'registration/customer_profile.html', variables)
        else:
                if group.name=="Member":
                       timeline_li=Timeline.objects.filter(user=request.user).order_by('-id')[:5]
                       image1=UserProfile.objects.get(user_id=request.user)
                       variables = RequestContext(request,
                                       {'timeline_li':timeline_li,'image1':image1,'group':group,'update_profile':update_profile, 'updatepassword':ChangePasswordForm})
                       return render(request,'registration/member_profile.html', variables)
		elif group.name=="Company":
                      
                    cust=CustCompany.objects.get(email=server1)
                    val=getProfileCompletedCount(cust.pk,group.name)
                    print("$$$$$$$$5",cust)
                    company=CustForm(instance=cust)
                    userimage1 = company_imageForm()
                    #print("!!@@@@@@@@@@",userimage1)
                    timeline_li=Timeline.objects.filter(user=request.user).order_by('-id')[:5]
                    userimage1 = company_imageForm(request.FILES)
                    return render(request,'registration/company_profile.html',{'val':val,'group':group,'company':company,'image2':cust,'userimage1':userimage1,'updatepassword':ChangePasswordForm,'timeline_li':timeline_li,'context2': "Please enter all valid details"})  

                else:
                       timeline_li=Timeline.objects.filter(user=request.user).order_by('-id')[:5]
                       image2=Lead.objects.get(pk=lead_u.customer.pk)
                       variables = RequestContext(request,
                                       {'image2':image2,'timeline_li':timeline_li,'group':group,'update_profile':update_profile, 'updatepassword':ChangePasswordForm})
                       return render(request, 'registration/customer_profile.html',variables)