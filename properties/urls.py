from django.urls import path
from . import views
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static

urlpatterns = [
      path('', views.home_page, name='home'), 
       path('', views.plot_list, name='plot_list'),
    path('create-state/', views.create_state, name='create_state'),
    path('state-list/', views.state_list, name='state_list'),
      path('add-district/', views.add_district, name='add_district'),
      path('get-districts/<int:state_id>/', views.get_districts, name='get_districts'),
        path('add-taluk/', views.add_taluk, name='add_taluk'),
         path('add-revenue-village/', views.add_revenue_village, name='add_revenue_village'),
     path('add-plot/', views.add_plot, name='add_plot'),
      path('get-revenue-villages/<int:taluk_id>/', views.get_revenue_villages, name='get_revenue_villages'),
    path('get-taluks/<int:district_id>/', views.get_taluks, name='get_taluks'),
     path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
     path('dashboard/', views.user_dashboard, name='user_dashboard'),
     path('logout/', views.user_logout, name='logout'),
           path('cart/', views.view_cart, name='view_cart'),  
    path('send_interest_email/', views.send_interest_email_view, name='send_interest_email'),
 path('add-to-cart/<int:plot_id>/', views.add_to_cart, name='add_to_cart'),
    
    path('remove-from-cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/process/', views.process_checkout, name='process_checkout'),
    path('order/confirmation/', views.order_confirmation, name='order_confirmation'),
    
       path('my-orders/', views.my_orders, name='my_orders'),
        
    path('order/<int:order_id>/', views.order_details, name='order_details'),  # Define the order_details route
    path('single_image_view/<int:pk>/', views.single_image_view, name='single_image_view'),
] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)