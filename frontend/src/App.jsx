import { useState } from 'react';
import './index.css';

function App() {
  const [formData, setFormData] = useState({
    dateOfRequest: '',
    applicationNumber: '',
    applicantName: '',
    applicantAddress: '',
    caseType: '',
    apfNumber: '',
    techVisitNumber: '1',
    propertyAddressPlan: '',
    propertyAddressPostal: '',
    boundaryNorth: '',
    boundarySouth: '',
    boundaryEast: '',
    boundaryWest: '',
    flatUdsLandExtend: '',
    flatSuperBuildUpArea: '',
    buildingLandExtend: '',
    buildingBuildUpArea: '',
    landExtend: '',
    contactPersonName: '',
    contactPersonNumber: '',
    bcmName: ''
  });

  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
      const response = await fetch(`${apiUrl}/api/generate-tech-request`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      
      if (!response.ok) {
        throw new Error(`Server error: ${response.statusText}`);
      }

      // Handle the PDF blob
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `Tech_Request_${formData.applicationNumber || 'Draft'}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.parentNode.removeChild(link);
      
      alert('PDF generated and downloaded successfully!');
    } catch (error) {
      console.error('Error submitting form:', error);
      alert('Error submitting form. Make sure the Python backend is running on port 8000.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="app-layout">
      {/* Sidebar Navigation */}
      <aside className="sidebar">
        <h2>Ledgerly Forms</h2>
        <ul className="nav-list">
          <li className="nav-item active">Technical Request</li>
          <li className="nav-item">Other Forms...</li>
        </ul>
      </aside>

      {/* Main Content Area */}
      <main className="main-content">
        <div className="glass-card">
          <div className="form-header">
            <h1>Technical Request Form</h1>
            <p>Fill in the details to generate the PDF</p>
          </div>

          <form onSubmit={handleSubmit}>
            {/* General Info */}
            <h3 className="section-title">General Information</h3>
            <div className="form-grid">
              <div className="form-group">
                <label className="form-label">Date of Request</label>
                <input type="date" name="dateOfRequest" value={formData.dateOfRequest} onChange={handleChange} className="form-control" required />
              </div>
              <div className="form-group">
                <label className="form-label">Application Number</label>
                <input type="text" name="applicationNumber" value={formData.applicationNumber} onChange={handleChange} className="form-control" placeholder="e.g. APP123456" required />
              </div>
              <div className="form-group">
                <label className="form-label">Name of the Applicant</label>
                <input type="text" name="applicantName" value={formData.applicantName} onChange={handleChange} className="form-control" placeholder="John Doe" required />
              </div>
              <div className="form-group">
                <label className="form-label">Case Type</label>
                <select name="caseType" value={formData.caseType} onChange={handleChange} className="form-control" required>
                  <option value="" disabled>Select Case Type</option>
                  <option value="Builder (APF / Individual)">Builder (APF / Individual)</option>
                  <option value="Home Equity (LAP)">Home Equity (LAP)</option>
                  <option value="Resale">Resale</option>
                  <option value="Self Construction">Self Construction</option>
                  <option value="Land loan">Land loan</option>
                  <option value="Home Extension">Home Extension</option>
                  <option value="Home Improvement">Home Improvement</option>
                  <option value="Top up">Top up</option>
                  <option value="Purchase">Purchase</option>
                </select>
              </div>
            </div>

            <div className="form-grid full">
              <div className="form-group">
                <label className="form-label">Applicant Address with contact number</label>
                <textarea name="applicantAddress" value={formData.applicantAddress} onChange={handleChange} className="form-control" placeholder="Full address and phone number..." rows="2" required></textarea>
              </div>
            </div>

            <div className="form-grid">
              {(formData.caseType === 'Builder (APF / Individual)') && (
                <div className="form-group">
                  <label className="form-label">APF Number (if Builder/Individual)</label>
                  <input type="text" name="apfNumber" value={formData.apfNumber} onChange={handleChange} className="form-control" placeholder="APF Number" />
                </div>
              )}
              <div className="form-group">
                <label className="form-label">Tech Visit Number</label>
                <select name="techVisitNumber" value={formData.techVisitNumber} onChange={handleChange} className="form-control">
                  {[1, 2, 3, 4, 5, 6].map(num => (
                    <option key={num} value={num}>{num}</option>
                  ))}
                </select>
              </div>
            </div>

            {/* Property Address */}
            <h3 className="section-title">Property Details</h3>
            <div className="form-grid full">
              <div className="form-group">
                <label className="form-label">Address of the property as per Plan / Document</label>
                <textarea name="propertyAddressPlan" value={formData.propertyAddressPlan} onChange={handleChange} className="form-control" placeholder="Property address per plan..." rows="2" required></textarea>
              </div>
              <div className="form-group">
                <label className="form-label">Postal Address of the property with pin code</label>
                <textarea name="propertyAddressPostal" value={formData.propertyAddressPostal} onChange={handleChange} className="form-control" placeholder="Postal address and pincode..." rows="2" required></textarea>
              </div>
            </div>

            {/* Boundaries */}
            <h3 className="section-title">Boundaries</h3>
            <div className="form-grid">
              <div className="form-group">
                <label className="form-label">North</label>
                <input type="text" name="boundaryNorth" value={formData.boundaryNorth} onChange={handleChange} className="form-control" placeholder="North" />
              </div>
              <div className="form-group">
                <label className="form-label">South</label>
                <input type="text" name="boundarySouth" value={formData.boundarySouth} onChange={handleChange} className="form-control" placeholder="South" />
              </div>
              <div className="form-group">
                <label className="form-label">East</label>
                <input type="text" name="boundaryEast" value={formData.boundaryEast} onChange={handleChange} className="form-control" placeholder="East" />
              </div>
              <div className="form-group">
                <label className="form-label">West</label>
                <input type="text" name="boundaryWest" value={formData.boundaryWest} onChange={handleChange} className="form-control" placeholder="West" />
              </div>
            </div>

            {/* Area */}
            <h3 className="section-title">Area of the property in Sq.Ft</h3>
            
            <div className="form-grid">
              <div className="form-group">
                <label className="form-label">Flat - UDS Land Extend</label>
                <input type="text" name="flatUdsLandExtend" value={formData.flatUdsLandExtend} onChange={handleChange} className="form-control" placeholder="e.g. 500 Sq.Ft" />
              </div>
              <div className="form-group">
                <label className="form-label">Flat - Super Build up area</label>
                <input type="text" name="flatSuperBuildUpArea" value={formData.flatSuperBuildUpArea} onChange={handleChange} className="form-control" placeholder="e.g. 1200 Sq.Ft" />
              </div>
              
              <div className="form-group">
                <label className="form-label">Building - Land Extend</label>
                <input type="text" name="buildingLandExtend" value={formData.buildingLandExtend} onChange={handleChange} className="form-control" placeholder="e.g. 1000 Sq.Ft" />
              </div>
              <div className="form-group">
                <label className="form-label">Building - Build up area</label>
                <input type="text" name="buildingBuildUpArea" value={formData.buildingBuildUpArea} onChange={handleChange} className="form-control" placeholder="e.g. 2000 Sq.Ft" />
              </div>

              <div className="form-group">
                <label className="form-label">Land - Land Extend</label>
                <input type="text" name="landExtend" value={formData.landExtend} onChange={handleChange} className="form-control" placeholder="e.g. 1500 Sq.Ft" />
              </div>
            </div>

            {/* Contact Details */}
            <h3 className="section-title">Contact person details at site</h3>
            <div className="form-grid">
              <div className="form-group">
                <label className="form-label">Name</label>
                <input type="text" name="contactPersonName" value={formData.contactPersonName} onChange={handleChange} className="form-control" placeholder="Contact Name" />
              </div>
              <div className="form-group">
                <label className="form-label">Contact number</label>
                <input type="text" name="contactPersonNumber" value={formData.contactPersonNumber} onChange={handleChange} className="form-control" placeholder="Phone number" />
              </div>
            </div>

            <h3 className="section-title">Other Details</h3>
            <div className="form-grid">
              <div className="form-group">
                <label className="form-label">BCM Name (Signature of the BCM)</label>
                <input type="text" name="bcmName" value={formData.bcmName} onChange={handleChange} className="form-control" placeholder="Name for BCM Signature" />
              </div>
            </div>

            <button type="submit" className="btn btn-primary" disabled={isSubmitting}>
              {isSubmitting ? 'Generating PDF...' : 'Generate Form'}
            </button>
          </form>
        </div>
      </main>
    </div>
  );
}

export default App;
