from core.selectors.dashboard_selector import DashboardSelector


class DashboardService:

    @staticmethod
    def get_student_dashboard(user):

        return DashboardSelector.get_student_dashboard_data(
            user
        )