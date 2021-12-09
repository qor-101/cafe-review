from django.urls import path
from . import views

urlpatterns = [
        path('',views.index,name='default page'),
        path('write-review',views.new_review,name='new review'),
        path('upload',views.upload_review,name='upload review'),
        path('search',views.search,name='search'),
        path('fetch',views.fetch,name='fetch'),
        path('results',views.results,name='results'),
        path('login',views.login_user,name='login_user'),
        path('signup',views.signup_user,name='signup_user'),
        path('profile',views.profile,name='profile'),
        path('logout',views.logout_user,name='logout_user'),
        path('dashboard',views.dash_user,name='dash-user'),
]
