from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter
from apps.users.views import (
    LoginUser, ValidateEmail, ForgotPassword,
    SignupUser, CurrentUserProfile, ResetPassword,
    ChangePassword, UpdateUserAvatar, ResendSignupVerification
)
router = DefaultRouter()

urlpatterns = [
    path('signup/', SignupUser.as_view()),
    path('login/', LoginUser.as_view()),
    path('forgot_password/', ForgotPassword.as_view()),
    path('validate_email/', ValidateEmail.as_view()),
    path('resend_verification_email/', ResendSignupVerification.as_view()),
    path('reset_password/', ResetPassword.as_view()),
    path('change_password/', ChangePassword.as_view()),
    path('update_user_avatar/', UpdateUserAvatar.as_view()),
    path('me/', CurrentUserProfile.as_view()),
    path('', include(router.urls)),
]
