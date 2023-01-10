from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash 
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, PasswordChangeForm 
from .forms import CommentForm, NewUserForm, AboutForm, EmailForm, ContactForm 
from .models import Post, Category, Comment, User, StripeCustomer, Randomquote 
from django.contrib.auth.decorators import login_required 
from django.http import HttpResponseRedirect, HttpResponse 
from django.http.response import JsonResponse 
from django.contrib.sites.shortcuts import get_current_site 
from django.template.loader import render_to_string 
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError 
from .utils import generate_token
from django.urls import reverse
from django.core.mail import EmailMessage 
from django.conf import settings
from django.db.models.query_utils import Q 
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from hitcount.views import HitCountDetailView, HitCountMixin
from hitcount.utils import get_hitcount_model 
import stripe 
import random 

# Create your views here.

stripe.api_key=settings.STRIPE_SECRET_KEY


#this if for the list of posts on the home page not the feed 
class PostList(generic.ListView):

    template_name="index.html"
    paginate_by=3 

    def get_queryset(self):   

        #queryset for private posts and public posts as well lets get it 
        user=self.request.user 
        if user.is_authenticated and user.is_premium: 
            return Post.objects.filter(status=1).order_by("-created_on") 
        else: 
            return Post.objects.filter(category__is_public=True, status=1).order_by("-created_on")

#random 
#def random_quote(request): 
#    quotelist=list(Randomquote.objects.all()) 
#    randomquote=random.choice(quotelist) 
#    return HttpResponse(randomquote) 

#individual pages 
def about(request):
    return render(request, "about.html")

def categories(request):
    return render(request, "categories.html")

def contact(request):
    if request.method=="POST":
        form=ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("success_contact") 
    form=ContactForm()
    context={"form": form}
    return render(request, "contact.html", context)

def success_contact(request): 
    return render(request, "success_contact.html")

def future(request):
    return render(request, "future.html") 

def regsuccess(request):
    return render(request, "regsuccess.html") 

def social(request):
    return render(request, "social.html") 

def changemsuccess(request):
    return render(request, "profile/changemsuccess.html") 


#category page public
def category_page(request):
    #object_list=Category.objects.all()

    #display private categories if user is authenticated and premium 
    user=request.user  
    #print(user.is_authenticated)
    #print(user.is_premium) 
    if user.is_authenticated and user.is_premium: 
        object_list=Category.objects.all()  
    else: 
        object_list=Category.objects.all().filter(is_public=True)    

    context={"object_list": object_list,} 
    return render(request, "categories.html", context)


#send activation email 
def send_activation_email(user, request): 
    current_site=get_current_site(request)
    email_subject="Activate your account" 
    email_body=render_to_string("activate.html", {
        "user":user,
        "domain":current_site, 
        "uid":urlsafe_base64_encode(force_bytes(user.pk)),
        "token": generate_token.make_token(user)
        } 
        )

    email=EmailMessage(subject=email_subject, body=email_body, from_email=settings.EMAIL_FROM_USER, to=[user.email])  
    email.send() 


#activate user
def activate_user(request, uidb64, token): 

    try:
        uid=force_str(urlsafe_base64_decode(uidb64)) 
        user=User.objects.get(pk=uid) 

    except Exception as e: 
        user=None 

    if user and generate_token.check_token(user, token):
        user.is_email_verified=True 
        user.save()

        messages.success(request, "Email verified you can login")
        return redirect("login")

    return render(request, "activate-failed.html") 


#register request page 
def register_request(request):
    template_name="register.html" 

    if request.method=="POST": 
        form=NewUserForm(request.POST)

        if form.is_valid():
            user=form.save()
            send_activation_email(user, request) 

            #login(request, user) 
            messages.success(request, "Registration successful.") 
            return redirect("regsuccess")

        messages.error(request, "Unsuccesful registration, bad info.")
        return redirect("register") 

    form=NewUserForm()
    return render(request, template_name, context={"register_form":form}) 


