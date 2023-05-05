from django.shortcuts import render, redirect
from django.views import View
from django.core.mail import send_mail
from .models import MenuItem, Category, OrderModel
from django.contrib.auth.decorators import login_required

 
class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/index.html')

class About(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/about.html')

class Order(View):
    def get(self, request, *args, **kwargs):
        # get every item from each category
        pizza = MenuItem.objects.filter(category__name__contains='Pizza')
        desserts = MenuItem.objects.filter(category__name__contains='Dessert')
        drinks = MenuItem.objects.filter(category__name__contains='Drink')

        # pass into context
        context = {
            'pizza': pizza,
            'desserts': desserts,
            'drinks': drinks,
        }

        # render the template
        return render(request, 'customer/order.html', context)

    def post(self, request, *args, **kwargs):#creating dictionary
        name = request.POST.get('name')
        email = request.POST.get('email')
        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code= request.POST.get('zip')
        
      
         
        
        order_items = {
            'items': []# this is a list
        }

        items = request.POST.getlist('items[]')

        for item in items:
            menu_item = MenuItem.objects.get(pk__contains=int(item))
            item_data = {
                'id': menu_item.pk,
                'name': menu_item.name,
                'price': menu_item.price
            }

            order_items['items'].append(item_data)

            price = 0
            item_ids = []

        for item in order_items['items']:
            price += item['price']
            item_ids.append(item['id'])
        #creates order
        order = OrderModel.objects.create(
            price=price,
            name=name,
            email=email,
            street=street,
            city=city,
            state=state,
            zip_code=zip_code
        )
        order.items.add(*item_ids)
#after user submits order send a confirmation email
        body = ('Thank you for your order, we will prepare your food\n'

             f'Your total :{price}\n'
             'Our delivery guy will knock on your door soon!')
        send_mail(
            'Thanks for your order!',
            body,
            'example@ivytech.edu',
            [email],
            fail_silently=False    
        )
        context = {
            'items': order_items['items'],
            'price': price
        }

        return redirect('order-confirmation', pk=order.pk)
    
class OrderConformation(View):
    def get(self, request, pk, *args, **kwargs):
        order =  OrderModel.objects.get(pk=pk)
        
        context = {
        'pk': order.pk,
        'items': order.items,
        'price': order.price,
        }
        
        return render(request, 'customer/order_confirmation.html', context)
    def post(self, request, pk, *args, **kwargs):
        print(request.body)
        
class OrderPayConfirmation(View):
    def get(self, request, *args, **kwargs):
        return render(request,'customer/order_pay_confirmation.html')


