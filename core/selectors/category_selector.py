from core.models import ComplaintCategory


class CategorySelector:
    """
    Read-only queries for complaint categories.
    """

    @staticmethod
    def list_active_categories():
        return (
            ComplaintCategory.objects
            .filter(
                is_active=True,
            )
            .order_by(
                "display_order",
                "name",
            )
        )