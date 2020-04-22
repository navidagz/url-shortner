from django.conf.urls import url
from django.urls import include, path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from authentication.views import UserCreateViewAPI, TokenObtainPairView

router = SimpleRouter()

# Register route
router.register("register", UserCreateViewAPI, "user")

urlpatterns = [
    # Obtain token route
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    # Refresh token route
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Verify token route
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # Add router urls
    url(r'', include(router.urls)),
]
