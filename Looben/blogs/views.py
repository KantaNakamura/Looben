from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404 

from .forms import CreateBlogForm, EditBlogPostForm
from .models import Blog
from accounts.models import FollowForUser
from accounts import contribution_calculation
from notifications.models import Notification
from chat.models import ConversationPartner


class CheckForUserMatchMixin(LoginRequiredMixin, UserPassesTestMixin):
    
    def test_func(self):
        target_blog_post = get_object_or_404(Blog, pk=self.kwargs['pk'])
        return self.request.user == target_blog_post.author
        
    def handle_no_permission(self):
        return JsonResponse(
            {'message': 'Only user who made this author have access to this view'}
        )
        

@login_required
def create_blog(request):
    create_blog_form = CreateBlogForm(request.POST or None)
    if create_blog_form.is_valid():
        create_blog_form.instance.author = request.user
        create_blog_form.save()
        contribution_calculation.for_creating_post(author=request.user)
        # フォロワーへのブログ記事作成の通知を作成
        for follow in FollowForUser.objects.filter(followed_user=request.user).all():
            create_blog_notification = Notification(sender=request.user, receiver=follow.user, message= str(request.user.username) + 'が新しくブログ記事を投稿しました。')
            create_blog_notification.save()
        return redirect('blogs:blog_list')
    notification_lists =  Notification.objects.filter(receiver=request.user).order_by('timestamp').reverse()[:3]
    number_of_notification =  Notification.objects.filter(receiver=request.user).count()
    has_notifications =  Notification.objects.filter(receiver=request.user).exists()
    has_not_seen_message = ConversationPartner.objects.filter(current_user=request.user, have_new_message=True).exists()
    return render(
        request, 'blog/create_blog.html', context={
            'create_blog_form': create_blog_form,
            'notification_lists': notification_lists,
            'number_of_notification': number_of_notification,
            'has_notifications': has_notifications,
            'has_not_seen_message': has_not_seen_message
        }
    )
    
    
class DeletePostView(CheckForUserMatchMixin, DeleteView):
    template_name = 'blog/delete_post.html'
    model = Blog
    
    def get_success_url(self):
        return reverse_lazy('dashboard:post_in_dashboard', kwargs={'username': self.object.author.username}) 
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['notification_lists'] =  Notification.objects.filter(receiver=self.request.user).order_by('timestamp').reverse()[:3]
        context['number_of_notification'] =  Notification.objects.filter(receiver=self.request.user).count()
        context['has_notifications'] =  Notification.objects.filter(receiver=self.request.user).exists()
        context['has_not_seen_message'] = ConversationPartner.objects.filter(current_user=self.request.user, have_new_message=True).exists()
        return context
    

class EditBlogPostView(CheckForUserMatchMixin, UpdateView):
    template_name = 'blog/edit_blog_post.html'
    form_class = EditBlogPostForm
    model = Blog
    
    def get_success_url(self):
        return reverse_lazy('dashboard:post_in_dashboard', kwargs={'username': self.object.author.username}) 
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['notification_lists'] =  Notification.objects.filter(receiver=self.request.user).order_by('timestamp').reverse()[:3]
        context['number_of_notification'] =  Notification.objects.filter(receiver=self.request.user).count()
        context['has_notifications'] =  Notification.objects.filter(receiver=self.request.user).exists()
        context['has_not_seen_message'] = ConversationPartner.objects.filter(current_user=self.request.user, have_new_message=True).exists()
        return context
    
    
class BlogListView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        user = request.user
        number_of_following_user = FollowForUser.objects.filter(user=user).count()
        number_of_followed_user = FollowForUser.objects.filter(followed_user=user).count()
        number_of_blog_post = Blog.objects.filter(author=user).count()
        newest_blog_posts = Blog.objects.order_by('-created_at')[:6]
        notification_lists =  Notification.objects.filter(receiver=user).order_by('timestamp').reverse()[:3]
        number_of_notification =  Notification.objects.filter(receiver=user).count()
        has_notifications =  Notification.objects.filter(receiver=user).exists()
        has_not_seen_message = ConversationPartner.objects.filter(current_user=request.user, have_new_message=True).exists()
        if 'search' in self.request.GET:
            keyword_query = request.GET.get('search')
            if keyword_query == '':
                searched_blogs = []
                number_of_searched_blogs = 0
                user_searched_something = False
            else:
                blogs = list(Blog.objects.all())
                searched_blogs = []
                for blog in blogs:
                    if keyword_query in blog.meta_description:
                        searched_blogs.append(blog)
                number_of_searched_blogs = len(searched_blogs)
                user_searched_something = True
        else:
            searched_blogs = []
            number_of_searched_blogs = 0
            user_searched_something = False
        return render(request, 'blog/blog_list.html', {
            'number_of_following_user': number_of_following_user,
            'number_of_followed_user': number_of_followed_user,
            'number_of_blog_post': number_of_blog_post,
            'newest_blog_posts': newest_blog_posts,
            'number_of_searched_blogs': number_of_searched_blogs,
            'user_searched_something': user_searched_something,
            'searched_blogs': searched_blogs,
            'notification_lists': notification_lists,
            'number_of_notification': number_of_notification,
            'has_notifications': has_notifications,
            'has_not_seen_message': has_not_seen_message
            })
    
    
class InOrderBlogListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        blog_posts_order_by_date = Blog.objects.order_by('-created_at')[:20]
        official_blog_post_lists = Blog.objects.filter(is_official=True)[:20]
        notification_lists =  Notification.objects.filter(receiver=request.user).order_by('timestamp').reverse()[:3]
        number_of_notification =  Notification.objects.filter(receiver=request.user).count()
        has_notifications =  Notification.objects.filter(receiver=request.user).exists()
        has_not_seen_message = ConversationPartner.objects.filter(current_user=request.user, have_new_message=True).exists()
        return render(request, 'blog/in_order_blog_post.html', {
            'blog_posts_order_by_date': blog_posts_order_by_date,
            'official_blog_post_lists': official_blog_post_lists,
            'notification_lists': notification_lists,
            'number_of_notification': number_of_notification,
            'has_notifications': has_notifications,
            'has_not_seen_message': has_not_seen_message
            })
        