from io import BytesIO
import os

from django.conf import settings
from django.utils.timezone import now

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

from reportlab.pdfgen import canvas

from reportlab.platypus import Paragraph
from reportlab.lib.enums import TA_CENTER


def generate_complaint_slip_pdf(
    complaint,
):
    """
    Professional Complaint Slip

    - Official institute layout
    - Automatic word wrapping
    - Dynamic spacing
    - Print friendly
    """

    buffer = BytesIO()

    c = canvas.Canvas(
        buffer,
        pagesize=A4,
    )

    width, height = A4

    LEFT = 45
    RIGHT = width - 45

    TOP = height - 60

    y = TOP

    LABEL_X = LEFT
    VALUE_X = LEFT + 165

    LINE_GAP = 18

    styles = getSampleStyleSheet()

    body_style = styles["BodyText"]
    body_style.fontName = "Helvetica"
    body_style.fontSize = 10
    body_style.leading = 16

    remark_style = styles["BodyText"]
    remark_style.fontName = "Helvetica-Oblique"
    remark_style.fontSize = 10
    remark_style.leading = 15

    title_style = styles["Heading2"]
    title_style.alignment = TA_CENTER

    # ==========================================================
    # HEADER
    # (UNCHANGED)
    # ==========================================================

    logo_path = os.path.join(
        settings.BASE_DIR,
        "static",
        "logo.png",
    )

    if os.path.exists(logo_path):

        c.drawImage(
            logo_path,
            LEFT,
            y - 55,
            width=60,
            height=50,
            preserveAspectRatio=True,
            mask="auto",
        )

    c.setFont(
        "Helvetica-Bold",
        20,
    )

    c.drawCentredString(
        width / 2,
        y - 10,
        "Complaint Slip",
    )

    c.setFont(
        "Helvetica-Bold",
        14,
    )

    c.drawCentredString(
        width / 2,
        y - 40,
        "National Institute of Technology, Patna",
    )

    c.setFont(
        "Helvetica",
        9,
    )

    c.setFillColor(
        colors.grey,
    )

    c.drawRightString(
        RIGHT,
        y - 15,
        f"Printed on: {now().strftime('%d %b %Y, %I:%M %p')}",
    )

    c.setFillColor(
        colors.black,
    )

    c.setLineWidth(1)

    c.line(
        LEFT,
        y - 70,
        RIGHT,
        y - 70,
    )

    y -= 100

    # ==========================================================
    # Helpers
    # ==========================================================

    def section(title):

        nonlocal y

        c.setFont(
            "Helvetica-Bold",
            13,
        )

        c.drawString(
            LEFT,
            y,
            title,
        )

        y -= 20


    def row(label, value):

        nonlocal y

        c.setFont(
            "Helvetica-Bold",
            10,
        )

        c.drawString(
            LABEL_X,
            y,
            label,
        )

        c.setFont(
            "Helvetica",
            10,
        )

        c.drawString(
            VALUE_X,
            y,
            str(value) if value else "-",
        )

        y -= LINE_GAP


    def paragraph(text):

        nonlocal y

        p = Paragraph(
            (text or "-").replace("\n", "<br/>"),
            body_style,
        )

        w, h = p.wrap(
            RIGHT - LEFT,
            500,
        )

        p.drawOn(
            c,
            LEFT,
            y - h,
        )

        y -= h + 10


    def latest_update():

        log = (
            complaint.status_logs
            .order_by("-timestamp")
            .first()
        )

        if not log:
            return "-"

        return log.message


    def formatted_status():

        return (
            complaint.status
            .replace("_", " ")
            .title()
        )


    def formatted_priority():

        return complaint.priority.title()


    def formatted_date(dt):

        if not dt:
            return "-"

        return dt.strftime(
            "%d %b %Y, %I:%M %p"
        )
        
        
        
        
        
    # ==========================================================
    # Complaint Information
    # ==========================================================

    section(
        "Complaint Information"
    )

    row(
        "Complaint Number",
        complaint.complaint_number,
    )

    row(
        "Category",
        complaint.category.name,
    )

    row(
        "Priority",
        formatted_priority(),
    )

    row(
        "Status",
        formatted_status(),
    )

    row(
        "Location",
        complaint.location_details,
    )

    row(
        "Created On",
        formatted_date(
            complaint.created_at
        ),
    )

    row(
        "Resolved On",
        formatted_date(
            complaint.resolved_at
        ),
    )

    y -= 12

    # ==========================================================
    # Student Information
    # ==========================================================

    section(
        "Student Information"
    )

    row(
        "Name",
        complaint.user.name,
    )

    row(
        "Roll Number",
        complaint.user.roll_no,
    )

    row(
        "Department",
        (
            complaint.user.department.name
            if complaint.user.department
            else "-"
        ),
    )

    row(
        "Hostel",
        complaint.user.hostel,
    )

    row(
        "Room Number",
        complaint.user.room_no,
    )

    row(
        "Phone Number",
        complaint.user.phone_number,
    )

    y -= 12

    # ==========================================================
    # Complaint Description
    # ==========================================================

    section(
        "Complaint Description"
    )

    paragraph(
        complaint.description
    )

    y -= 8

    # ==========================================================
    # Latest Update
    # ==========================================================

    section(
        "Latest Update"
    )

    latest = latest_update()

    p = Paragraph(
        latest,
        remark_style,
    )

    w, h = p.wrap(
        RIGHT - LEFT,
        120,
    )

    p.drawOn(
        c,
        LEFT,
        y - h,
    )

    y -= h + 25      
    
    
    
    
        # ==========================================================
    # Signature Section
    # ==========================================================

    # Keep signatures from going off the page
    if y < 140:

        c.showPage()

        y = TOP

    y -= 20

    c.setLineWidth(1)

    # Student Signature
    c.line(
        LEFT,
        y,
        LEFT + 170,
        y,
    )

    c.setFont(
        "Helvetica",
        10,
    )

    c.drawCentredString(
        LEFT + 85,
        y - 15,
        "Student Signature",
    )

    # Office Verification
    c.line(
        RIGHT - 170,
        y,
        RIGHT,
        y,
    )

    c.drawCentredString(
        RIGHT - 85,
        y - 15,
        "Office Verification",
    )

    # ==========================================================
    # FOOTER
    # (UNCHANGED)
    # ==========================================================

    c.setFont(
        "Helvetica",
        8,
    )

    c.setFillColor(
        colors.grey,
    )

    c.drawCentredString(
        width / 2,
        25,
        "System Generated Document | Complaint Tracking System",
    )

    c.showPage()

    c.save()

    buffer.seek(0)

    return buffer