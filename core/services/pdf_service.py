from io import BytesIO
import os

from django.conf import settings
from django.utils.timezone import now

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors


def generate_complaint_slip_pdf(complaint):
    """
    Generate a clean, professional A4 Complaint Slip PDF.

    Design goals:
    - Clear visual hierarchy
    - Official institute-style layout
    - Good spacing & readability
    - Print-friendly
    """

    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    width, height = A4

    # =============================
    # Layout constants
    # =============================
    LEFT = 40
    RIGHT = width - 40
    TOP = height - 60
    y = TOP

    LABEL_X = LEFT
    VALUE_X = LEFT + 150
    LINE_GAP = 18

    # ---------------- HEADER ----------------

    # Logo (top-left)
    logo_path = os.path.join(settings.BASE_DIR, "static", "logo.png")
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

    # 🔑 MAIN TITLE (first, biggest)
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(
        width / 2,
        y - 10,
        "Complaint Slip"
    )

    # 🔑 SUBTITLE (below title)
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(
        width / 2,
        y - 40,
        "National Institute of Technology, Patna"
    )

    # Printed timestamp (small, metadata)
    c.setFont("Helvetica", 9)
    c.setFillColor(colors.grey)
    c.drawRightString(
        RIGHT,
        y - 15,
        f"Printed on: {now().strftime('%d %b %Y, %I:%M %p')}",
    )
    c.setFillColor(colors.black)

    # Divider
    c.setLineWidth(1)
    c.line(LEFT, y - 70, RIGHT, y - 70)

    # Push content down
    y -= 100


    # =============================
    # Helper functions
    # =============================

    def section(title):
        nonlocal y
        c.setFont("Helvetica-Bold", 12)
        c.drawString(LEFT, y, title)
        y -= 6
        c.setLineWidth(0.7)
        c.line(LEFT, y, RIGHT, y)
        y -= 20

    def row(label, value):
        nonlocal y
        c.setFont("Helvetica-Bold", 10)
        c.drawString(LABEL_X, y, label)
        c.setFont("Helvetica", 10)
        c.drawString(VALUE_X, y, value or "-")
        y -= LINE_GAP

    def boxed_text(title, text):
        nonlocal y
        c.setFont("Helvetica-Bold", 10)
        c.drawString(LABEL_X, y, title)
        y -= 12

        box_height = 80
        c.setLineWidth(0.6)
        c.rect(LEFT, y - box_height, RIGHT - LEFT, box_height)

        c.setFont("Helvetica", 10)
        text_y = y - 18
        for line in (text or "").split("\n"):
            c.drawString(LEFT + 10, text_y, line)
            text_y -= 14

        y -= box_height + 20

    # =============================
    # Complaint Information
    # =============================

    section("Complaint Information")
    row("Complaint ID", str(complaint.complaint_id))
    row("Status", complaint.status.replace("_", " ").title())
    row(
        "Created At",
        complaint.created_at.strftime("%d %b %Y, %I:%M %p"),
    )

    if complaint.resolved_at:
        row(
            "Resolved At",
            complaint.resolved_at.strftime("%d %b %Y, %I:%M %p"),
        )

    y -= 10

    # =============================
    # Student Details
    # =============================

    section("Student Details")
    row("Name", complaint.user.name)
    row("Roll Number", complaint.user.roll_no)
    row("Hostel", complaint.hostel)
    row("Room Number", complaint.room_no)
    row("Phone Number", complaint.phone_number)

    y -= 10

    # =============================
    # Complaint Details
    # =============================

    section("Complaint Details")
    row("Type", complaint.complaint_type.title())
    boxed_text("Description", complaint.description)

    # =============================
    # Admin Remarks (latest)
    # =============================

    if getattr(complaint, "latest_admin_remark", None):
        section("Admin Action / Remarks")
        boxed_text("Remarks", complaint.latest_admin_remark)

    # =============================
    # Signature
    # =============================

    y -= 40
    c.setLineWidth(1)
    c.line(RIGHT - 220, y, RIGHT, y)
    c.setFont("Helvetica", 10)
    c.drawRightString(RIGHT, y - 14, "Student Signature")

    # =============================
    # Footer
    # =============================

    c.setFont("Helvetica", 8)
    c.setFillColor(colors.grey)
    c.drawCentredString(
        width / 2,
        25,
        "System Generated Document | Complaint Tracking System",
    )

    c.showPage()
    c.save()

    buffer.seek(0)
    return buffer

