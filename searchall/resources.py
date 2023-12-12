# resources.py

#************create excel resource for all models**********
from import_export import resources,fields
from accounts.models import FacultyCourseAddition, Course, Batch,Subject,Module,Topic,SubTopic,Branch,User,Faculty
class CourseResource(resources.ModelResource):
    course_name = fields.Field(attribute='id', column_name='Course ID')
    branch_name = fields.Field(attribute='name', column_name='Course Name')
    batch_type_name = fields.Field(attribute='batch_type__name', column_name='Batch Type')
    level_name = fields.Field(attribute='level__name', column_name='Level Name')
    class Meta:
        model = Course
        fields = []
        # column_name = {
        #     'id': 'Course ID',
        #     'name': 'Course Name',
        #     'batch_type_name': 'Batch Type',
        #     'is_online': 'Online Course',
        #     'level_name': 'Level'
        # }

class BatchResource(resources.ModelResource):
    batch_id = fields.Field(attribute='id', column_name='ID')
    batch_name = fields.Field(attribute='name', column_name='Batch Name')
    start_date = fields.Field(attribute='start_date', column_name='Start Date')
    end_date = fields.Field(attribute='end_date', column_name='End Date')
    course_name = fields.Field(attribute='course__name', column_name='Course Name')
    branch_name = fields.Field(attribute='branch__name', column_name='Branch Name')

    class Meta:
        model = Batch
        fields = []
        

class SubjectResource(resources.ModelResource):
    sub_id = fields.Field(attribute='id', column_name='ID')
    id = fields.Field(attribute='name', column_name='Batch Name')
    course_name = fields.Field(attribute='course__name', column_name='Course Name')
    class Meta:
        model = Subject
        fields = []
        
class ModuleResource(resources.ModelResource):
    id = fields.Field(attribute='id', column_name='ID')
    name = fields.Field(attribute='name', column_name='Module Name')
    subject_name = fields.Field(attribute='subject__name', column_name='Subject Name')
    class Meta: 
        model = Module
        fields = []
    
class TopicResource(resources.ModelResource):
    id = fields.Field(attribute='id', column_name='ID')
    name = fields.Field(attribute='name', column_name='Topic Name')
    subject_name = fields.Field(attribute='module__name', column_name='Module Name')
    day = fields.Field(attribute='day', column_name='Day')
    class Meta:
        model = Topic
        fields = []  

class SubTopicResource(resources.ModelResource):
    class Meta:
        model = SubTopic
        fields = ['id', 'name','topic__name','time_needed']
        

#branch,branchadmin,superuser
from import_export import resources
from import_export.fields import Field
from import_export import resources

class BranchResource(resources.ModelResource):
    class Meta:
        model = Branch
        fields = ['id','name','location','description']
        
    # courses = Field()
    
    # def dehydrate_courses(self, branch):
    #     return ', '.join([course.name for course in branch.courses.all()])

        
        
# class BrachAdminResource(resources.ModelResource):
#     class Meta:
#         model = BranchAdmin
#         fields = ['id','superadmin__username','branch__name']

class SuperAdminResource(resources.ModelResource):
    class Meta:
        model = User
        fields = ['id','username','email','mobile','joined_date','last_login']
   
   
class FacultyResource(resources.ModelResource):
    id = fields.Field(attribute='id', column_name='ID')
    name = fields.Field(attribute='user__username', column_name='Name')
    address = fields.Field(attribute='address', column_name='Address')
    gender = fields.Field(attribute='gender', column_name='Gender')
    district = fields.Field(attribute='district', column_name='District')
    address = fields.Field(attribute='whatsapp_contact_number', column_name='WhatsApp No')
    dob = fields.Field(attribute='date_of_birth', column_name='DOB')
    qualification = fields.Field(attribute='qualification', column_name='Qualification')

    class Meta:
        model = Faculty
        fields = []    

class FacultyCourseResource(resources.ModelResource):
    id = fields.Field(attribute='id', column_name='ID')
    name = fields.Field(attribute='user__username', column_name='Faculty Name')
    category = fields.Field(attribute='category', column_name='Category')
    level = fields.Field(attribute='level', column_name='Level')
    course = fields.Field(attribute='course', column_name='Course')
    subject = fields.Field(attribute='subject', column_name='Subject')
    module = fields.Field(attribute='module', column_name='Module')
    topic = fields.Field(attribute='topic', column_name='Topic')
    status = fields.Field(attribute='status', column_name='Status')
    class Meta: 
        model = FacultyCourseAddition
        fields = []

#********************end excel resouce**********************


################create pdf common file###################### 


from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from django.http import FileResponse
from io import BytesIO
from reportlab.lib.pagesizes import landscape, letter


from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.pdfgen.canvas import Canvas
from django.http import FileResponse
from io import BytesIO
import datetime



from io import BytesIO
import datetime

from django.http import FileResponse
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Table, TableStyle, Spacer
from reportlab.lib import colors


# def export_to_pdf(queryset, fields, file_name, header_text):
#     # Create the PDF file
#     buffer = BytesIO()
#     doc = BaseDocTemplate(buffer, pagesize=landscape(letter))

