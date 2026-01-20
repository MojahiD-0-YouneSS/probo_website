from probo.styles.frameworks.bs5.components import (
    BS5NavBar,
    BS5Button,
    BS5Collapse,
    BS5Nav,
    BS5Badge,
    BS5Table,
    BS5TableRow,
    BS5Card,
    BS5Modal,
)
from apps.core.models import CartItem
from probo import (
    ul,li,div,span,i,button,h6,
)

def cart_badge(session_key,is_hx_oob=False):
    hx_oob = {}
    if is_hx_oob:
        hx_oob.update({'hx-swap-oob':"true"})
    orders = CartItem.objects.filter(session_key=session_key,is_ordered=False)
    cart_section = div(button(
        i(
            Class="bi bi-basket",
        ),
        # span(0,Id="cart-count",Class="fab-badge"),
        BS5Badge(len(orders), variant='danger', Class='fab-badge ms-3 px-1 py-2'),
        Id="cart-fab", Class="fab-cart", data_bs_toggle='modal', data_bs_target='#cartModal', Type="button",**hx_oob)
    )
    return cart_section

def cart_item_row(item):
    cart_item = li(
        div(
            h6(
                item.menu_item.name,
                Class="my-0",
            ),
        ),
        span(
            f"{item.price} X {item.quantity}",
            Class="text-muted",
        ),
        i(
            Class="bi bi-trash text-danger", style="cursor:pointer",hx_get=f"{{% url 'core:remove_order_item' obj_id={item.id} %}}", hx_target=f'#item-{item.id}',hx_swap='outerHTML',
        ),
        Class="list-group-item d-flex justify-content-between lh-sm",Id=f'item-{item.id}',
    )
    return cart_item

def cart_total(session_key,is_hx_oob=False):
    hx_oob = {}
    if is_hx_oob:
        hx_oob.update({'hx-swap-oob': "true"})
    cart_total = sum([item.price*item.quantity for item in CartItem.objects.filter(session_key=session_key,is_ordered=False)])
    cart_total_string = div(
        span('Total:',),
        span(cart_total,), Id='CardTotal',
        Class="d-flex justify-content-between fw-bold fs-5",**hx_oob
    )
    return cart_total_string

def cart_item_list(session_key,is_hx_oob=False):
    hx_oob = {}
    if is_hx_oob:
        hx_oob.update({'hx-swap-oob': "true"})
    cart_items_obj = CartItem.objects.filter(session_key=session_key,is_ordered=False)

    cart_items = [cart_item_row(item) for item in cart_items_obj]
    cart_items_string = ul(*cart_items,Id="cart-items", Class="list-group mb-3",**hx_oob)
    return cart_items_string

def cart_modal(props,is_hx_oob=False):
    hx_oob = {}
    if is_hx_oob:
        hx_oob.update({'hx-swap-oob':"true"})


    cart_list = cart_item_list(props.get('session_key'))

    cart_details = div(cart_list,cart_total(props.get('session_key')))

    close_button = BS5Button('Close',variant='secondary',Type='button',data_bs_toggle="modal",data_bs_target='#cartModal',)
    place_order_button = BS5Button('Place Order',variant='success',Type='button',hx_get='{% url "core:place_order" %}', hx_target='#cart-items', hx_swap='innerHtml')

    modal_template = BS5Modal(render_constraints={"Viewer_role":'customer',},Class="fade", Id="cartModal", tabindex="-1",**hx_oob)
    modal_template.add_modal_header('',title='Your Order',Class='bg-warning text-white')
    modal_template.add_modal_body(cart_details,)
    modal_template.add_modal_footer(close_button.render()+place_order_button.render(),)
    modal_template.include_env_props(**props)
    return modal_template.render()