from django.conf.urls import include, url

urlpatterns = [
    url(r'^auth/', include('ersaauth.urls')),
]
