from . import views
from django.contrib.auth import views as auth_views 
from django.urls import path
#feed
from .feeds import LatestPostsFeed

urlpatterns = [
        path('', views.PostList.as_view(), name = 'home'),
        #random quote 
        #path('random/', views.random_quote, name='random'), 
        path('about/', views.about, name = 'about'),
        path('categories/', views.category_page, name = 'categories'),
        path('contact/', views.contact, name = 'contact'),
        path('success_contact/', views.success_contact, name='success_contact'), 
        path('social/', views.social, name = 'social'), 
        path('future/', views.future, name = 'future'),
        path('register/', views.register_request, name = 'register'),
        path('login/', views.login_request, name = 'login'), 
        path('logout/', views.logout_request, name = 'logout'),
        path('regsuccess/', views.regsuccess, name = 'regsuccess'),
        path('activate-user/<slug:uidb64>/<slug:token>', views.activate_user, name = 'activate'),

        #view profile 
        path('view_profile/<slug:username>', views.view_profile, name = 'view_profile'), 
        path('edit_profile/<slug:username>', views.edit_profile, name = 'edit_profile'),  
        path('change_password/', views.change_password, name = 'change_password'),
        path('change_email/', views.change_email, name = 'change_email'),
        path('changemsuccess/', views.changemsuccess, name = 'changemsuccess'), 
        path('change_about/', views.change_about, name = 'change_about'), 
        path('get_premium/', views.get_premium, name = 'get_premium'),
        path('delete_account/', views.delete_account, name = 'delete_account'),
        path('delete_account_confirm/', views.delete_account_confirm, name = 'delete_account_confirm'),
        path('delete/', views.delete, name = 'delete'),
        path('deletion_complete', views.deletion_complete, name='deletion_complete'), 

        #premium
        path('config/', views.stripe_config), 
        path('get_premium/', views.get_premium, name = 'get_premium'),
        #these two are forms leading to the actual cancelation 
        path('cancel_premium/', views.cancel_premium, name = 'cancel_premium'),
        path('cancel_premium_confirm/', views.cancel_premium_confirm, name = 'cancel_premium_confirm'),  
        path('cancel_premium_complete/', views.cancel_premium_complete, name = 'cancel_premium_complete'),   
        #this cancel actually cancels
        path('cancel/', views.cancel, name = 'cancel'), 
        path('checkout/', views.checkout, name = 'checkout'),
        path('success_checkout/', views.success_checkout, name = 'success_checkout'), 
        path('cancel_checkout/', views.cancel_checkout, name = 'cancel_checkout'), 
        path('webhook/', views.stripe_webhook), 

        #donate
        path('donate_request/', views.donate_request, name = 'donate_request'),
        path('donate_checkout/', views.donate_checkout, name = 'donate_checkout'),
        path('success_donate/', views.success_donate, name = 'success_donate'), 
        path('cancel_donate/', views.cancel_donate, name = 'cancel_donate'),
 
        #reset password
        path('reset_password/', auth_views.PasswordResetView.as_view(template_name = 'resetpass/reset_password.html'), name = 'reset_password'), 
        path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name = 'resetpass/password_reset_done.html'), name = 'password_reset_done'),
        path('password_reset_confirm/<slug:uidb64>/<slug:token>/', auth_views.PasswordResetConfirmView.as_view(template_name = 'resetpass/password_reset_confirm.html'), name = 'password_reset_confirm'),
        path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name = 'resetpass/password_reset_complete.html'), name = 'password_reset_complete'), 

        #ORDER URL PATTERNS MATTERS, PUT CONCRETE PAGES FIRST, THEN SLUGS
        #path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
        #path('category/<str:cats>/', views.CategoryView, name='category'),
        #bad ones^
        path('delete_comment/<slug:slug>', views.PostDetail.delete_comment, name = 'delete_comment'), 
        path('posts/<slug:slug>/', views.PostDetail.post_detail, name = 'post_detail'),
        path('categories/<slug:slug>/', views.category_detail, name = 'category_detail'), 
        #path(r'^category/(?P<hierarchy>.+)/$', views.show_category, name='category'),
        #rss feed 
        path('feed/rss', LatestPostsFeed(), name = 'post_feed'),
        
        ]


