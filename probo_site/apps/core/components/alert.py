from probo import (
    div, button,
)

def get_messages_html():
    html = div(
        '{% if messages %}',
        '{% for message in messages %}',
        div(
            '{{ message }}',
            button(
                type="button",
                Class ="btn-close",
                data_bs_dismiss = "alert",
                aria_label = "Close",
            ),Class="alert alert-dismissible {% if message.tags %}alert-{{ message.tags }}{% endif %}"
        ),

        '{% endfor %}',
    '{% endif %}',
        Class="container page-section", Id="alert-container", hx_swap_oob="true"

    )
    return html