from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView, View
from django.urls import reverse_lazy


from .forms import CreateBlogForm
from .models import Blog
    
    
def create_blog(request):
    create_blog_form = CreateBlogForm(request.POST or None, files=request.FILES)
    if create_blog_form.is_valid():
        create_blog_form.instance.author = request.user
        create_blog_form.save()
        return redirect('blogs:blog_list')
    return render(
        request, 'blog/create_blog.html', context={
            'create_blog_form': create_blog_form
        }
    )
    
    
class BlogListView(View):

    def get(self, request, *args, **kwargs):
        user = request.user
        number_of_following_user = user.connection.all().count()
        number_of_followed_user = user.connected_users.all().count()
        number_of_blog_post = Blog.objects.filter(author=user).all().count()
        return render(request, 'blog/blog_list.html', {
            'number_of_following_user': number_of_following_user,
            'number_of_followed_user': number_of_followed_user,
            'number_of_blog_post': number_of_blog_post,
            })
        
        
class BlogDetailView(DetailView):
    template_name = 'blog/blog_detail.html'
    model = Blog
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object.author
        context['number_of_following_user'] = user.connection.all().count()
        context['number_of_followed_user'] = user.connected_users.all().count()
        context['number_of_blog_post'] = Blog.objects.filter(author=user).all().count()
        return context
    
    