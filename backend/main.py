from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TechRequestForm(BaseModel):
    dateOfRequest: str = ""
    applicationNumber: str = ""
    applicantName: str = ""
    applicantAddress: str = ""
    caseType: str = ""
    apfNumber: str = ""
    techVisitNumber: str = ""
    propertyAddressPlan: str = ""
    propertyAddressPostal: str = ""
    boundaryNorth: str = ""
    boundarySouth: str = ""
    boundaryEast: str = ""
    boundaryWest: str = ""
    flatUdsLandExtend: str = ""
    flatSuperBuildUpArea: str = ""
    buildingLandExtend: str = ""
    buildingBuildUpArea: str = ""
    landExtend: str = ""
    contactPersonName: str = ""
    contactPersonNumber: str = ""
    bcmName: str = ""

@app.post("/api/generate-tech-request")
async def generate_pdf(form_data: TechRequestForm):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    first_name = form_data.applicantName.split()[0] if form_data.applicantName.strip() else "Unknown"
    output_filename = f"TRF {first_name}.pdf"
    
    # We must write to /tmp on Vercel
    if os.environ.get("VERCEL"):
        output_path = os.path.join("/tmp", output_filename)
    else:
        output_path = os.path.join(base_dir, output_filename)
    
    try:
        doc = SimpleDocTemplate(output_path, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
        elements = []
        styles = getSampleStyleSheet()
        
        # Styles
        title_style = ParagraphStyle(name='TitleStyle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=14, alignment=1, spaceAfter=10)
        normal_bold = ParagraphStyle(name='NormalBold', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10)
        normal_style = ParagraphStyle(name='NormalStyle', parent=styles['Normal'], fontName='Helvetica', fontSize=10)
        
        def P(text, style=normal_style):
            return Paragraph(text, style)
            
        def B(text):
            return Paragraph(text, normal_bold)

        # 1. Title Table
        t_title = Table([[Paragraph("Technical Request", title_style)]], colWidths=[535])
        t_title.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('BOX', (0,0), (-1,-1), 1, colors.black),
            ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ]))
        elements.append(t_title)
        
        # Format Date
        formatted_date = form_data.dateOfRequest
        if formatted_date and "-" in formatted_date:
            try:
                from datetime import datetime
                date_obj = datetime.strptime(formatted_date, "%Y-%m-%d")
                formatted_date = date_obj.strftime("%d-%m-%Y")
            except ValueError:
                pass
                
        # 2. General Info Table
        data_general = [
            [B("Date of Request"), ": " + formatted_date],
            [B("Application Number"), ": " + form_data.applicationNumber],
            [B("Name of the Applicant"), ": " + form_data.applicantName],
        ]
        t_gen = Table(data_general, colWidths=[150, 385])
        t_gen.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 1, colors.black),
            ('INNERGRID', (0,0), (-1,-1), 1, colors.black),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        elements.append(t_gen)
        
        # 3. Applicant Address
        t_addr = Table([[B("Applicant Address with contact number :"), P(form_data.applicantAddress)]], colWidths=[200, 335])
        t_addr.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 1, colors.black),
            ('INNERGRID', (0,0), (-1,-1), 1, colors.black),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 30),
        ]))
        elements.append(t_addr)

        # 4. Case Type & APF
        data_case = [
            [B(f"Case Type : {form_data.caseType}")],
            [B(f"If Builder case / Individual tech, Provide APF Number : {form_data.apfNumber}")],
            [B(f"Tech Visit Number : {form_data.techVisitNumber}")]
        ]
        t_case = Table(data_case, colWidths=[535])
        t_case.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 1, colors.black),
            ('INNERGRID', (0,0), (-1,-1), 1, colors.black),
        ]))
        elements.append(t_case)

        # 5. Property Addresses
        t_prop1 = Table([[B("Address of the property as per Plan / Document"), P(form_data.propertyAddressPlan)]], colWidths=[235, 300])
        t_prop1.setStyle(TableStyle([('BOX', (0,0), (-1,-1), 1, colors.black), ('INNERGRID', (0,0), (-1,-1), 1, colors.black), ('VALIGN', (0,0), (-1,-1), 'TOP'), ('BOTTOMPADDING', (0,0), (-1,-1), 30)]))
        elements.append(t_prop1)
        
        t_prop2 = Table([[B("Postal Address of the property with pin code"), P(form_data.propertyAddressPostal)]], colWidths=[235, 300])
        t_prop2.setStyle(TableStyle([('BOX', (0,0), (-1,-1), 1, colors.black), ('INNERGRID', (0,0), (-1,-1), 1, colors.black), ('VALIGN', (0,0), (-1,-1), 'TOP'), ('BOTTOMPADDING', (0,0), (-1,-1), 30)]))
        elements.append(t_prop2)

        # 6. Boundaries Header
        t_bound_h = Table([[B("Boundaries")]], colWidths=[535])
        t_bound_h.setStyle(TableStyle([('BOX', (0,0), (-1,-1), 1, colors.black)]))
        elements.append(t_bound_h)
        
        # Boundaries data
        data_bound = [
            [B("North:"), P(form_data.boundaryNorth), B("South:"), P(form_data.boundarySouth)],
            [B("East:"), P(form_data.boundaryEast), B("West:"), P(form_data.boundaryWest)],
        ]
        t_bound = Table(data_bound, colWidths=[50, 217.5, 50, 217.5])
        t_bound.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 1, colors.black),
            ('INNERGRID', (0,0), (-1,-1), 1, colors.black),
        ]))
        elements.append(t_bound)

        # 7. Area Header
        t_area_h = Table([[B("Area of the property in Sq.Ft")]], colWidths=[535])
        t_area_h.setStyle(TableStyle([('BOX', (0,0), (-1,-1), 1, colors.black)]))
        elements.append(t_area_h)
        
        # Area data
        data_area = [
            [B("Flat"), ": UDS Land Extend :", P(form_data.flatUdsLandExtend), B("Super Build up area :"), P(form_data.flatSuperBuildUpArea)],
            [B("Building"), ": Land Extend :", P(form_data.buildingLandExtend), B("Build up area :"), P(form_data.buildingBuildUpArea)],
            [B("Land"), ": Land Extend :", P(form_data.landExtend), "", ""],
        ]
        t_area = Table(data_area, colWidths=[60, 110, 100, 120, 145])
        t_area.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 1, colors.black),
            ('INNERGRID', (0,0), (-1,-1), 1, colors.black),
        ]))
        elements.append(t_area)

        # 8. Contact Details Header
        t_cont_h = Table([[B("Contact person details at site")]], colWidths=[535])
        t_cont_h.setStyle(TableStyle([('BOX', (0,0), (-1,-1), 1, colors.black)]))
        elements.append(t_cont_h)
        
        data_cont = [
            [B("Name:"), P(form_data.contactPersonName), B("Contact number:"), P(form_data.contactPersonNumber)]
        ]
        t_cont = Table(data_cont, colWidths=[50, 217.5, 90, 177.5])
        t_cont.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 1, colors.black),
            ('INNERGRID', (0,0), (-1,-1), 1, colors.black),
        ]))
        elements.append(t_cont)

        # 9. Signature
        t_sig = Table([[B("Signature of the BCM :"), P(form_data.bcmName)]], colWidths=[150, 385])
        t_sig.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 1, colors.black),
            ('INNERGRID', (0,0), (-1,-1), 1, colors.black),
            ('BOTTOMPADDING', (0,0), (-1,-1), 30),
            ('TOPPADDING', (0,0), (-1,-1), 10),
        ]))
        elements.append(t_sig)

        # Build PDF
        doc.build(elements)
        
        # Return the generated file
        return FileResponse(output_path, filename=output_filename, media_type="application/pdf")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
