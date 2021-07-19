from django.utils import translation
from django.shortcuts import redirect, render, get_object_or_404
from django.conf import settings
from django.shortcuts import HttpResponse
from .forms import UserForm
from .models import User, Profile
from django.views.generic import CreateView, FormView
from django.contrib import messages
from food_bundle_app.send_sms import send_sms

from django.utils.html import strip_tags
from django.template.loader import render_to_string

from django.core import mail
from django.core.mail import EmailMultiAlternatives

from food_bundle_app.models import CustomOrder, Product, Bundle, PriceVariation
from food_bundle_app.forms import CustomOrderForm

def index(request):
    template_name = "public/index.html"
    form = UserForm
    bundles = Bundle.objects.filter(status=1).exclude(title = "UMUFUNGO W'UMUHINZI")
    umufungo = Bundle.objects.filter(status=1).filter(title="UMUFUNGO W'UMUHINZI")    

    if request.method == "POST":
        form = UserForm(request.POST)
        
    context = {
        'form': form,
        'bundles':bundles,
        'umufungo':umufungo,

        'title': "Welcome || Food Bundle"
    }
    return render(request, template_name=template_name, context=context)

def contact(request):
    template_name = "public/contact.html"
        
    context = {
        'title': "Our Contact || Food Bundle"
    }
    return render(request, template_name=template_name, context=context)

class Register(FormView):
    template_name = "public/register.html"
    form_class = UserForm
    model = User
    success_url = 'get-a-quote/sent'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Register || Food Bundle"
        return context

    def form_valid(self, form):
        user = User()
        profile = Profile()

        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.gender = form.cleaned_data['gender']
        user.category = form.cleaned_data['category']
        
        profile.phone = form.cleaned_data['phone']
        profile.district = form.cleaned_data['district']
        profile.sector = form.cleaned_data['sector']
        profile.cell = form.cleaned_data['cell']
        profile.tin = form.cleaned_data['tin']
        profile.nid = form.cleaned_data['nid']
        
        user.email = str(profile.phone)+"@food-user.site"
        try:
        
            created_user = user.save()
            
            profile.user = user
            
            profile.save()
            
            messages.success(self.request, 'Your registration successfully')

            form.send_email()
            
            context = {
                'title' : 'Welcome || Food Bundle',
                'user': user
            }
            
            subject = "Email Confirmartion | Food Bundle"
            html_message = render_to_string('admin/authentication/confirm.html', context)

            text_content = strip_tags(html_message)
            email = "claudemani01@gmail.com"
            msg = EmailMultiAlternatives(subject, text_content, "norepley@food.rw", [email])
            msg.attach_alternative(html_message, "text/html")
            msg.send()
            
        except Exception as identifier:
            messages.danger(self.request, 'Registration failed please try again')
            return redirect("/register/")
        
        context = {
                'title' : 'Welcome || Food Bundle',
            }
        
        # return render(self.request, "public/index.html", context)
        return redirect("index")
        return super().form_valid(form)
    

def confirmEmail(request, user):
    user = get_object_or_404(User, id=user)
    user.status = 'approved'
    
    try:
        user.save()
        messages.error(request, 'Account confirmed')
        return redirect("/admin/")
    except:
        messages.error(request, 'Account not confirmed')
        return HttpResponse("/register/")
        
class CustomOrderCreateView(CreateView):
    model = CustomOrder
    template_name = "public/order.html"
    form_class = CustomOrderForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        items = Product.objects.all()
        context['title'] = "Make order || Food Bundle"
        context['items'] = items
        return context
    
    def form_valid(self, form):
        order = CustomOrder()
        messages.success(self.request, 'Order sent successfully')
        form.save()
        return redirect("index")