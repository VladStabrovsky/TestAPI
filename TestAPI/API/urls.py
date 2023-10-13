from django.urls import path

from API.views import *

urlpatterns = [
    path('', index),
    path('user_credits/<int:user_id>', user_credits.as_view()),
    path('plans_insert', plans_insert.as_view()),
    path('plans_performance', plans_performance.as_view()),
    path('year_performance', year_performance.as_view())
]
