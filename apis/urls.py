# from django.urls import path
# # from .views import login_api, logout_api, user_info_api, user_data_api, test_api
# from rest_framework.authtoken.views import obtain_auth_token

# # urlpatterns = [
# #     path('test/', test_api, name='test_api'),
# #     path('login/', login_api, name='login_api'),
# #     path('logout/', logout_api, name='logout_api'),
# #     path('user/info/', user_info_api, name='user_info_api'),
# #     path('user/data/', user_data_api, name='user_data_api'),
# #     path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
# # ]

# from . import views

# urlpatterns = [
#     path('test/', views.test_api, name='test_api'),
#     # path('csrf/', views.get_csrf, name='api-csrf'),
#     path('login/', views.login_view, name='api-login'),
#     path('logout/', views.logout_view, name='api-logout'),
#     path('session/', views.SessionView.as_view(), name='api-session'),  # new
#     path('whoami/', views.WhoAmIView.as_view(), name='api-whoami'),  # new
# ]


from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from .views import *

urlpatterns = [
    # path('register/', RegisterView.as_view(), name='register'),
    # path('login/', LoginView.as_view(), name='login'),
    # path('logout/', LogoutView.as_view(), name='logout'),
    # path('user/', UserDataView.as_view(), name='user'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('user/', handle_users, name='all_users'),
    path('user/<int:pk>/', user_info, name='user_info'),
    path('user/<int:pk>/subject/', get_user_subjects, name='user_subjects'),
    
    path('subject/', handle_subject, name='all_subjects'),
    path('subject/<int:pk>/', handle_one_subject, name='handle_one_subject'),
    path('subject/<int:pk>/user/', handle_subject_user, name='handle_subject_user'),
    path('subject/<int:pk>/professor/', handle_subject_professor, name='handle_subject_professor'),

    path('professor/', handle_professor, name='all_professor'),
    path('professor/<int:pk>/', handle_one_professor, name='handle_one_professor'),
    path('professor/<int:pk>/subject/', handle_professor_subject, name='handle_professor_subject'),

    path('term/', handle_term, name='all_terms'),
    path('term/<int:pk>/', get_term, name='term_info'),
    path('term/<int:pk>/subject/', handle_term_subject, name='term_subjects'),
]