from lzma import FORMAT_AUTO
from urllib import request
from django.contrib.auth.models import User
from django.views.generic import DetailView, View, FormView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseBadRequest, JsonResponse

from feed.models import Post
from followers.models import Follower
from profiles.models import Profile
from profiles.forms import PostFrom


class ProfileDetailView(DetailView):
    http_method_names = ["get"]
    template_name = "profiles/detail.html"
    model = User
    context_object_name = "user"
    slug_field = "username"
    slug_url_kwarg = "username"

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        return super().dispatch(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        user = self.get_object()
        context = super().get_context_data(**kwargs)
        context['total_posts'] = Post.objects.filter(author=user).count()
        context['total_followers'] = Follower.objects.filter(following=user).count();
        if self.request.user.is_authenticated:
            context['you_follow'] = Follower.objects.filter(following=user,followed_by=self.request.user).exists()
        return context


class FollowView(LoginRequiredMixin,View):
    http_method_names = ["post"]
    # template_name = "profiles/detail.html"
    # model = User
    # context_object_name = "user"
    def post(self, request, *args,**kwargs):
        data = request.POST.dict()
        if "action" not in data or "username" not in data:
            return HttpResponseBadRequest("Missing Data")
        try:
            other_user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            return HttpResponseBadRequest("Missing Data")
        
        if data['action'] == 'follow':
            follower, created = Follower.objects.get_or_create(
                followed_by= request.user,
                following = other_user
            )
        else:
            try:
                follower = Follower.objects.get(
                    followed_by= request.user,
                    following = other_user
                )
            except Follower.DoesNotExist:
                follower = None
            if Follower:
                follower.delete()

        return JsonResponse({
            'success': True,
            'wording':"Unfollow" if data['action'] == "follow" else "Follow"
        })


class EditProfileView(LoginRequiredMixin,FormView):
    template_name = "profiles/editprofile.html"
    form_class = PostFrom
    success_url = "/"

    def dispatch(self, request, *args, **kwargs):
        self.request = request 
        return super().dispatch(request, *args, **kwargs)


    def form_valid(self,form):
        #create new Post
        if form.cleaned_data['text']:
            print(form.cleaned_data['text'])
            user = User.objects.get(username = self.request.user.username)
            user.username = form.cleaned_data['text']
            user.save()
        if form.cleaned_data['image']:
            obj = Profile.objects.get(user=self.request.user.id)
            obj.image = form.cleaned_data['image']
            obj.save()
    

        return super().form_valid(form)