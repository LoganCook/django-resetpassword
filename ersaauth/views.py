from django.template.response import TemplateResponse
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import resolve_url
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from django.contrib.auth.forms import PasswordResetForm
from django.contrib.sites.shortcuts import get_current_site
from django.core.urlresolvers import reverse
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters

from datetime import timedelta
from django.core import signing
from django.conf import settings

from .forms import SetPasswordForm
from .activedirectory import ErsaAD

import logging
logger = logging.getLogger(settings.APP_LOGGER)

def default_token_generator(email):
    """Create self-contained varied length token. No backend is needed"""
    return signing.dumps(email, salt=settings.PASSWORD_RESET_TOKEN_SALT)


def check_token(token):
        """
        Check that a password reset token is correct for a given user.
        Token is valid until expires: can be used multiple times
        """

        #TODO: log token: once used, no more ?
        #       compare last time password reset timestamp < age of token, stop user abuses system

        # No distinguish on SignatureExpired, BadSignature
        try:
            values = signing.loads(token, salt=settings.PASSWORD_RESET_TOKEN_SALT, max_age=timedelta(hours=settings.PASSWORD_RESET_TIMEOUT))
        except:
            return False

        #Currently, only email
        return values

# Modified from Django.contrib.auth.views
# Create your views here.
# 4 views for password reset:
# - password_reset sends the mail
# - password_reset_link_sent shows a success message for the above
# - password_reset_confirm checks the link the user clicked and prompts for a new password
# - password_reset_complete shows a success message for the above

@csrf_protect
def password_reset(request, is_admin_site=False,
                   template_name='ersa_password_reset_form.html',
                   email_template_name='ersa_password_reset_email.html',
                   subject_template_name='password_reset_subject.txt',
                   password_reset_form=PasswordResetForm,
                   token_generator=default_token_generator,
                   post_reset_redirect=None,
                   from_email=None,
                   current_app=None,
                   extra_context=None,
                   html_email_template_name=None):

    if post_reset_redirect is None:
        post_reset_redirect = reverse('password_reset_link_sent')
    else:
        post_reset_redirect = resolve_url(post_reset_redirect)
    if request.method == "POST":
        #Use django.contrib.auth.forms.PasswordResetForm to collect email address
        #and send email
        form = password_reset_form(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]

            current_site = get_current_site(request)
            site_name = current_site.name
            domain = current_site.domain
            context = {
                'email': email,
                'domain': domain,
                'site_name': site_name,
                'uid': urlsafe_base64_encode(force_bytes('1')),
                'token': token_generator(email),
                'protocol': 'https' if request.is_secure() else 'http',
            }

            form.send_mail(subject_template_name, email_template_name,
                           context, from_email, email,
                           html_email_template_name=html_email_template_name)
            return HttpResponseRedirect(post_reset_redirect)
    else:
        form = password_reset_form()
    context = {
        'form': form,
        'title': 'Password reset',
    }
    if extra_context is not None:
        context.update(extra_context)

    if current_app is not None:
        request.current_app = current_app

    return TemplateResponse(request, template_name, context)

#Use template from Django's admin template
def password_reset_link_sent(request,
                        template_name='ersa_password_reset_link_sent.html',
                        current_app=None, extra_context=None):
    context = {
        'title': 'Password reset link sent',
    }
    if extra_context is not None:
        context.update(extra_context)

    if current_app is not None:
        request.current_app = current_app

    return TemplateResponse(request, template_name, context)


@sensitive_post_parameters()
@never_cache
def password_reset_confirm(request, token=None,
                           template_name='ersa_password_reset_confirm.html', current_app=None):
    logger.debug("Received token for restting password: %s " % token)
    email = check_token(token)

    if token is not None and email:
        set_password_form = SetPasswordForm
        ersa_ad = ErsaAD(settings.AD_SERVER, settings.AD_DOMAIN, settings.AD_RESETER, settings.AD_RESETER_PWD, settings.AD_BASE)
        users = ersa_ad.get_user_by_email(email)
        #~ for user in users:
            #~ print(user.entry_get_dn())

        if len(users) != 1:
            logger.info("Single user was expected but %d found with %s" % (len(users), email))

            if settings.DEBUG:
                logger.debug("Reset the password of the user's first account. Only allowed in debug mode")
            else:
                return HttpResponse('<p>Your password cannot be reset var portal.</p> Please contact <a href="https://www.ersa.edu.au/support/">helpdesk</a>.')

        user = users[0].entry_get_dn()

        validlink = True
        title = 'Enter new password'
        if request.method == 'POST':
            form = set_password_form(request.POST)
            if form.is_valid():
                password = form.cleaned_data['new_password1']
                logger.info("Trying to reset password for %s" % user)
                if ersa_ad.reset_password(user, password):
                    logger.info("Password reset was successful")
                    post_reset_redirect = reverse('password_reset_complete')
                    logger.debug("Before redirect to rest/done")
                    return HttpResponseRedirect(post_reset_redirect)
                else:
                    logger.error("Password reset failed")
                    return HttpResponse("Failed to reset your password.\nPlease contact Helpdesk")
        else:
            form = set_password_form()
    else:
        validlink = False
        form = None
        title = 'Password reset unsuccessful'

    context = {
        'form': form,
        'title': title,
        'validlink': validlink,
    }

    if current_app is not None:
        request.current_app = current_app

    return TemplateResponse(request, template_name, context)


def password_reset_complete(request,
                            template_name='ersa_password_reset_complete.html',
                            current_app=None):
    context = {
        'login_url': settings.FIM_URL,
        'title': 'Password reset complete',
    }

    if current_app is not None:
        request.current_app = current_app

    return TemplateResponse(request, template_name, context)
