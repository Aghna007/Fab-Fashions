from django.urls import path,include
from.import views

urlpatterns = [
    path('',views.index,name='index'),
    path('register/',views.register,name='register'),
    path('Login/',views.login,name='Login'),
    path('home/',views.home,name='home'),
    path('Logout/',views.logout,name='Logout'),
    path('Profile/',views.profile,name='Profile'),
    path('home/editprofile/',views.editprofile,name='editprofile'),
    path('productlist_user/',views.productlist_user,name='productlist_user'),
    path('productlist_admin/',views.productlist_admin,name='productlist_admin'),
    path('adminlogin/',views.adminlogin,name='adminlogin'),
    path('adminhome/',views.adminhome,name='adminhome'),
    path('userlist_admin/',views.userlist_admin,name='userlist_admin'),
    path('editproduct/<int:id>/',views.editproduct,name='editproduct'),
    path('deleteproduct/<int:id>/',views.deleteproduct,name='deleteproduct'),
    path('addproducts/',views.addproducts,name='addproducts'),
    path('shopowner_register/',views.shopowner_register,name='shopowner_register'),
    path('owner_login/',views.owner_login,name='owner_login'),
    path('owner_home/',views.owner_home,name='owner_home'),
    path('owner_profile/',views.owner_profile,name='owner_profile'),
    path('editprofile/',views.owner_editprofile,name='owner_editprofile'),
    path('addproducts_owner/',views.addproducts_owner,name='addproducts_owner'),
    path('productlist_shop/',views.productlist_shop,name='productlist_shop'),
    path('editproduct_owner/<int:id>/',views.editproduct_owner,name='editproduct_owner'),
    path('add_to_cart/<int:id>/',views.add_to_cart,name='add_to_cart'),
    path('cart_list/',views.cart_list,name='cart_list'),path('remove_from_cart/<int:id>/',views.remove_from_cart,name='remove_from_cart'),
    path('product_detail/<int:id>/',views.product_detail,name='product_detail'),
    path('buy_now/<int:id>/',views.buy_now,name='buy_now'),
    path('checkout/',views.checkout,name='checkout'),
    path('orderlist_user/',views.orderlist_user,name='orderlist_user'),
    path('feedback/',views.feedback,name='feedback'),
    path('feedback_list/',views.feedback_list,name='feedback_list'),
    path('feedback_user/',views.feedback_user,name='feedback_user'),
    path('wishlist/<int:id>/',views.wishlist,name='wishlist'),
    path('wishlist_user/',views.wishlist_user,name='wishlist_user'),
    path('add_feedback/<int:id>/',views.add_feedback,name='add_feedback'),
    path('orderlist_owner/', views.orderlist_owner, name='orderlist_owner'),
    path('order_list/', views.order_list, name='order_list'),
    path('add_designer_owner/', views.add_designer_owner, name='add_designer_owner'),
    path('designer_login/', views.designer_login, name='designer_login'),
    path('designer_home/', views.designer_home, name='designer_home'),
    path('designer_list/', views.designer_list, name='designer_list'),
    path('designer_list_admin/', views.designer_list_admin, name='designer_list_admin'),
    path('designer_profile/',views.designer_profile,name='designer_profile'),
    path('designer_editprofile/',views.designer_editprofile,name='designer_editprofile'),


    #customization
    path('addcustomization/',views.addcustomization,name='addcustomization'),
    path('mycustomizationlist/',views.mycustomizationlist,name='mycustomizationlist'),
    path('customization_list_admin/',views.customization_list_admin,name='customization_list_admin'),
    path('customlist_owner/',views.customlist_owner,name='customlist_owner'),
    path('customlist_designer/',views.customlist_designer,name='customlist_designer'),
    path('approve_customization_designer/<int:id>/',views.approve_customization_designer,name='approve_customization_designer'),
    path('reject_customization_designer/<int:id>/',views.reject_customization_designer,name='reject_customization_designer'),


    


]

 