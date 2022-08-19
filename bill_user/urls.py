from django.urls import path

urlpatterns = [
    path('login/',BillUserLoginView.as_view(),name="登录接口"),
    path('regist/',BillUserRegistView.ase_view(),name="注册接口"),
    path('logout/',BillUserLogoutView.as_view(),name="登出操作"),
    path('info/',BillUserInfoView.as_view(),name="用户详情"),
]
