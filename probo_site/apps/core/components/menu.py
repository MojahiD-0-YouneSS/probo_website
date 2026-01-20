from probo.styles.frameworks.bs5.components import BS5Button
from probo.components import (
    Component,ComponentState,
)
from .cart import cart_modal,cart_badge
from probo import (
    section,div,h2,p,h3,h5,span,form,Input,
)
from django.utils.text import slugify
from apps.core.models import MenuCategory, MenuItem
from apps.core.forms import QuantityForm


def menu_item_form(item_id,crf_token,is_hx_oob=False):
    hx_oob = {}
    if is_hx_oob:
        hx_oob.update({'hx-swap-oob': "true"})
    form_string = form(
                    Input(
                        Type="hidden", name="csrfmiddlewaretoken", value=crf_token,
                    ),
                    div(
                    div(
                        str(QuantityForm(initial={'obj_id':item_id})),
                        Class='col-md-4 mb-3',
                    ),div(
                        BS5Button('order',variant='outline-warning',Type='submit',Class='w-100').lg,
                        Class='col-md-8 mb-3',
                    ),Class='row',),Id=f'form-{item_id}',hx_post="{% url 'core:add_order_item' %}",**hx_oob
    )
    return  form_string

def menu_item(item,crf_token):
    menu_item_string = div(
                div(
                    div(
                        div(
                            h5(
                                item.name,
                                Class="card-title mb-0",
                            ),
                            span(
                                item.price,
                                Class="price-tag"
                            ),
                            Class="d-flex justify-content-between align-items-center mb-2"
                        ),
                        p(
                            item.description,
                            Class="card-text text-muted small",
                        ),div(menu_item_form(item.id,crf_token), Class='row gx-3', ),
                        Class="card-body"
                    ),
                    Class="card h-100 border-0 shadow-sm",
                ),
                Class="col-md-6 mb-3",

            )
    return menu_item_string

def menu_section(props):
    menu_state = ComponentState(Viewer_role='customer')
    crf_token=props.get('crf_token',None)
    content_category=MenuCategory.objects.all()
    menu_items = {category:MenuItem.objects.filter(category=category) for category in content_category}

    content = [
        div(
            div(
                h3(
                    category.name,
                    Class="text-warning"
                ),
              Class='col-12 border-bottom mb-3',
            ),
            ''.join(
            [menu_item(item,crf_token) for item in items]
            ),
            Class='row mb-4',
        )
        for category , items in menu_items.items()
    ]
    menu_content = div(
       ''.join(content),
        Id="menu-content",
    )

    order_menu = div()

    menu = section(
        div(
            cart_badge(props.get('session_key')),
            div(
                h2(
                    'Our Menu',
                    Class='isplay-5 fw-bold',
                ),
                p(
                    'Seasonally curated dishes.',
                    Class="text-muted"
                ),
                Class="text-center mb-5",
            ),
            menu_content,
            Class="container py-5",
        ),

        Id='menu',Class='page-section',
    )
    menu_comp = Component(name='customer-menu',template=menu+cart_modal(props),state=menu_state,props=props)
    return menu_comp.render()