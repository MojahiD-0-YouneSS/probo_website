from probo.styles.frameworks.bs5.components import (
    BS5NavBar,
    BS5Button,
    BS5Collapse,
    BS5Nav,
    BS5Badge,
    BS5Table,
    BS5TableRow,
    BS5Card,
)
from apps.core.models import MenuCategory, MenuItem,Order,CartItem
from collections import OrderedDict
from probo import (
    section,div,span,a,ul,li,script,i,h1,p,h3,h2,button,br,small
)
from .cart import cart_badge
from probo.htmx import HTMXElement
from probo.components import Component, ComponentState
from apps.core.components.cart import cart_modal
from apps.core.components.menu_item_modal import admin_menu_item_modal

def admin_row(item,is_hx_oob=False):
    hx_oob = {}
    if is_hx_oob:
        hx_oob.update({'hx-swap-oob':"true"})
    row = BS5TableRow(Id=f'menu_item-{item.id}',Class='admin-row',*hx_oob)
    row.add_table_cel(item.name)
    row.add_table_cel(BS5Badge(item.category, variant='info', Class='text-dark'))
    row.add_table_cel(item.price)
    row.add_table_cel(BS5Button('delete', variant='danger', hx_get=f"{{% url 'core:remove_menu_item' obj_id={item.id} %}}",
                                hx_target=f'#menu_item-{item.id}', hx_swap='outerHTML').sm)
    return row
'''
<tr>
    <td>#${order.id.toString().slice(-4)} <br> <small class="text-muted">${order.time}</small></td>
    <td>${itemNames}</td>
    <td>$${order.total.toFixed(2)}</td>
    <td><span class="badge ${badgeClass} status-badge">${order.status}</span></td>
    <td>
        ${order.status === 'Pending' ? `<button class="btn btn-sm btn-warning" onclick="updateStatus(${order.id}, 'Cooking')">Cook</button>` : ''}
        ${order.status === 'Cooking' ? `<button class="btn btn-sm btn-success" onclick="updateStatus(${order.id}, 'Ready')">Ready</button>` : ''}
        ${order.status === 'Ready' ? `<button class="btn btn-sm btn-dark" onclick="updateStatus(${order.id}, 'Delivered')">Deliver</button>` : ''}
        ${order.status === 'Delivered' ? `<button class="btn btn-sm btn-outline-danger" onclick="deleteOrder(${order.id})">Clear</button>` : ''}
    </td>
</tr>
'''
def staff_row(order,is_hx_oob=False):
    hx_oob = {}

    BUTTON_STATES = OrderedDict([
        ('Pending', ['cook', 'warning']),
        ('Cooking', ['ready', 'success']),
        ('Ready', ['deliver', 'dark']),
        ('Delivered', ['clear record', 'outline-danger']),
        ('Remove', ['', 'danger']),
    ])
    keys = list(BUTTON_STATES.keys())

    nex_state = 0
    for x,y in enumerate(keys):
        if y==order.status:
            if len(keys)==x:
                nex_state = x
            else:
                nex_state = x+1
    item_names = [f'{item.menu_item.name} X {item.quantity}' for item in CartItem.objects.filter(order=order)]
    # t = [ordr.menu_item.name for ordr in Order.objects.filter(session_key=order.session_key)]
    if is_hx_oob:
        hx_oob.update({'hx-swap-oob':"true"})
    row = BS5TableRow(Id=f'order-{order.id}',Class='admin-row',*hx_oob)
    row.add_table_cel(f'{order.id}{br()}{small(order.created_at,Class="text-muted")}')
    row.add_table_cel(' '.join(set(item_names)))
    row.add_table_cel(order.total_price)
    row.add_table_cel(BS5Badge(order.status, variant='info', Class='text-dark'))
    btn_state = BUTTON_STATES[order.status]
    row.add_table_cel(BS5Button(btn_state[0], variant=btn_state[1], hx_get=f"{{% url 'core:process_order' obj_id={order.id} %}}",
                                hx_target=f'#order-{order.id}', hx_swap='outerHTML',hx_vals=f"js:{{next_status:'{keys[nex_state]}'}}").sm)
    return row

