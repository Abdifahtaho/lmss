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
    path('users/create/', views.create_user, name='user_create'),

    # Application URLs
    path('', auth_views.LoginView.as_view(template_name='land_management/general/login.html'), name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.land_registration, name='land_registration'),
    path('register/<int:registration_id>/', views.land_registration, name='edit_land_registration'),
    path('gift-register/', views.gift_land_registration, name='gift_land_registration'),
    path('gift-register/<int:registration_id>/', views.gift_land_registration, name='edit_gift_land_registration'),
    path('inheritance-register/', views.inheritance_land_registration, name='inheritance_land_registration'),
    path('inheritance-register/<int:registration_id>/', views.inheritance_land_registration, name='edit_inheritance_land_registration'),
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
    path('registrations/', views.registration_list, name='registration_list'),
    path('registrations/<int:registration_id>/edit/', views.edit_land_registration, name='edit_land_registration'),
    path('registrations/<int:registration_id>/delete/', views.delete_land_registration, name='delete_land_registration'),
    path('password-reset/', views.password_reset_request, name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='land_management/general/password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='land_management/general/password_reset_confirm.html',
        success_url='/password-reset/complete/'
    ), name='password_reset_confirm'),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='land_management/general/password_reset_complete.html'
    ), name='password_reset_complete'),
    
    # Password Reset Approval (Superuser Only)
    path('password-reset-approval/', views.password_reset_approval_dashboard, name='password_reset_approval_dashboard'),
    path('password-reset-approval/<int:request_id>/approve/', views.approve_password_reset, name='approve_password_reset'),
    path('password-reset-approval/<int:request_id>/reject/', views.reject_password_reset, name='reject_password_reset'),
    
    # Notifications (Superuser Only)
    path('notifications/', views.notifications_view, name='notifications'),
    path('notifications/<int:notification_id>/mark-read/', views.mark_notification_read, name='mark_notification_read'),
    path('ajax/check-password-reset/', views.check_pending_password_reset, name='ajax_check_password_reset'),
] 