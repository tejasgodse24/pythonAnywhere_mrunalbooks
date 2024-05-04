from io import BytesIO
from django.template.loader import get_template
import xhtml2pdf.pisa as pisa
from django.conf import settings


def save_invoice_pdf(params:dict, invoive_no):
    template = get_template("pdfs/invoice.html")
    html = template.render(params)
    response = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), response)
    file_name = invoive_no
    
    try:
        # with open(str(settings.BASE_DIR) + f"/public/media/invoices/{file_name}.pdf", "wb") as output :
        with open(f"/var/www/mrunalbooks/media/invoices/{file_name}.pdf", "wb") as output : 
            pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), output)
    except Exception as e:
        print(e)

    if pdf.err:
        return "", False
    
    return file_name, True

def save_courier_script_pdf(params:dict, invoive_no):
    template = get_template("pdfs/courier_script.html")
    html = template.render(params)
    response = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), response)
    file_name = invoive_no + '_courier_script'
    
    try:
        # with open(str(settings.BASE_DIR) + f"/public/media/courier_scripts/{file_name}.pdf", "wb") as output : 
        with open(f"/var/www/mrunalbooks/media/courier_scripts/{file_name}.pdf", "wb") as output : 
            pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), output)
    except Exception as e:
        print(e)

    if pdf.err:
        return "", False
    
    return file_name, True


