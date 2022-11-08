import stripe
from django.views.generic import TemplateView
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.models import Permission

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY


class OrdersPageView(TemplateView):
    template_name = 'orders/purchase.html'

    # переопределяем метод что бы достать данные
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stripe_key'] = settings.STRIPE_TEST_PUBLISHABLE_KEY
        return context


# платеж в stripe
def charge(request):
    # get the permission
    permission = Permission.objects.get(codename='special_status')

    # get user
    user = request.user

    # give a permission
    user.user_permissions.add(permission)

    if request.method == 'POST':
        charge = stripe.Charge.create(
            amount=3900,
            currency='usd',
            description='Purchase all books',
            source=request.POST['stripeToken']
        )
        return render(request, 'orders/charge.html')
