from django.urls import path
from .views import *

urlpatterns = [
    path('', technos, name='products'),
    path('category/<int:cat_id>/', category_filter, name='products-category'),
    path('Mahsulot malumoti/<int:pk>/', MahsulotlarDetail.as_view(), name='products_detail'),
    path('comment/<int:pk>/edit/', comment_edit, name='comment_edit'),
    path('comment/<int:pk>/delete/', comment_delete, name='comment_delete'),
    path('mahsulot/qoshish', MahsulotlarCreate.as_view(), name='mahsulot_add'),
    path('mahsulot/<int:pk>/ozgartirish/', MahsulotlarUpdate.as_view(), name='mahsulot_update'),
    path('mahsulot/<int:pk>/delete/', MahsulotlarDelete.as_view(), name='mahsulot_delete'),
    path('profile/', profile, name='profile'),
    path('update-profile/', update_profile, name='update_profile'),
]