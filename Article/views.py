from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import CreateView, UpdateView, ListView, DetailView, View, TemplateView, DeleteView
from Article.models import Article_model, Comment, Likes
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from Article.forms import CommentForm
import uuid
from django.utils.text import slugify


# Create your views here.
class MyArticles(LoginRequiredMixin, TemplateView):
    context_object_name = 'article'
    template_name = 'Article/my_articles.html'


class article_list(ListView):
    context_object_name = 'Articles'
    model = Article_model
    template_name = 'Article/article_list.html'

# def article_list(request):
#     return render(request, 'Article/article_list.html', context={})


class CreateArticle(LoginRequiredMixin, CreateView):
    context_object_name = 'article'
    model = Article_model
    template_name = 'Article/create_article.html'
    fields = ('article_title', 'article_content', 'article_image')

    def form_valid(self, form):
        article_obj = form.save(commit=False)
        article_obj.author = self.request.user
        title = article_obj.article_title
        article_obj.slug = slugify(title+'-' + str(uuid.uuid4()))
        article_obj.save()
        return HttpResponseRedirect(reverse('index'))


class ArticleList(ListView):
    context_object_name = 'article'
    model = Article_model
    template_name = 'Article/article_list.html'


@login_required
def article_details(request, slug):
    article = Article_model.objects.get(slug=slug)
    comment_form = CommentForm()
    already_liked = Likes.objects.filter(article=article, user=request.user)
    if already_liked:
        liked = True
    else:
        liked = False

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.article = article
            comment.save()
            return HttpResponseRedirect(reverse('Article:article_details', kwargs={'slug': slug}))
    return render(request, 'Article/article_details.html', context={'article': article, 'comment_form': comment_form, 'liked': liked, })


@login_required
def liked(request, pk):
    article = Article_model.objects.get(pk=pk)
    user = request.user
    already_liked = Likes.objects.filter(article=article, user=user)
    if not already_liked:
        liked_post = Likes(article=article, user=user)
        liked_post.save()
    return HttpResponseRedirect(reverse('Article:article_details', kwargs={'slug': article.slug}))


@login_required
def unliked(request, pk):
    article = Article_model.objects.get(pk=pk)
    user = request.user
    already_liked = Likes.objects.filter(article=article, user=user)
    already_liked.delete()
    return HttpResponseRedirect(reverse('Article:article_details', kwargs={'slug': article.slug}))


class UpdateArticle(LoginRequiredMixin, UpdateView):
    context_object_name = 'article'
    model = Article_model
    fields = ('article_title', 'article_content', 'article_image')
    template_name = 'Article/edit_article.html'

    def get_success_url(self, **kwargs):
        return reverse_lazy('Article:article_details', kwargs={'slug': self.object.slug})
