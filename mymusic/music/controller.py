from django.urls import path,include
from .views import index,detail,loginpage,signup,Addalbum,UpdateAlbum,AddSong,UpdateSong,Signout,DelAlbum,DelSong,search,search1

app_name='music'

urlpatterns = [
    path('',index.as_view(),name='index'),
    path('<int:pk>',detail,name='detail'),
    path('login',loginpage.as_view(),name='login'),
    path('signup',signup.as_view(),name='signup'),
    path('album/add',Addalbum.as_view(),name='addalbum'),
    path('album/update/<int:pk>',UpdateAlbum.as_view(),name='updatealbum'),
    path('song/add/<int:pk>',AddSong.as_view(),name='addsong'),
    path('song/update/<int:pk>',UpdateSong.as_view(),name='updatesong'),
    path('album/delete/<int:pk>',DelAlbum.as_view(),name='deletealbum'),
    path('song/delete/<int:pk>',DelSong.as_view(),name='deletesong'),
    path('logout',Signout,name='signout'),
    path('search',search,name='search'),
    path('search1',search1,name='search1'),

]
