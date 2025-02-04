from django.contrib import admin
from django.urls import path, include
from tickets import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
router = DefaultRouter()
router.register('guests', views.viewsets_guests)
router.register('movies', views.viewsets_movie)
router.register('reservation', views.viewsets_reservation)
urlpatterns = [
    path('admin/', admin.site.urls),
    # 1
    path('nrnm/', views.NRNM),
    # 2
    path('nrwm/', views.NRWM),
    # 3.1
    path('fbv-list/', views.FBV_LIST),
    # 3.2
    path('fbv-pk/<int:pk>/', views.FBV_pk),
    # 4.1
    path('cbv-list/', views.CBV_LIST.as_view()),
    # 4.2
    path('cbv-pk/<int:pk>/', views.CBV_PK.as_view()),
    # 5.1
    path('mixins-list/', views.mixins_list.as_view()),
    # 5.2
    path('mixins-pk/<int:pk>/', views.mixins_pk.as_view()),
    # 6.1
    path('generics-list/', views.generics_list.as_view()),
    # 6.2
    path('generics-pk/<int:pk>/', views.generics_pk.as_view()),
    # 7
    path('viewsets-guests/', include(router.urls)),
    path('viewsets-movies/', include(router.urls)),
    path('viewsets-reservations/', include(router.urls)),
    # 8
    path('fbv/find-movie/', views.find_movie),
    # 9
    path('fbv/reserve/', views.reserve),
    # 10
    path('api-auth', include('rest_framework.urls')),
    # 11
    path('api-token-auth', obtain_auth_token, name='api-token-auth'),

]