#login request page 
def login_request(request): 
    template_name="login.html" 

    if request.method=="POST":
        form=AuthenticationForm(request, data=request.POST) 

        if form.is_valid():
            username=form.cleaned_data.get("username") 
            password=form.cleaned_data.get("password")
            user=authenticate(username=username, password=password)

            #check if email verified 
            if not user.is_email_verified:
                messages.error(request, "Email not verified check your inbox") 
                return redirect("login")  

            #check if user exists 
            if user is not None:
                login(request, user) 
                messages.success(request, f"You are now logged in as {username}.") 
                return redirect("home") 
            else:
                messages.error(request, "Invalid username or password.")

        else:
            messages.error(request, "Invalid username or password.")

    form=AuthenticationForm() 
    return render(request, template_name, context={"login_form":form})


#logout request
def logout_request(request):
    logout(request)
    messages.success(request, "You have succesfully logged out.") 
    return redirect("home") 


#view profile page for self 
def view_profile(request, username): 
    displayuser=User.objects.get(username=username)
    if displayuser==request.user:
        context="profile/view_profile_self.html"
    else: 
        context="profile/view_profile_other.html"

    return render(request, context, {
        "displayuser":displayuser
        },
        )   


#edit profile page 
@login_required 
def edit_profile(request, username): 
    user=User.objects.get(username=username) 
    if user==request.user:  
        return render(request, "profile/edit_profile.html", {
            "user":user,  
            },
            ) 
    else:
        return redirect("home") 


#change about
@login_required
def change_about(request):
    user=request.user  
    if request.method=="POST": 
        form=AboutForm(request.POST) 
        if form.is_valid():
            user.about=form.cleaned_data["about"] 
            user.save() 
            return redirect("view_profile", request.user)
    else:
        form=AboutForm()
    return render(request, "profile/change_about.html", 
            {"form": form}) 


#change email
@login_required
def change_email(request):
    user=request.user  
    if request.method=="POST": 
        form=EmailForm(request.POST) 
        if form.is_valid():
            user.email=form.cleaned_data["email"] 
            user.is_email_verified=False 
            user.save()
            send_activation_email(user, request) 
            logout(request) 
            return redirect("changemsuccess")
    else:
        form=EmailForm() 
    return render(request, "profile/change_email.html",
            {"form": form}) 


#change password
@login_required 
def change_password(request):
    if request.method=="POST":
        form=PasswordChangeForm(request.user, request.POST) 
        if form.is_valid():
            user=form.save() 
            update_session_auth_hash(request, user)
            messages.success(request, "Your password was succesfully updated!") 
            return redirect("home")
        else:
            messages.error(request, "Passwords do not match.")
    else:
        form=PasswordChangeForm(request.user)
    return render(request, "profile/change_password.html", 
            {"form": form}) 


#get premium 
@login_required
def get_premium(request):
    return render(request, "profile/get_premium.html")


#cancel premium first page 
@login_required
def cancel_premium(request):
    if request.user.is_premium:
        return render(request, "profile/cancel_premium.html")
    else:
        return redirect("home") 

#cancel premium confirm 
@login_required
def cancel_premium_confirm(request):
    if request.user.is_premium:
        return render(request, "profile/cancel_premium_confirm.html")
    else:
        return redirect("home") 

#cancel premium 
@login_required
def cancel(request):
    if request.user.is_authenticated:
        user=request.user
        user.is_premium=False
        user.save() 
        stripe_customer=StripeCustomer.objects.get(user=request.user)
        stripe_id=stripe_customer.stripeCustomerId
        sub_id=stripe.Subscription.retrieve(stripe_customer.stripeSubscriptionId)
        try:
            stripe.Subscription.delete(sub_id) 
            stripe.Customer.delete(stripe_id) 
            stripe_customer.delete()
            return redirect("cancel_premium_complete") 
        #Redirect to Thanks for the good times. 
        except Exception as e:
            return JsonResponse({"error": (e.args[0])}, status=403)
    else:
        return redirect("home") 

@login_required
def cancel_premium_complete(request):
    return render(request, "profile/cancel_premium_complete.html")


