from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create/", views.create_deck, name="create_deck"),
    path("deck/<int:deck_id>/", views.deck_detail, name="deck_detail"),
    path("deck/<int:deck_id>/add/", views.add_card, name="add_card"),
    path("deck/<int:deck_id>/study/", views.study_deck, name="study_deck"),
    path('share/<int:deck_id>/', views.share_deck, name='share_deck'),
    # path("deck/<int:deck_id>/card/<int:card_id>/rate/", views.rate_card, name="rate_card"),
    # path("deck/<int:deck_id>/card/<int:card_id>/delete/", views.delete_card, name="delete_card"),
]