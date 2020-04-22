from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from shortener.views import RedirectAPI
from url_shortener import settings

api_v1 = [
    path('authentication/', include('authentication.urls')),
    path('shortener/', include("shortener.urls")),
    path('analytics/', include("analytics.urls")),

]

urlpatterns = [
    path('jet/', include(('jet.urls', 'jet'))),
    path('admin/', admin.site.urls),
    path('api/v1/', include(api_v1)),
    path('<short_code>/', RedirectAPI.as_view(), name="redirect")

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
