
from django.contrib import admin
from django.urls import path, include
from core.views import home
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('category/<slug:category_slug>/', home, name='category_wise_book'),
    path('book/', include('book.urls')),
    path('account/', include('account.urls')),
    path('transaction/', include('transaction.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
