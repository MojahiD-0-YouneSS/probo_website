
from probo import (
    footer,div,p,small,
)

from probo.components import (
    Component,ComponentState,
)

def footer_section(props):
    footer_state = ComponentState(Viewer_role='customer',)
    footer_section_string = footer(
        div(
            p(
                '&copy; 2026 The Rustic Spoon. All rights reserved.',
                Class='mb-0'
            ),
            small(
                'Made with probo-ui/Bootstrap 5/django/htmx',
                Class='text-secondary',
            ),
            Class="container text-center",
        ),
        Class="bg-dark text-white py-4 mt-auto",
    )
    footer_comp=Component(name='footer',template=footer_section_string,state=footer_state,props=props)
    return footer_comp
