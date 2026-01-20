from probo.styles.frameworks.bs5.components import (
    BS5NavBar,
    BS5Button,
    BS5Collapse,
    BS5Nav,
    BS5Dropdown,
)
from probo import (
    div,span,a,ul,li,script,i
)
import json

def nav_bar(props):
    brand_link_text = 'The Rustic Spoon'
    nav_universal_content=[
        'Home','Menu','Reservation'
    ]

    nav_btn = BS5Button(
        span(Class="navbar-toggler-icon"),
        Type="button",
        data_bs_toggle = "collapse",
        data_bs_target = "#navbarNav",
        aria_controls = "navbarNav",
        aria_expanded = "false",
        aria_label = "Toggle navigation",
        Class="navbar-toggler",
    )

    # nav_btn.template.classes.remove('btn',)
    # nav_btn.template.classes.remove('btn-primary',)
    nav_link = a(
        brand_link_text,i(Class="bi bi-egg-fried"),
        Class="navbar-brand",
        href="{% url 'core:home' %}"
    )
    role_list= ['Customer','Staff','Admin',]
    role_hx_attrs= {
        0: {'hx_get':"/", 'hx_target':"#app", 'hx_swap':"innerHTML", 'hx_push_url':"true",'hx-vals':"js:{Viewer_role: 'customer',}",},
        1: {'hx_get':"/", 'hx_target':"#app", 'hx_swap':"innerHTML", 'hx_push_url':"true",'hx-vals':"js:{Viewer_role: 'staff',}",},
        2: {'hx_get':"/", 'hx_target':"#app", 'hx_swap':"innerHTML", 'hx_push_url':"true",'hx-vals':"js:{Viewer_role: 'admin',}",},
    }
    role_switcher = BS5Dropdown()#escape_btn=True)


    role_switcher.add_btn(f'Current View :',Class="btn btn-outline-success")
    role_switcher.add_menu(*role_list,items_attrs=role_hx_attrs)
    role_container = div(
        # role_switcher.dropdown_btn,
        role_switcher,
        Class="d-flex align-items-center gap-2",
    )
    nav = BS5Nav(Class="navbar-nav ms-auto")
    conter = 1
    for x in nav_universal_content:
        if conter==1:
            content = a(x,Class="nav-link active", href="{% url 'core:home' %}",Id=f'nav-{x.lower()}')
        else:
            content = a(x,Class="nav-link", href=f"#",Id=f'nav-{x.lower()}',hx_get=f"{{% url 'core:{x.lower()}' %}}", hx_target = "#app", hx_swap = "innerHTML", hx_push_url = "true",)
        nav.add_nav_item(content,)
        conter+=1

    collaps_navbar =BS5Collapse(nav.render(),Class="navbar-collapse",Id="navbarNav")
    def navbar_container(content):
        return div(content,Class="container")
    navbar = BS5NavBar(nav_link,nav_btn,collaps_navbar,role_container,wraper_func=navbar_container,Class='navbar-expand-lg navbar-light bg-light fixed-top shadow-sm')

    container = div(navbar.render(),Class="mb-1")
    return container
