from rest_framework.throttling import UserRateThrottle

class ComplaintRateThrottle(UserRateThrottle):
    scope = 'complaints'
    rate = '100/day'  # 100 requests per day per user