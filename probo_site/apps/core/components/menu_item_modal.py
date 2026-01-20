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
from probo import (
    ul,li,div,span,i,form,label,Input,button
)
from apps.core.forms import MenuItemForm
def field_wraper(field):
    return div(field,Class='mb-3',)


def admin_form(props,is_hx_oob=False):
    hx_oob = {"hx-on::after-request":"if(event.detail.successful) this.reset()",}
    if is_hx_oob:
        hx_oob.update({'hx-swap-oob': "true"})
    form_obj =MenuItemForm()
    menu_form = form(
        Input(Type='hidden',name='csrfmiddlewaretoken',value=f'{props.get("crf_token")}'),
      *[
    field_wraper(label(field.label) + str(field))
    for field in form_obj
],button('Add to Menu',Type='submit',Class="btn btn-primary w-100",),
        Id='addItemForm',
        method='post',
        hx_post= "{% url 'core:add_menu_item'%}",
        hx_target= "#admin-menu-list",
        hx_swap= "beforeend",
        hx_select='.admin-row',
        hx_push_url= "true",
        **hx_oob
        )
    return menu_form

def admin_menu_item_modal(props):


    menu_form = admin_form(props,)
    menu_item_template = BS5Modal(render_constraints={"Viewer_role": 'admin', }, Class="fade", Id="addItemModal",
                              tabindex="-1")
    menu_item_template.add_modal_header('', title='Add Menu Item', Class='bg-light text-dark')
    menu_item_template.add_modal_body(menu_form)
    menu_item_template.add_modal_footer(button('close',Type='submit',Class="btn btn-danger w-100",data_bs_dismiss='modal',data_bs_target='addItemModal',))
    menu_item_template.include_env_props(**props)
    return menu_item_template.render()
