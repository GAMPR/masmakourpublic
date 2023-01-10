from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django_summernote.admin import SummernoteModelAdmin
from .models import Post, Category, Comment, User, StripeCustomer, Contact, Randomquote 
# Register your models here.

#old postadmin with no summernote 
#class PostAdmin(admin.ModelAdmin):
#    list_display = ('title','slug','status','created_on')
#    list_filter = ("status",)
#    search_fields = ['title', 'content']
#    prepopulated_fields = {'slug': ('title',)}

#for users 
class MyUserAdmin(UserAdmin):
    model = User 
    fieldsets = UserAdmin.fieldsets + ((None, {'fields': ('is_email_verified', 'is_premium', 'about')}),
            )

#for posts 
class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',) 

#@admin.register(Comment)
#for comments
class CommentAdmin(admin.ModelAdmin): 
    readonly_fields = ('user',) 
    list_display = ('body', 'post', 'created_on', 'active') 
    list_filter = ('active', 'created_on')
    search_fields = ('name', 'body') 
    actions = ['approve_comments'] 

    def approve_comments(self, request, queryset): 
        queryset.update(active = True) 

admin.site.register(Comment, CommentAdmin) 
admin.site.register(Post, PostAdmin) 
admin.site.register(Category) 
admin.site.register(User, MyUserAdmin)
admin.site.register(StripeCustomer)
admin.site.register(Contact)
admin.site.register(Randomquote) 
