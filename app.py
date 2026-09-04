import io
import zipfile
import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PyPDF2 import PdfReader, PdfWriter

st.set_page_config(
    page_title="Master Multi-Form Auto-Filler",
    page_icon="📑",
    layout="wide"
)

# --- 1. FORM TEMPLATE CREATION FUNCTION ---
def create_base_template_pdf(title, subtitle, labels):
    """Dynamically generates a clean, structured base PDF form template."""
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    
    # Header Section
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, 740, title)
    c.setFont("Helvetica-Oblique", 11)
    c.drawString(50, 722, subtitle)
    c.line(50, 712, 560, 712)
    
    # Render Form Input Boxes
    y_pos = 660
    c.setFont("Helvetica-Bold", 10)
    
    for idx, label in enumerate(labels):
        c.drawString(50, y_pos + 15, f"{idx + 1}. {label}:")
        c.setLineWidth(1)
        c.rect(50, y_pos - 12, 510, 24)
        y_pos -= 60

    c.setFont("Helvetica-Oblique", 8)
    c.drawString(50, 40, "Official Form Template — Automated Streamlit System")
    
    c.save()
    buffer.seek(0)
    return buffer

# --- 2. OVERLAY & AUTO-FILL ENGINE ---
def fill_pdf_template(template_buffer, field_entries):
    """
    Overlays user text onto specific y-coordinates of a base PDF form template.
    field_entries = [{"text": "Alice", "y": 650}, ...]
    """
    overlay_buffer = io.BytesIO()
    c = canvas.Canvas(overlay_buffer, pagesize=letter)
    c.setFont("Helvetica", 11)
    
    for item in field_entries:
        text_str = str(item["text"]) if item["text"] is not None else ""
        c.drawString(60, item["y"], text_str)
        
    c.save()
    overlay_buffer.seek(0)
    
    # Merge overlay canvas with base template
    base_pdf = PdfReader(template_buffer)
    overlay_pdf = PdfReader(overlay_buffer)
    writer = PdfWriter()
    
    page = base_pdf.pages[0]
    page.merge_page(overlay_pdf.pages[0])
    writer.add_page(page)
    
    output = io.BytesIO()
    writer.write(output)
    output.seek(0)
    return output.getvalue()


# --- 3. STREAMLIT APP LAYOUT & LOGIC ---
st.title("📑 Master PDF Auto-Filler & Multi-Form Hub")
st.write(
    "Enter your information **once** in the unified interface below. "
    "The app automatically maps and fills all 10 underlying forms."
)

st.markdown("---")

