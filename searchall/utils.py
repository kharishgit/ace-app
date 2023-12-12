from io import StringIO as StringIO
from xhtml2pdf import pisa
from django.template import Context
from django.http import HttpResponse
from django.template.loader import get_template
from django.contrib.staticfiles import finders
from django.conf import settings

def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    result = finders.find(uri)
    if result:
            logger.info(f"RESULT FIND URI---------------{result}")
            if not isinstance(result, (list, tuple)):
                    result = [result]
            result = list(os.path.realpath(path) for path in result)
            path=result[0]
    else:
            sUrl = settings.STATIC_URL        # Typically /static/
            sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
            mUrl = settings.MEDIA_URL         # Typically /media/
            mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/

            if uri.startswith(mUrl):
                    path = os.path.join(mRoot, uri.replace(mUrl, ""))
            elif uri.startswith(sUrl):
                    path = os.path.join(sRoot, uri.replace(sUrl, ""))
            else:
                    return uri

    # make sure that file exists
    if not os.path.isfile(path):
            raise Exception(
                    'media URI must start with %s or %s' % (sUrl, mUrl)
            )
    return path

def generate_pdf(template_src, context_dict,file_name='volofin.pdf'):
    context = context_dict
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename={file_name}'
    # find the template and render it.
    template = get_template(template_src)
    html = template.render(context)
    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response, link_callback=link_callback)
    print("hhhhhhhhhhhhhhhhhhhhhh")
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def generate_pdf_new(template_src, context_dict,file_name='volofin.pdf'):
    context = context_dict
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename={file_name}'
    # find the template and render it.
    template = get_template(template_src)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response, link_callback=link_callback)
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def get_queryset_headers_data(queryset, fields=None,manyKey={},arr=[]):
    model = queryset.model  # Get the model class from the queryset
    model_meta = model._meta
    
    keys={}
    for field in model_meta.get_fields():
        keys[field.name]=str(field.get_internal_type())
        if field.is_relation:
            relationship_type = field.get_internal_type()
            print(f"Field: {field.name}, Relationship Type: {relationship_type}")
    print(keys)
    
    if fields is None:
        headers = [field.name for field in model._meta.fields]
    else:
        headers = fields
    
    data = []

    for obj in queryset:
        obj_data = []
        for field in headers:
           

            try:
                new=keys[field]
            except:
                new = None

            if new=='ManyToManyField':

                if str(field) in arr:
                     
                    j=''
                    
                    val=getattr(obj, field, None)
                    p=val.all()
                    for value in p:

                        j+=str(value.__dict__.get(manyKey[field], None)) + ', '

                    obj_data.append(j)

                else:
                     
                    j=''
                    val=getattr(obj, field, None)
                    p=val.all()
                    for value in p:
                        # j+=str(value.name) + ', '
                        j+=str(value.__dict__.get('name', None)) + ', '

                    obj_data.append(j)
                
            elif '__' in field:  # Check if the field has a "__" indicating a related field
                related_fields = field.split('__')
                value = obj
                for related_field in related_fields:
                    value = getattr(value, related_field, None)
                    if value is None:
                        break
                obj_data.append(value)
            else:
                value = getattr(obj, field, None)
                obj_data.append(value)
        
        data.append(obj_data)
    
    # Remove the "__" prefix from headers
    formatted_headers = [field.split('__')[-1].capitalize() if '__' in field else field.capitalize() for field in headers]


    # Truncate headers and data strings to 10 characters
    max_line_length = 180//len(headers)  # Maximum length of a line
    truncated_headers = [header[:max_line_length] + '\n' + header[max_line_length:] if len(header) > max_line_length else header for header in formatted_headers]

#     truncated_data = [[str(value)[:13] + '\n' + str(value)[13:]+'\n'+str(value)[13:]+'\n' if len(str(value)) > 13 else str(value) for value in row] for row in data]
    truncated_data = [
                        [
                            '\n'.join(
                                [
                                    str(value)[i:i+max_line_length]  # Split the value into chunks of max_line_length
                                    for i in range(0, len(str(value)), max_line_length)
                                ]
                            )
                            if len(str(value)) > max_line_length
                            else str(value)
                            for value in row
                        ]
                        for row in data
                    ]



    print(truncated_headers, "%%%%%%%%%%%%5")
    print("*****************")
    print(truncated_data, "LLLLLLLLLLLLLLLLL")
    # print(len(str(truncated_data[0][0])))


    
    return truncated_headers, truncated_data


   