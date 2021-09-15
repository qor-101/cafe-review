from django.urls import path
from . import views

urlpatterns = [
        path('',views.index,name='default page'),
        path('write-review',views.new_review,name='new review'),
        path('upload',views.upload_review,name='upload review'),
        path('upload-success',views.upload_success,name='upload success'),
        path('upload-failed',views.upload_failed,name='upload failed'),
        path('search',views.search,name='search'),
        path('fetch',views.fetch,name='fetch'),
        path('results',views.results,name='results'),
        path('noresults',views.noresults,name='noresults'),
        path('login',views.login,name='login'),
]
