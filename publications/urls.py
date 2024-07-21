from django.urls import path
from publications.apps import PublicationsConfig
from publications.views import PublicationsListView, PublicationCreateView, PublicationsDetailView, \
    PublicationsUpdateView, PublicationsDeleteView, get_user_public

app_name = PublicationsConfig.name

urlpatterns = [
    path('', PublicationsListView.as_view(), name='list'),
    path('create/', PublicationCreateView.as_view(), name='create'),
    path('view/<int:pk>/', PublicationsDetailView.as_view(), name='detail'),
    path('update/<int:pk>/', PublicationsUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', PublicationsDeleteView.as_view(), name='delete'),
    path('user_public/', get_user_public, name='user_public'),
]
