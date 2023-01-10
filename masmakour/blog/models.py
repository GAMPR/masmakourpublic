from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User, AbstractUser 
from django.conf import settings
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from hitcount.models import HitCountMixin, HitCount 


# Create your models here.

STATUS = (
        (0,"Draft"),
        (1,"Publish"),
        )

#random quote
class Randomquote(models.Model): 
    quote = models.CharField(max_length=255) 

    def __str__(self): 
        return self.quote 

#contact
class Contact(models.Model):
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()

    def __str__(self):
        return self.email


class Category(models.Model):

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    parent = models.ForeignKey('self', blank = True, null = True, related_name = 'children', on_delete = models.CASCADE)
    #for premium, if false then premium is needed to see 
    is_public = models.BooleanField(default = True) 

    class Meta: 
        #enforcing that there can't be two categories under a parent with the same slug 
        #__str__ method elaborated later in post. use __unicode in place of __str__ if using python 2 
        unique_together = ('slug', 'parent',) 
        verbose_name_plural = "categories"

    def __str__(self):
        full_path = [self.name]
        p = self.parent 

        while p is not None:
            full_path.append(p.name)
            p = p.parent 
        return ' -> '.join(full_path[::-1]) 



class Post(models.Model):

    title = models.CharField(max_length = 200, unique = True)
    slug = models.SlugField(max_length = 200, unique = True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name = 'blog_posts') 
    category = models.ForeignKey(Category, null = False, blank = True, on_delete = models.CASCADE)
    content = models.TextField() 
    status = models.IntegerField(choices = STATUS, default = 0) 
    created_on = models.DateTimeField(auto_now_add = True) 
    updated_on = models.DateTimeField(auto_now = True) 

    hit_count_generic = GenericRelation(
            HitCount, object_id_field='object_pk',
            related_query_name='hit_count_generic_relation'
            ) 
    

    def current_hit_count(self):
       return self.hit_count.hits 

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title 

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"slug": str(self.slug)})




class Comment(models.Model):

    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name = 'comments') 
    user = models.ForeignKey(settings.AUTH_USER_MODEL, editable = False, on_delete = models.CASCADE) 
    body = models.TextField() 
    created_on = models.DateTimeField(auto_now_add = True) 
    active = models.BooleanField(default = True) 
    #parent for replie
    parent = models.ForeignKey('self', on_delete = models.CASCADE, null = True, blank = True, related_name = 'replies',) 

    #email = models.EmailField()
    #^ old without user models

    class Meta:
        ordering = ['created_on'] 

    def __str__(self): 
        return 'Comment {} by {}'.format(self.body, self.user)



class User(AbstractUser):

    is_email_verified = models.BooleanField(default = False) 
    is_premium = models.BooleanField(default = False)
    about = models.TextField(max_length = 300)
    email = models.EmailField(unique = True) 

    def __str__(self):
        return self.username 

#stripe customers

class StripeCustomer(models.Model): 
    user = models.OneToOneField(to = settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    stripeCustomerId = models.CharField(max_length = 255) 
    stripeSubscriptionId = models.CharField(max_length = 255) 

    def __str__(self):
        return self.user.username 