#new stripe config 
@csrf_exempt
def stripe_config(request):
    if request.method=="GET":
        stripe_config={"publicKey": settings.STRIPE_PUBLISHABLE_KEY} 
        return JsonResponse(stripe_config, safe=False) 


#checkout 
@csrf_exempt
@login_required
def checkout(request):
    if request.method=="GET":
        domain_url="https://www.masmakour.com/"
        try: 
            checkout_session=stripe.checkout.Session.create(
                    client_reference_id=request.user.id,
                    success_url=domain_url + "success_checkout/",
                    cancel_url=domain_url + "cancel_checkout/",
                    payment_method_types=["card"], 
                    mode="subscription", 
                    line_items=[
                        {
                            "price": settings.STRIPE_PRICE_ID, 
                            "quantity": 1, 
                            }
                        ]
                    )
            return JsonResponse({"sessionId": checkout_session["id"]})
        except Exception as e:
            return JsonResponse({"error": str(e)})


#success checkout
@login_required
def success_checkout(request):
    return render(request, "profile/success_checkout.html")

#cancel checkout 
@login_required 
def cancel_checkout(request):
    return render(request, "profile/cancel_checkout.html") 

#stripe webhook 
@csrf_exempt
def stripe_webhook(request):
    endpoint_secret=settings.STRIPE_ENDPOINT_SECRET
    payload=request.body
    sig_header=request.META["HTTP_STRIPE_SIGNATURE"]
    event=None

    try:
        event=stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as e:
        return HttpResponse(status=400)
    #except stripe.error.SignatureVerificationError as e:
    #    return HttpResponse(status=400)

    if event["type"]=="checkout.session.completed":
        session=event["data"]["object"] 

        client_reference_id=session.get("client_reference_id") 
        stripe_customer_id=session.get("customer")
        stripe_subscription_id=session.get("subscription") 

        if stripe_subscription_id is None: 
            print("donation") 

        else:

            user=User.objects.get(id=client_reference_id)

            StripeCustomer.objects.create(
                    user=user,
                    stripeCustomerId=stripe_customer_id,
                    stripeSubscriptionId=stripe_subscription_id, 
                    )

            print(user.username + " just subscribed.")
            user.is_premium=True
            user.save() 

    return HttpResponse(status=200) 


#donation page
def donate_request(request):
    return render(request, "donate_request.html") 


#donate
@csrf_exempt
def donate_checkout(request):
    if request.method=="GET":
        domain_url="https://www.masmakour.com/"
        try: 
            checkout_session=stripe.checkout.Session.create(
                    client_reference_id=request.user.id,
                    success_url=domain_url + "success_donate/",
                    cancel_url=domain_url + "cancel_donate/",
                    payment_method_types=["card"], 
                    mode="payment", 
                    line_items=[
                        {
                            "price": settings.STRIPE_PRICE_ID_DONATE, 
                            "quantity": 1, 
                            }
                        ]
                    )
            return JsonResponse({"sessionId": checkout_session["id"]})
        except Exception as e:
            return JsonResponse({"error": str(e)})


#success donate
def success_donate(request):
    return render(request, "success_donate.html")


#cancel donate
def cancel_donate(request):
    return render(request, "cancel_donate.html") 


#delete account 
@login_required
def delete_account(request): 
    return render(request, "profile/delete_account.html")


#delete account confirm 
@login_required
def delete_account_confirm(request): 
    return render(request, "profile/delete_account_confirm.html")


#delete account delete 
@login_required
def delete(request):
    if request.user.is_authenticated:
        user=request.user 
      

        try:
            if user.is_premium: 
                stripe_customer=StripeCustomer.objects.get(user=request.user)
                stripe_id=stripe_customer.stripeCustomerId
                sub_id=stripe.Subscription.retrieve(stripe_customer.stripeSubscriptionId) 
                stripe.Subscription.delete(sub_id) 
                stripe.Customer.delete(stripe_id) 
                stripe_customer.delete()
                user.delete()
            else:
                user.delete()
            return redirect("deletion_complete")  
        except Exception as e:
            return JsonResponse({"error": (e.args[0])}, status=403)
    else:
        return redirect("home")

