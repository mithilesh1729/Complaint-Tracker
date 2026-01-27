from rest_framework.throttling import UserRateThrottle

class ComplaintRateThrottle(UserRateThrottle):
    scope = "complaints"