class HomePage:
    def __init__(self,props):
        self.props = props
        self.role = props.get('Viewer_role',None)
        self.session_key = props.get('session_key',None)

    def home_page(self,):
        customer_state = ComponentState(Viewer_role='customer')

        # ===================================================== Customer View
        hero_header = h1(
            'Authentic & Organic',
            Class='display-3 fw-bold',
        )
        hero_paragraph = p(
            'Farm-to-table dining experience in the heart of the city.',
            Class='lead mb-4',
        )

        cart_section = cart_badge(self.session_key)

        hero_button_warning = BS5Button(
            'View Menu',
            variant='warning',
            Class='text-dark',
            Type='button',
            hx_get="menu/",
            hx_target = "#app",
            hx_swap = "innerHTML",
            hx_push_url = "true",
        ).lg

        hero_button_light = BS5Button(
            'Book Table',
            variant='outline-light',
            Class='ms-2',
            Type='button',
            hx_get="reservation/",
            hx_target="#app",
            hx_swap="innerHTML",
            hx_push_url="true",
        ).lg

        card_texts = {
            'bi-geo-alt':[
                'Local Sourcing',
                'We partner with over 20 local farms to bring you the freshest ingredients daily.',
            ],
            'bi-star':[
                'Michelin Rated',
                'Award-winning chefs preparing classic dishes with a modern twist.',
            ],
            'bi-cup-hot':[
                'Cozy Ambience',
                'A perfect spot for romantic dates, family dinners, or business meetings.',
            ],
        }
        columns = [
            div(
                div(
                    i(Class=f'bi {k} fs-1 text-warning'),
                    h3(v[0],Class='mt-3'),
                    p(v[1],Class='text-muted'),
                    Class='p-4 border rounded shadow-sm h-100',
                ),
                Class='col-md-4'
            )
            for k,v in card_texts.items()
        ]

        infographs = div(
            div(
                ''.join(columns),
                Class='row g-4'
            ),
            Class='container py-5 text-center'
        )

        hero_section = section(
            div(
                div(
                    hero_header,
                    hero_paragraph,
                    hero_button_warning,
                    hero_button_light,
                    cart_section,

                    Class='container',

                ),
                Class='hero-section',
            ), infographs,
            Class='page-section active',
            Id='home',
        )+cart_modal(self.props)

        # ===================================================== Admin View

        customer_component=Component(name='home-customer',template=hero_section,state=customer_state,props=self.props)
        return customer_component.render()

    def home_staff_page(self,):
        staff_state = ComponentState(Viewer_role='staff')

        # ===================================================== Staff View

        orders = Order.objects.filter(session_key=self.session_key,status__in=['Pending','Cooking','Ready','Delivered',],cleared=False)
        # orders.delete()
        order_table_header_row = BS5TableRow()
        order_table_header_row.add_table_head('Order #')
        order_table_header_row.add_table_head('Items')
        order_table_header_row.add_table_head('Total')
        order_table_header_row.add_table_head('Status')
        order_table_header_row.add_table_head('Actions')

        order_table = BS5Table(variant='hover', Class='border')
        order_table.add_table_head(order_table_header_row, Class="table-dark", )
        order_table_body_row = BS5TableRow()

        if orders:
            order_table_body_row = [staff_row(order) for order in orders]
            order_table.add_table_body(*order_table_body_row, Id="staff-orders-body")
        else:
            order_table_body_row.add_table_cel('No active orders', colspan="5", Class="text-center")

            order_table.add_table_body(order_table_body_row, Id="staff-orders-body")
        staff_section = section(
              div(order_table, Class="table-responsive"),
            Id="staff",
            Class="page-section container py-4"
        )
        staff_component=Component(name='home-staff',template=staff_section,state=staff_state,props=self.props)

        return staff_component.render()

    def home_admin_page(self,):
        admin_state = ComponentState(Viewer_role='admin')
        menu_items = MenuItem.objects.filter(is_available=True)

        order_table_header_row = BS5TableRow()
        order_table_header_row.add_table_head('Item Name')
        order_table_header_row.add_table_head('Category')
        order_table_header_row.add_table_head('Price')
        order_table_header_row.add_table_head('Action')

        admin_table = BS5Table(variant='striped', Class='mb-0')

        admin_table.add_table_head(order_table_header_row, )

        if menu_items:
            admin_table_rows = [admin_row(item) for item in menu_items]

            admin_table.add_table_body(*admin_table_rows, Id="admin-menu-list")
        else:

            admin_table.add_table_body(
                BS5TableRow().add_table_cel('No active menu items', colspan="5", Class="text-center"),
                Id="admin-menu-list",
            )

        menu_managment_section = div(
            h2(
                i(Class="bi bi-gear"),
                'Menu Management',
            ),
            BS5Button(
                i(
                    Class="bi bi-plus-lg",
                ) +
                'Add New Item',
                variant='success',data_bs_toggle='modal',data_bs_target='#addItemModal',
            ).sm,
            Class='d-flex justify-content-between align-items-center mb-4',
            data_bs_toggle="modal",
            data_bs_target="#addItemModal",
        )
        admin_card = BS5Card(card_body=admin_table,Class='shadow-sm')
        admin_section = section(
            menu_managment_section,
            admin_card,
            Id="admin",
            Class="page-section container py-4"
        )+admin_menu_item_modal(self.props)
        admin_component=Component(name='home-admin',template=admin_section,state=admin_state,props=self.props)

        return admin_component.render()

    def render(self,):
        if self.role == 'admin':
            return self.home_admin_page()
        elif self.role == 'staff':
            return self.home_staff_page()
        else:
            return self.home_page()