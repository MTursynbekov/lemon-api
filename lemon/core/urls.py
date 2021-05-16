from django.urls import path
from rest_framework import routers

from core import views

router = routers.DefaultRouter()
router.register(r'categories', views.CategoryViewSet, basename='core')
router.register(r'stores', views.StoreViewSet, basename='core')
router.register(r'promotions', views.PromotionViewSet, basename='core')
router.register(r'products', views.ProductViewSet, basename='core')
router.register(r'product_images', views.ProductImageViewSet, basename='core')
router.register(r'product_specifications', views.ProductSpecificationViewSet, basename='core')

urlpatterns = router.urls

urlpatterns += [
       path('cities/', views.cities_list),
       path('cities/<int:pk>/', views.get_city),
       path('cities/<int:pk>/products/', views.get_city_products),
       path('brands/', views.BrandsListAPIView.as_view()),
       path('brands/<int:pk>/', views.BrandDetailAPIView.as_view()),
       path('brands/<int:pk>/promotions/', views.BrandsPromotionsAPIView.as_view())
]