with st.form("master_unified_form"):
    st.header("1. Common Information (Shared Across Forms)")
    st.caption("These details auto-fill into every form where required.")
    
    col1, col2 = st.columns(2)
    with col1:
        full_name = st.text_input("Full Name", value="Jane Doe")
        dob = st.date_input("Date of Birth")
        phone = st.text_input("Phone Number", value="+1 (555) 019-2834")
    with col2:
        email = st.text_input("Email Address", value="jane.doe@example.com")
        address = st.text_input("Street / Home Address", value="742 Evergreen Terrace")
        national_id = st.text_input("National ID / SSN / Tax ID", value="SSN-987-65-4321")

    st.markdown("---")
    st.header("2. Form-Specific Unique Details")
    st.caption("Provide specialized information required by individual institutions.")

    exp1, exp2, exp3 = st.columns(3)
    
    with exp1:
        with st.expander("🏦 Bank & Financial", expanded=True):
            bank_deposit = st.number_input("Initial Deposit ($)", value=1000, step=100)
            account_type = st.selectbox("Account Type", ["Savings Account", "Checking Account", "Fixed Deposit"])
            
        with st.expander("🎓 Education & School", expanded=True):
            student_grade = st.selectbox("Grade / Level", ["Kindergarten", "Grade 1-5", "High School", "Undergraduate"])
            guardian_name = st.text_input("Parent/Guardian Name", value="Robert Doe")

        with st.expander("📦 Postal & Logistics", expanded=True):
            recipient_name = st.text_input("Package Recipient Name", value="Alex Smith")
            recipient_address = st.text_input("Recipient Address", value="100 Main St, Springfield")
            pkg_weight = st.number_input("Package Weight (kg)", value=2.5, step=0.5)

    with exp2:
        with st.expander("🏥 Medical & Health", expanded=True):
            blood_group = st.selectbox("Blood Group", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
            primary_history = st.text_input("Medical Allergies/History", value="None / Penicillin Allergy")

        with st.expander("📚 Library Membership", expanded=True):
            dept_name = st.text_input("University Department", value="Computer Science")
            member_duration = st.slider("Membership (Years)", 1, 5, 2)

        with st.expander("🚗 DMV Vehicle Renewal", expanded=True):
            license_plate = st.text_input("License Plate No.", value="ABC-1234")
            vin_number = st.text_input("VIN Number", value="1HGCR2F83HA000000")

    with exp3:
        with st.expander("🏠 Housing & Lease", expanded=True):
            monthly_income = st.number_input("Monthly Income ($)", value=5500, step=500)
            occupants_count = st.number_input("Number of Occupants", value=2, min_value=1)

        with st.expander("✈️ Passport Renewal", expanded=True):
            passport_no = st.text_input("Current Passport No.", value="Z12345678")
            place_of_birth = st.text_input("Place of Birth", value="New York, USA")

        with st.expander("💼 Employment & Gym", expanded=True):
            job_title = st.text_input("Job Title", value="Software Engineer")
            gym_plan = st.selectbox("Gym Membership Plan", ["Gold Unlimited", "Silver Standard", "Weekend Pass"])

    submitted = st.form_submit_button("⚡ Auto-Fill All 10 Forms Simultaneously", type="primary")

# --- 4. FORM PROCESSING & GENERATION ---
if submitted:
    # Definition of the 10 forms with their base structure and data overlay mappings
    forms_config = [
        {
            "filename": "01_Bank_Account_Opening.pdf",
            "title": "01. National Savings Bank - Account Opening",
            "subtitle": "Customer Registration Form",
            "labels": ["Full Name", "Date of Birth", "Tax ID / SSN", "Initial Deposit ($)", "Account Type"],
            "mappings": [
                {"text": full_name, "y": 650},
                {"text": str(dob), "y": 590},
                {"text": national_id, "y": 530},
                {"text": f"${bank_deposit:,.2f}", "y": 470},
                {"text": account_type, "y": 410},
            ]
        },
        {
            "filename": "02_School_Admission.pdf",
            "title": "02. St. Jude Public School - Student Admission",
            "subtitle": "Academic Application Form",
            "labels": ["Student Full Name", "Date of Birth", "Grade Applying For", "Parent/Guardian Name", "Emergency Contact Phone"],
            "mappings": [
                {"text": full_name, "y": 650},
                {"text": str(dob), "y": 590},
                {"text": student_grade, "y": 530},
                {"text": guardian_name, "y": 470},
                {"text": phone, "y": 410},
            ]
        },
        {
            "filename": "03_Postal_Parcel_Dispatch.pdf",
            "title": "03. Express Postal Service - Parcel Dispatch",
            "subtitle": "Shipping Manifest",
            "labels": ["Sender Name", "Sender Address", "Recipient Name", "Recipient Address", "Package Weight (kg)"],
            "mappings": [
                {"text": full_name, "y": 650},
                {"text": address, "y": 590},
                {"text": recipient_name, "y": 530},
                {"text": recipient_address, "y": 470},
                {"text": f"{pkg_weight} kg", "y": 410},
            ]
        },
        {
            "filename": "04_Medical_Patient_Registration.pdf",
            "title": "04. City General Hospital - Patient Registration",
            "subtitle": "Medical Records Form",
            "labels": ["Patient Name", "Date of Birth", "Blood Group", "Medical Allergies/History", "Emergency Phone"],
            "mappings": [
                {"text": full_name, "y": 650},
                {"text": str(dob), "y": 590},
                {"text": blood_group, "y": 530},
                {"text": primary_history, "y": 470},
                {"text": phone, "y": 410},
            ]
        },
        {
            "filename": "05_University_Library_Membership.pdf",
            "title": "05. Central Academic Library - Membership",
            "subtitle": "Patron Registration",
            "labels": ["Full Name", "Email Address", "Department", "Phone Number", "Membership Duration"],
            "mappings": [
                {"text": full_name, "y": 650},
                {"text": email, "y": 590},
                {"text": dept_name, "y": 530},
                {"text": phone, "y": 470},
                {"text": f"{member_duration} Year(s)", "y": 410},
            ]
        },
        {
            "filename": "06_DMV_Vehicle_Registration.pdf",
            "title": "06. Department of Motor Vehicles - Renewal",
            "subtitle": "Vehicle Registration",
            "labels": ["Owner Name", "License Plate No.", "VIN Number", "Contact Email", "Home Address"],
            "mappings": [
                {"text": full_name, "y": 650},
                {"text": license_plate, "y": 590},
                {"text": vin_number, "y": 530},
                {"text": email, "y": 470},
                {"text": address, "y": 410},
            ]
        },
        {
            "filename": "07_Residential_Lease_Application.pdf",
            "title": "07. Metro Housing Authority - Lease Request",
            "subtitle": "Residential Application",
            "labels": ["Applicant Name", "Monthly Income ($)", "Number of Occupants", "Phone Number", "Email Address"],
            "mappings": [
                {"text": full_name, "y": 650},
                {"text": f"${monthly_income:,.2f}", "y": 590},
                {"text": str(occupants_count), "y": 530},
                {"text": phone, "y": 470},
                {"text": email, "y": 410},
            ]
        },
        {
            "filename": "08_Passport_Renewal.pdf",
            "title": "08. Passport & Immigration Bureau - Renewal",
            "subtitle": "Travel Document Application",
            "labels": ["Full Name", "Current Passport No.", "Place of Birth", "National ID / SSN", "Permanent Address"],
            "mappings": [
                {"text": full_name, "y": 650},
                {"text": passport_no, "y": 590},
                {"text": place_of_birth, "y": 530},
                {"text": national_id, "y": 470},
                {"text": address, "y": 410},
            ]
        },
        {
            "filename": "09_Employee_Onboarding.pdf",
            "title": "09. Apex Global Tech - Employee Onboarding",
            "subtitle": "Human Resources Profile",
            "labels": ["Employee Name", "Job Title", "Email Address", "Phone Number", "Emergency Contact"],
            "mappings": [
                {"text": full_name, "y": 650},
                {"text": job_title, "y": 590},
                {"text": email, "y": 530},
                {"text": phone, "y": 470},
                {"text": f"{guardian_name} ({phone})", "y": 410},
            ]
        },
        {
            "filename": "10_Fitness_Club_Membership.pdf",
            "title": "10. PowerFit Gym - Membership Application",
            "subtitle": "Club Enrollment",
            "labels": ["Member Name", "Membership Plan", "Phone Number", "Email Address", "Home Address"],
            "mappings": [
                {"text": full_name, "y": 650},
                {"text": gym_plan, "y": 590},
                {"text": phone, "y": 530},
                {"text": email, "y": 470},
                {"text": address, "y": 410},
            ]
        }
    ]

    generated_pdfs = {}
    zip_buffer = io.BytesIO()

    # Generate each form and bundle into a ZIP file
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for cfg in forms_config:
            # 1. Build base template in-memory
            base_pdf_buf = create_base_template_pdf(cfg["title"], cfg["subtitle"], cfg["labels"])
            
            # 2. Fill template with mapped inputs
            filled_pdf_bytes = fill_pdf_template(base_pdf_buf, cfg["mappings"])
            
            # 3. Store for preview and add to ZIP
            generated_pdfs[cfg["filename"]] = filled_pdf_bytes
            zip_file.writestr(cfg["filename"], filled_pdf_bytes)

    zip_buffer.seek(0)

    st.success("🎉 All 10 forms have been successfully processed and auto-filled!")

    # --- 5. DOWNLOAD & PREVIEW SECTION ---
    st.subheader("3. Download Package & Preview Documents")
    
    col_dl, col_blank = st.columns([1, 2])
    with col_dl:
        st.download_button(
            label="📦 Download All 10 Filled Forms (.ZIP)",
            data=zip_buffer,
            file_name="completed_10_forms_package.zip",
            mime="application/zip",
            type="primary"
        )

    st.markdown("---")
    st.write("### 👁️ Individual Document Inspection")
    selected_pdf_name = st.selectbox("Select a form to inspect:", list(generated_pdfs.keys()))

    if selected_pdf_name:
        st.download_button(
            label=f"📥 Download {selected_pdf_name}",
            data=generated_pdfs[selected_pdf_name],
            file_name=selected_pdf_name,
            mime="application/pdf"
        )
