from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from apps.core.components import (
    nav_bar,
    HomePage,
    footer_section,
    menu_section,
    reservation_section,
    menu_item_form,
    cart_badge,
    cart_modal,
    cart_total,
    admin_form,
    admin_row,
    staff_row,
get_messages_html,
)
from apps.core.probo_tcm import render_probo
from probo.request import RequestDataTransformer,ComponentRequestContext
from django.middleware.csrf import get_token
from django.http import HttpResponse
from apps.core.forms import (
    MenuItemForm,
    QuantityForm,
)
from apps.core.models import (
    MenuItem,CartItem,Order,Table
)
from probo import li
# Create your views here.
def home(request,*args,**kwargs):
    view_role = request.GET.get('Viewer_role','customer',)

    if not request.session.get('Viewer_role',None) and view_role:
        request.session['Viewer_role']=view_role
    elif request.session.get('Viewer_role',None) and view_role:
        request.session['Viewer_role']=view_role
    else:
        view_role=request.session.get('Viewer_role')
    props = {
        'Viewer_role':view_role,
        'crf_token':get_token(request),
        'session_key':request.session.session_key,
    }

    if request.headers.get("HX-Request") == "true" and view_role=='customer':
        return HttpResponse(render_probo(request,HomePage(props),footer_section(props)))
    elif request.headers.get("HX-Request") == "true":
        return HttpResponse(render_probo(request,HomePage(props),))
    else:
        # return render_probo(request,'base.html',block_body=nav_bar(props))
        return render(request,'base.html',{
            'block_nav':render_probo(request,nav_bar(props)),
            'block_home':render_probo(request,HomePage(props)),
            'block_footer':render_probo(request,footer_section(props)),
        })

def menu(request,*args,**kwargs):

    props = {
        'Viewer_role': request.session['Viewer_role'],
        'crf_token': get_token(request),
        'session_key': request.session.session_key,
    }
    if request.headers.get("HX-Request") == "true":
        if menu_section(props):
            return HttpResponse(render_probo(request,menu_section(props),footer_section(props)))
        else:
            return HttpResponse(render_probo(request,HomePage(props)))
    else:

        return redirect('core:home')

def reservation(request,*args,**kwargs):
    props = {
        'Viewer_role': request.session['Viewer_role'],
        'crf_token': get_token(request),
        'session_key': request.session.session_key,
    }
    request_data = RequestDataTransformer(request)
    if request.headers.get("HX-Request") == "true":
        if reservation_section(request_data,props):
            return HttpResponse(render_probo(request,reservation_section(request_data,props),footer_section(props)))
        else:
            return HttpResponse(render_probo(request,HomePage(props)))
    else:
        return redirect('core:home')

def add_menu_item(request,*args,**kwargs):
    item_row = str()
    form = MenuItemForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            item = form.save()
            item_row=admin_row(item,is_hx_oob=True)
            messages.success(request, "menu item is saved successfully!")
        else:
            messages.success(request, "menu item was not saved!!")
    request.session['Viewer_role'] = 'admin'
    if request.headers.get("HX-Request") == "true":
        return HttpResponse(render_probo(request,item_row,get_messages_html()))
    else:
        return redirect('core:home')

def remove_menu_item(request,*args,**kwargs):
    obj_id = kwargs.get('obj_id')
    obj = MenuItem.objects.get(id=obj_id)
    obj.delete()
    request.session['Viewer_role'] = 'admin'
    messages.success(request, "item was removed successfully!")
    if request.headers.get("HX-Request") == "true":
        return HttpResponse(render_probo(request,get_messages_html()))
    else:
        return redirect('core:home')

def add_order_item(request,*args,**kwargs):
    props = {
        'Viewer_role': request.session.get('Viewer_role'),
        'session_key':request.session.session_key,
     }
    form = QuantityForm(request.POST,)
    if request.method == 'POST':
        if form.is_valid():
            quantity=form.cleaned_data['quantity']
            obj_id=form.cleaned_data['obj_id']
            menu_item_obj = get_object_or_404(MenuItem,id=obj_id)
            cart_item, created = CartItem.objects.get_or_create(
                menu_item=menu_item_obj,
                price=menu_item_obj.price,
                session_key=request.session.session_key,
                is_ordered = False,
            )

            # 3. If it wasn't created (it existed), update the quantity
            if not created:
                cart_item.quantity += quantity
            else:
                cart_item.quantity = quantity

            cart_item.save()
            messages.success(request, f"{cart_item} is saved successfully!")
        else:
            messages.error(request, "item is not saved!!")
    if request.headers.get("HX-Request") == "true":
        return HttpResponse(render_probo(
        request,
        menu_item_form(cart_item.menu_item.id,get_token(request),is_hx_oob=True,),
        cart_badge(request.session.session_key,is_hx_oob=True),
        cart_modal(props,is_hx_oob=True),get_messages_html()
    ))
    else:
        return redirect('core:home')

def remove_order_item(request,*args,**kwargs):
    obj_id = kwargs.get('obj_id')
    item_obj = get_object_or_404(CartItem, id=obj_id)
    item_obj.delete()
    messages.success(request, "item deleted successfully!")
    if request.headers.get("HX-Request") == "true":
        return HttpResponse(render_probo(request,cart_badge(request.session.session_key,is_hx_oob=True), cart_total(request.session.session_key,is_hx_oob=True),get_messages_html()))
    else:
        return redirect('core:home')

def book_table(request,*args,**kwargs):
    if request.method == 'POST':
        booker_name = request.POST.get('full_name')
        booked_date = request.POST.get('booked_date')
        booked_time = request.POST.get('booked_time')
        number_of_guests = request.POST.get('number_of_guests')
        Table.objects.create(
            session_key=request.session.session_key,
            booker_name=booker_name,
            booked_date =booked_date,
            booked_time =booked_time,
            number_of_guests =int(number_of_guests.replace('+','').replace(' People','')),
        )
        messages.success(request, "Your table is booked successfully!")
    return redirect('core:reservation')

def place_order(request,*args,**kwargs):
    session_key = request.session.session_key
    props = {
        'Viewer_role': request.session.get('Viewer_role'),
        'session_key': session_key,
    }
    order = Order.objects.create(session_key=session_key,)
    order_items = CartItem.objects.filter(session_key=session_key,is_ordered=False)
    total = sum([item.price*item.quantity for item in order_items])
    for item in order_items:
        item.is_ordered = True
        item.order=order
        item.save()
    order.total_price=total
    order.save()
    messages.success(request, "Your order is created successfully!")
    if request.headers.get("HX-Request") == "true":
        return HttpResponse(render_probo(request,cart_modal(props,),get_messages_html(),cart_badge(request.session.session_key,is_hx_oob=True),cart_total(request.session.session_key,is_hx_oob=True)))
    else:
        return redirect('core:home')

def process_order(request,*args,**kwargs):
    order_id = kwargs.get('obj_id')
    order = get_object_or_404(Order,id=order_id)
    next_status = request.GET.get('next_status')
    if next_status == 'Remove':
        order.cleared=True
        order.save()
        return HttpResponse(render_probo(request,))
    order.status=next_status
    order.save()
    messages.success(request, "Your changes were saved successfully!")
    if request.headers.get("HX-Request") == "true":
        return HttpResponse(render_probo(request,staff_row(order),get_messages_html()))
    else:
        return redirect('core:home')