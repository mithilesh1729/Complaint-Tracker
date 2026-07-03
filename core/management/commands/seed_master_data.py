from django.core.management.base import BaseCommand

from core.models import (
    Department,
    Hostel,
    ComplaintCategory,
)


class Command(BaseCommand):
    help = "Seed initial master data."

    def handle(self, *args, **options):

        departments = [
            ("CSE", "Computer Science and Engineering"),
            ("ECE", "Electronics and Communication Engineering"),
            ("EE", "Electrical Engineering"),
            ("ME", "Mechanical Engineering"),
            ("CE", "Civil Engineering"),
            ("MnC","Mathematics and Computing Technology"),
            ("CST", "Chemical Science and Technology"),
            ("MAE","Mechatronics and Automation Engineering"),
            ("HSS","Humanities & Social Sciences"),
            ("AP","ARCHITECTURE & PLANNING"),
            ("APME","Applied Physics and Materials Engineering"),
            
        ]

        for code, name in departments:
            Department.objects.get_or_create(
                code=code,
                defaults={
                    "name": name,
                },
            )

        hostels = [
            "Aryabhatta",
            "Kautilaya",
            "Brahmaputra",
            "Bagmati",
            "Kosi",
            "Kosi Extension",
            "Sone",
            "Ganga",
            "Kadimbini",
        ]

        for hostel in hostels:
            Hostel.objects.get_or_create(
                name=hostel,
            )

        categories = [
            (1, "Electricity"),
            (2, "Water"),
            (3, "Mess"),
            (4, "Furniture"),
            (5, "Cleanliness"),
            (6, "Internet/WiFi"),
            (7, "Other"),
        ]

        for order, name in categories:
            ComplaintCategory.objects.get_or_create(
                name=name,
                defaults={
                    "display_order": order,
                },
            )

        self.stdout.write(
            self.style.SUCCESS(
                "Master data seeded successfully."
            )
        )