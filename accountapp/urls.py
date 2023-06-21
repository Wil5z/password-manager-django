from django.urls import path
from . import views
   

urlpatterns = [
    path("", views.login_request),
    path("register", views.register_request, name="register"),
    path("home" , views.HomeView.as_view(), name="homepage"),
    path("login", views.login_request, name="userlogin"),
    path("logout", views.logout_request,name="logout"),
    path("savenewpassword", views.SavenewView.as_view() , name="savenew"),
    path("home/<int:pk>", views.DetialView,name="savedpasswords_detail"),
    path("home/<int:pk>/delete", views.DeletePassView.as_view(),name = "deleteit"),
    path("home/<int:pk>/edit", views.EditPassView.as_view(),name = "editit"),
    path("accountsettings/<int:pk>", views.AccountinfoView.as_view(), name="accountinfo"),
    #---------------! working account delete class view ------------------#
    # path("<int:pk>/accdelete", views.DeleteAccView.as_view(),name="deleteaccount"),
    path("<int:pk>/accdelete", views.DeleteAccView,name="deleteaccount"),
    path("changepassword", views.PassChangeView.as_view(),name="changepassword"),
    #new
    path("password_reset", views.password_reset_request, name="passwordreset")

]