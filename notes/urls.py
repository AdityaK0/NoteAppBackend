from django.urls import path
from .views import *
urlpatterns = [
    path('',home),
    path('api/',home),
    path('api/v1/',home),
    path('api/v1/notes/',allList),
    path('api/v1/notes/add-note/',add_note),
    path('api/v1/notes/<int:id>/',get_note),
    path('api/v1/notes/update/<int:id>/',update_note),
    path('api/v1/notes/delete/<int:id>/',delete_note),
    path('api/v1/notes/pin-note/<int:id>/',pin_note),
    path('api/v1/notes/search-notes/',search_notes),
]
