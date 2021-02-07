from django.contrib import admin
from django.urls import path,include
from users import views as user_views
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('register/',user_views.register,name='register'),
    path('profile/edit',user_views.profile,name='profile-edit'),
    path('login/',auth_views.LoginView.as_view(template_name='users/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='users/logout.html'),name='logout'),
    
    #NETWORK LOGIC
    path('profile/<int:pk>/',user_views.Profile_Detail_View.as_view(),name='detail_profile'),
    path('find/',user_views.ProfileListView.as_view(),name='FindFriends'),
    path('send-invite/',user_views.add_friends,name='send-invite'),
    path('remove-friend/',user_views.remove_friends,name='remove-friend'),
    path('invites/',user_views.Received_Invites,name='my-invites'),
    path('invites/accept',user_views.accept_invitations,name='accept'),
    path('invites/reject',user_views.reject_invitations,name='reject'),
    path('invites/withdraw',user_views.withdraw,name='withdraw'),
    #tinymce path

    path('', include('blog.urls')),
    path('tinymce/',include('tinymce.urls')),
    path('forum/',include('Forum.urls'))


]
urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
