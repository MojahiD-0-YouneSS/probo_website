from probo import (
    section,div,h3,form,label,span,Input,select,option,button,i,
)
from probo.components import (
    Component,ComponentState,
)
from .cart import cart_modal,cart_badge
from probo.components import (ProboForm,ProboFormField,)
from probo.styles.frameworks.bs5.components import BS5Card,BS5Button
from probo.htmx import HTMXElement

def reservation_section(request_data,props):
    reservation_state=ComponentState(Viewer_role='customer')
    text_input = ProboFormField()
    text_input.add_custom_field(div(
        label(
            'Full Name',
            Class="form-label"
        ),
        div(
            span(
                i(
                    Class="bi bi-person"
                ),
                Class="input-group-text"
            ),
            Input(
                Type="text",
                Class ="form-control",
                placeholder="Jane Doe",
                required='required',
                name='full_name'
            ),
            Class="input-group"
        ),
        Class='mb-3'
    ))
    def field_wraper(content):
        return div(content,Class="col")
    def form_field_wraper(content):
        return div(content,Class="row mb-3")
    date_booking_field = ProboFormField('input',field_label='Date',label_attr={'class':'form-label'},wraper_func=field_wraper,Type='date',Class='form-control',required='required',name='booked_date')
    time_booking_field = ProboFormField('input',field_label='Time',label_attr={'class':'form-label'},wraper_func=field_wraper,Type='time',Class='form-control',required='required',name='booked_time')

    datetime_booking_field = ProboFormField(wraper_func=form_field_wraper)

    datetime_booking_field.add_custom_field(
        date_booking_field.render(),
        time_booking_field.render(),

    )

    def select_wraper(content):
        return div(content,Class='mb-4')

    select_field = ProboFormField(wraper_func=select_wraper)
    select_options = [
        '2 People',
        '3 People',
        '4 People',
        '5+ People',
    ]
    select_field.add_select_option(select_options,[0],'Number of Guests',{'class':"form-label"},Class="form-select",name='number_of_guests')
    form_button = ProboFormField()
    form_button.add_custom_field(div(BS5Button(
        'Confirm Booking',
        variant='dark',
        Type="submit",
        ).lg.render(), Class='d-grid'))
    reservation_form = ProboForm('{% url "core:book_table" %}',text_input,datetime_booking_field,select_field,form_button,method='POST',override_button=True,request_data=request_data,Id="reservation-form")

    reservation_card = BS5Card(Class='shadow')
    reservation_card.add_card_header(
        h3(
            'Table Reservation',
            Class="mb-0",
        ),
        Class='bg-warning text-white text-center py-3',
    )
    reservation_card.add_card_body(
        reservation_form,
        Class='p-4'
    )
    reservation_section = section(
        div(cart_badge(props.get('session_key')),
            div(
                div(
                    reservation_card,
                    Class="col-md-8 col-lg-6"
                ),
                Class="row justify-content-center"
            ),
            Class="container py-5"
        ),
        Id="contact",Class ="page-section"
    )+cart_modal(props)

    reservation_comp = Component(name='customer-reservation',template=reservation_section,state=reservation_state,props=props)
    return reservation_comp.render()