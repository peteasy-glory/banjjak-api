

# -*- coding: utf-8 -*-

from django.urls import path
from apiPerformance.views import api_performance

urlpatterns = [
    path('sales/performance/<str:partner_id>', api_performance.TPerformance.as_view()),
]
