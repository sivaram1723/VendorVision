from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.analyze_place_reviews, name='index'),
    path('fetch_reviews_and_sentiment/<str:place_id>/', views.fetch_reviews_and_sentiment, name='fetch_reviews_and_sentiment'),
    path('review_dashboard/<str:place_id>/', views.review_dashboard, name='review_dashboard'),  # New route
    path('analyze_live_review/', views.analyze_live_review, name='analyze_live_review'),
    path('live_analysis/', views.live_analysis, name='live_analysis'),
]