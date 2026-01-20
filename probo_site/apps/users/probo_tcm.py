
from probo import TemplateComponentMap

from django.http import HttpResponse
from django.template import Template, RequestContext
def render_probo(request, *raw_template_strings,**context):
    ''' use this to desplay html string as safe html and use it as django's render '''
    raw_template_string = ''.join(raw_template_strings)
    context = RequestContext(request, context)
    template = Template(raw_template_string)

    # 4. Render and Return
    return HttpResponse(template.render(context))

tcm = TemplateComponentMap() #mapper of component objects
