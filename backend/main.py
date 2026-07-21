from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import fitz  # PyMuPDF
import os

app = FastAPI()

# Allow CORS for the React frontend
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

# Map fields to approximate (x, y) coordinates on an A4 page (595 x 842 points)
# Note: These coordinates are estimates based on standard form layout.
# You may need to tweak these x, y values to align perfectly with your PDF.
FIELD_COORDINATES = {
    "dateOfRequest": (200, 100),
    "applicationNumber": (200, 115),
    "applicantName": (200, 130),
    "applicantAddress": (50, 160),
    "caseType": (200, 270),
    "apfNumber": (200, 310),
    "techVisitNumber": (200, 340),
    "propertyAddressPlan": (50, 370),
    "propertyAddressPostal": (50, 480),
    "boundaryNorth": (100, 620),
    "boundarySouth": (300, 620),
    "boundaryEast": (100, 640),
    "boundaryWest": (300, 640),
    "flatUdsLandExtend": (150, 690),
    "flatSuperBuildUpArea": (450, 690),
    "buildingLandExtend": (150, 710),
    "buildingBuildUpArea": (450, 710),
    "landExtend": (150, 730),
    "contactPersonName": (150, 770),
    "contactPersonNumber": (150, 790),
    "bcmName": (50, 830),
}

@app.post("/api/generate-tech-request")
async def generate_pdf(form_data: TechRequestForm):
    # Determine absolute path relative to this script so it works on deployment
    base_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(base_dir, "Model", "Tech Request Format.pdf")
    
    # In deployment (like Render) or local, we can save the generated file to a temporary location
    output_filename = f"Generated_Tech_Request_{form_data.applicationNumber or 'Draft'}.pdf"
    output_path = os.path.join(base_dir, output_filename)
    
    if not os.path.exists(template_path):
        raise HTTPException(status_code=404, detail=f"PDF Template not found at {template_path}")

    try:
        # Open the PDF template
        doc = fitz.open(template_path)
        page = doc[0] # Assuming it's a 1-page form
        
        # Insert text for each field based on coordinates
        data_dict = form_data.model_dump()
        for field_name, value in data_dict.items():
            if value and field_name in FIELD_COORDINATES:
                x, y = FIELD_COORDINATES[field_name]
                # If text is long (like address), we could use insert_textbox, but for simplicity insert_text is used.
                if field_name in ["applicantAddress", "propertyAddressPlan", "propertyAddressPostal"]:
                    page.insert_textbox(fitz.Rect(x, y, 550, y+80), str(value), fontsize=10, fontname="helv")
                else:
                    page.insert_text((x, y), str(value), fontsize=10, fontname="helv")
        
        # Save the populated PDF
        doc.save(output_path)
        doc.close()
        
        # Return the generated file
        return FileResponse(output_path, filename=output_filename, media_type="application/pdf")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
