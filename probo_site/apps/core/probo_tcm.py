from probo.context import TemplateComponentMap
from django.utils.safestring import mark_safe
from django.template import Template, RequestContext

def render_probo(request, *raw_template_strings,**context):
    ''' use this to desplay html string as safe html and use it as django's render '''
    raw_template_string = ''.join([tmplt.render() if hasattr(tmplt,'render') else str(tmplt) for tmplt in raw_template_strings])
    context = RequestContext(request, context)
    template = Template(raw_template_string)

    # 4. Render and Return
    return mark_safe(template.render(context))

tcm = TemplateComponentMap() #mapper of component objects
