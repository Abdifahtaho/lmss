from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'land_management'

urlpatterns = [
    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='land_management/general/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='land_management:login'), name='logout'),
    
    # User Profile & Management
    path('profile/', views.profile, name='profile'),
    path('profile/change-password/', views.change_password, name='change_password'),
    path('users/', views.user_list, name='user_list'),
    path('users/<int:user_id>/edit/', views.user_edit, name='user_edit'),
    path('users/<int:user_id>/reset-password/', views.user_reset_password, name='user_reset_password'),

    # Application URLs
    path('', auth_views.LoginView.as_view(template_name='land_management/general/login.html'), name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.land_registration, name='land_registration'),
    path('register/<int:registration_id>/', views.land_registration, name='edit_land_registration'),
    path('registration/<int:registration_id>/', views.registration_detail, name='registration_detail'),
    path('registration/<int:registration_id>/survey-payment/', views.survey_payment, name='survey_payment'),
    path('registration/<int:registration_id>/land-survey/', views.land_survey, name='land_survey'),
    path('registration/<int:registration_id>/tax-payment/', views.tax_payment, name='tax_payment'),
    path('registration/<int:registration_id>/land-mapping/', views.land_mapping, name='land_mapping'),
    path('registration/<int:registration_id>/approval/', views.approval_process, name='approval_process'),
    path('survey-payments/', views.list_survey_payments, name='list_survey_payments'),
    path('land-surveys/', views.list_land_surveys, name='list_land_surveys'),
    path('tax-payments/', views.list_tax_payments, name='list_tax_payments'),
    path('land-mappings/', views.list_land_mappings, name='list_land_mappings'),
    path('approvals/director/', views.list_director_approvals, name='list_director_approvals'),
    path('approvals/secretary/', views.list_secretary_approvals, name='list_secretary_approvals'),
    path('approvals/deputy-mayor/', views.list_deputy_mayor_approvals, name='list_deputy_mayor_approvals'),
    path('approvals/mayor/', views.list_mayor_approvals, name='list_mayor_approvals'),
    path('certificates/', views.certificate_list, name='certificate_list'),
    path('certificate/<int:registration_id>/', views.generate_certificate, name='generate_certificate'),
    path('certificate/<int:registration_id>/download/', views.download_certificate_pdf, name='download_certificate_pdf'),
    path('reports/', views.report, name='report'),
] 