from django.urls import path
from .views import (
    signupfunc, loginfunc, Workview, Carelist, CareDetail, ProcessDetailView,
    get_related_processes)
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),  # Django管理画面
    path('logout/', LogoutView.as_view(next_page='/work/'), name='logout'),
    path('signup/', signupfunc, name='signup'), # 新規登録画面
    path('login/',loginfunc, name='login'),
    path('work/', Workview.as_view(), name='index_home'), #ホーム画面
    path('list/<int:pk>/', Carelist.as_view(), name='carelist'), #各作業の手順表示画面
    path('detail/<int:pk>/', CareDetail.as_view(), name='care_detail'), #マニュアル表示画面
    path('process/<int:pk>/', ProcessDetailView.as_view(), name='process_detail'), #手順表示画面
    path('get_related_processes/', get_related_processes, name='get_related_processes'), #関連手順の取得
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
