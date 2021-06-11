from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import CreateView, UpdateView, ListView, DetailView, View, TemplateView, DeleteView
from ForumApp.models import Forum, CommentForum
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from ForumApp.forms import CommentForm
import uuid
from django.utils.text import slugify
# Create your views here.


class CreateForum(LoginRequiredMixin, CreateView):
    context_object_name = 'forum'
    model = Forum
    template_name = 'ForumApp/create_forum.html'
    fields = ('forum_title', 'forum_content', 'forum_image')

    def form_valid(self, form):
        forum_obj = form.save(commit=False)
        forum_obj.author = self.request.user
        title = forum_obj.forum_title
        forum_obj.slug = slugify(title+'-' + str(uuid.uuid4()))
        forum_obj.save()
        return HttpResponseRedirect(reverse('index'))


class ForumList(ListView):
    context_object_name = 'Forum'
    model = Forum
    template_name = 'ForumApp/forum_list.html'


class MyProblems(LoginRequiredMixin, TemplateView):
    context_object_name = 'Forum'
    template_name = 'ForumApp/my_problems.html'


@login_required
def forum_details(request, slug):
    forum = Forum.objects.get(slug=slug)
    comment_form = CommentForm()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.forum = forum
            comment.save()
            return HttpResponseRedirect(reverse('ForumApp:forum_details', kwargs={'slug': slug}))
    return render(request, 'ForumApp/forum_details.html', context={'forum': forum, 'comment_form': comment_form})


class UpdateForum(LoginRequiredMixin, UpdateView):
    context_object_name = 'Forum'
    model = Forum
    fields = ('forum_title', 'forum_content', 'forum_image')
    template_name = 'ForumApp/edit_forum.html'

    def get_success_url(self, **kwargs):
        return reverse_lazy('ForumApp:forum_details', kwargs={'slug': self.object.slug})