#deletion complete 
def deletion_complete(request): 
    return render(request, "profile/deletion_complete.html")


#postdetail page (self warning due to function structure in class no big problem) 
#separate post detail and comment form
class PostDetail(HitCountDetailView):
    #@login_required

    def post_detail(request, slug):

        context = {} 
        
        #post object specific to check public and for hitcount  
        postobj=Post.objects.get(slug=slug) 
 
        #count hits
        hit_count = get_hitcount_model().objects.get_for_object(postobj)
        hits = hit_count.hits
        hitcontext = context['hitcount'] = {'pk': hit_count.pk}
        hit_count_response = HitCountMixin.hit_count(request, hit_count)
        if hit_count_response.hit_counted:
            hits = hits + 1
            hitcontext['hit_counted'] = hit_count_response.hit_counted
            hitcontext['hit_message'] = hit_count_response.hit_message
            hitcontext['total_hits'] = hits 

        #print(postobj) 
        #print(postobj.category.is_public)

        user=request.user 
        template_name="post_detail.html"
        #paginate, get page object
        post=get_object_or_404(Post, slug=slug) 
        #get parent comments 
        comments=post.comments.filter(active=True, parent__isnull=True).order_by("-created_on") 
        #get all comments for counter 
        commentcount=post.comments.filter(active=True).order_by("-created_on") 
        new_comment=None

        #print(post.slug) 

        if request.method=="POST": 
            comment_form=CommentForm(data=request.POST)
            if comment_form.is_valid():
                parent_obj=None 

                #get parent and allow replies 
                try:
                    parent_id=int(request.POST.get("parent_id")) 
                except:
                    parent_id=None 
                if parent_id: 
                    parent_obj=Comment.objects.get(id=parent_id)
                    if parent_obj:
                        reply_comment=comment_form.save(commit=False)
                        reply_comment.parent=parent_obj 

                #set user name
                comment_form.instance.user=request.user 
                #comment comment object no database add
                new_comment=comment_form.save(commit=False)
                #assigning current post to comment
                new_comment.post=post 
                #save comment to database
                new_comment.save()

                #redirect to clear form, without this it saves old comment 
                return redirect('post_detail', slug=post.slug) 
            #return absolue url 
                #eturn HttpResponseRedirect(request.path_info) 

        else:
            comment_form=CommentForm() 

        #based on premium acc and post category public restrict or allow access 
        if not bool(postobj.category.is_public): 
            if user.is_authenticated and user.is_premium: 
                return render(request, template_name, {
                    "post": post,
                    "comments": comments,
                    "commentcount": commentcount, 
                    "new_comment": new_comment,
                    "comment_form": comment_form,
                    },
                    )
            else:
                #blocked page for non premium redirect 
                return redirect("home")
        else: 
            return render(request, template_name, {
                "post": post,
                "comments": comments,
                "commentcount": commentcount, 
                "new_comment": new_comment,
                "comment_form": comment_form,
                },
                )

    #deleting comments 

    @login_required 
    def delete_comment(request, slug):

        post=get_object_or_404(Post, slug=slug)  
        comment_id=request.POST.get("comment_id")

        if request.method=="POST":
            comment=Comment.objects.get(id=comment_id) 
            try:
                #only allowed to delete own comment
                if(comment.user==request.user):
                    comment.delete()
                    messages.success(request, "Comment deleted succesfully.") 
            except:
                messages.error(request, "The comment could not be deleted.") 

        #comment_form.instance.user=request.user 

        return redirect(post.get_absolute_url()) 

#count hits 


#specific category page
def category_detail(request, slug): 

    catobj=Category.objects.get(slug=slug)
    user=request.user
    template_name="category_detail.html"
    category=get_object_or_404(Category, slug=slug) 


    if not bool(catobj.is_public): 
        if user.is_authenticated and user.is_premium: 
            return render(request, template_name, {
                "category": category,   
                },
                )
        else:
            #blocked page for non premium redirect 
                return redirect("home")
    else: 
        return render(request, template_name, {
            "category": category,
            },
            )

def page_not_found(request, exception):
    return render(request, "404.html", status=404)


