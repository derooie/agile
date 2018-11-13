from django.urls import path

from . import views

app_name = 'retrospectives'

urlpatterns = [
    path('<slug:slug>/', views.RetrospectiveDetailsView.as_view(), name='details'),
    path('<slug:slug>/add-values/', views.AddRetrospectiveNumberView.as_view(), name='add_values'),
    path('<int:pk>/update-values/', views.UpdateRetrospectiveNumberView.as_view(), name='update_values'),
    path('<int:pk>/feedback/', views.RetrospectiveUserFeedbackView.as_view(), name='feedback'),
    path('<int:feedback_pk>/<slug:slug>/vote/', views.vote, name='vote'),
    path('', views.IndexView.as_view(), name='index'),
]