#     # Set up the frames
#     header_frame = Frame(doc.leftMargin, doc.height + doc.topMargin - 0.5 * inch, doc.width, 0.5 * inch, id='header_frame', showBoundary=0)
#     body_frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height - 0.5 * inch, id='body_frame', showBoundary=0)
#     doc.addPageTemplates([PageTemplate(id='TwoFrames', frames=[header_frame, body_frame])])

#     # Set up the stylesheet
#     styles = getSampleStyleSheet()
#     styles.add(ParagraphStyle(name='Header', parent=styles['Heading2'], alignment=TA_CENTER))

#     # Set up the header
#     header = Paragraph(header_text, styles['Header'])
#     header_in_frame = [header]

#     # Set up the table
#     data = [[field for field in fields]]
#     for obj in queryset:
#         data.append([getattr(obj, field) for field in fields])
#     table = Table(data, colWidths=[1.5*inch]*len(fields))

#     # Set up the table style
#     table.setStyle(TableStyle([
#         ('BACKGROUND', (0,0), (-1,0), colors.grey),
#         ('TEXTCOLOR', (0,0), (-1,0), colors.black),
#         ('ALIGN', (0,0), (-1,0), 'CENTER'),
#         ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
#         ('FONTSIZE', (0,0), (-1,0), 14),
#         ('BOTTOMPADDING', (0,0), (-1,0), 12),
#         ('BACKGROUND', (0,1), (-1,-1), colors.white),
#         ('TEXTCOLOR', (0,1), (-1,-1), colors.black),
#         ('ALIGN', (0,1), (-1,-1), 'LEFT'),
#         ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
#         ('FONTSIZE', (0,1), (-1,-1), 12),
#         ('BOTTOMPADDING', (0,1), (-1,-1), 8),
#         ('GRID', (0,0), (-1,-1), 1, colors.black)
#     ]))

#     # Build the flowables
#     flowables = header_in_frame + [Spacer(1, 0.5 * inch), table]

#     # Build the document
#     doc.build(flowables)

#     # Return the PDF as a response
#     buffer.seek(0)
#     return FileResponse(buffer, as_attachment=True, filename=file_name)



from django.utils import timezone

def export_to_pdf(queryset, fields, file_name, header_text):
    # Create the PDF file
    buffer = BytesIO()
    doc = BaseDocTemplate(buffer, pagesize=landscape(letter))

    # Set up the frames
    header_frame = Frame(doc.leftMargin, doc.height + doc.topMargin - 0.2 * inch, doc.width, 0.9 * inch, id='header_frame', showBoundary=0)
    body_frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height + 0.2 * inch, id='body_frame', showBoundary=0)
    doc.addPageTemplates([PageTemplate(id='TwoFrames', frames=[header_frame, body_frame])])

    # Set up the stylesheet
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Header', parent=styles['Heading2'], alignment=TA_CENTER))
    styles.add(ParagraphStyle(name='AceEducationCenter', parent=styles['Normal'], fontName='Helvetica', fontSize=10, alignment=TA_LEFT))

    # Set up the header
    header = Paragraph(header_text, styles['Header'])
    ace_education_center = Paragraph('Ace Education Center', styles['AceEducationCenter'])
    current_date = Paragraph(timezone.now().strftime('%Y-%m-%d %H:%M:%S'), styles['Normal'])
    header_in_frame = [header, ace_education_center, current_date]

    # Set up the table
    data = [[field for field in fields]]
    for obj in queryset:
        data.append([getattr(obj, field) for field in fields])
    table = Table(data, colWidths=[1.5*inch]*len(fields))

    # Set up the table style
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.black),
        ('ALIGN', (0,0), (-1,0), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 14),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('BACKGROUND', (0,1), (-1,-1), colors.white),
        ('TEXTCOLOR', (0,1), (-1,-1), colors.black),
        ('ALIGN', (0,1), (-1,-1), 'LEFT'),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,1), (-1,-1), 12),
        ('BOTTOMPADDING', (0,1), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 1, colors.black)
    ]))

    # Build the flowables
    flowables = header_in_frame + [Spacer(1, 0.5 * inch), table]

    # Build the document
    doc.build(flowables)

    # Return the PDF as a response
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=file_name)





####### pdf file for may foriegn key details like branch###########
def export_to_pdfs(queryset, file_name):
    # Create the PDF file
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)

    # Write the header row
    pdf.setFont("Helvetica", 16)
    pdf.drawString(50, 800, "No.")
    pdf.drawString(100, 800, "Branch Name")
    pdf.drawString(250, 800, "Location")
    pdf.drawString(400, 800, "Courses")

    # Write the data
    pdf.setFont("Helvetica", 12)
    y = 750
    for i, obj in enumerate(queryset):
        pdf.drawString(50, y, str(i + 1))  # Add the manual number
        pdf.drawString(100, y, obj.name)
        pdf.drawString(250, y, obj.location)
        courses = obj.courses.all()
        for course in courses:
            if y <= 50:  # Check if the next line will reach the page boundary
                pdf.showPage()
                y = 800
            pdf.drawString(400, y, course.name)
            y -= 50

    pdf.showPage()
    pdf.save()

    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=file_name)





