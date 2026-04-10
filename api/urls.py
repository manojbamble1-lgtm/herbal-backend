from django.urls import path
from . import views   # ✅ safer import

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('profile/', views.get_user_profile, name='profile'),
    path('remedy/', views.get_remedy, name='remedy'),
    path('health-score/', views.health_score, name='health_score'),
    path('ai-chat/', views.ai_chat, name='ai_chat'),
    path('scan-herb/', views.scan_herb_ai),
    path('emotion/', views.emotion_ai, name='emotion'),
    path('dna-engine/', views.herb_dna_engine),
    path('feedback/', views.herb_feedback),

]