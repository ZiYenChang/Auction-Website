from django.urls import include, path, re_path
from django.conf import settings
from django.conf.urls.static import static

from . import views
# search
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path("accounts/login/", views.login, name="login"),
    path("accounts/signup/", views.signup, name="signup"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api/questions/',views.questions_api, name = 'questions'),
    path('api/question/<int:question_id>',views.question_api),
    path('api/bids/',views.bids_api),
    path('api/item/<int:item_id>',views.item_api),
    path('api/answers/',views.answers_api),
    path("api/user/", views.user_api),
    path('api/items/', views.newitem_api),
    path('api/item/search/', csrf_exempt(views.search_api)),
    path('',views.spa_view),
    path('userprofile/',views.spa_view),
    re_path(r'^item\/\d',views.spa_view),
    path('post/',views.spa_view),
    
] 
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
