from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django.urls import reverse
from django.views.generic.edit import CreateView
from .models import Post, Comment
from django.views import View
from .forms import CommentForm

# Create your views here.


# def index(request):
#     last_3_posts = Post.objects.all().order_by("-date")[:3]
#     return render(request, "blog/index.html", {
#         "last_3_posts" : last_3_posts
#     })

class IndexView(ListView):
    template_name = "blog/index.html"
    model = Post
    ordering = ["-date"]
    context_object_name = 'last_3_posts'

    def get_queryset(self):
        base_query = super().get_queryset()
        data = base_query[:3]
        return data


# def posts(request):
#     try:
#         # return render(request, "blog/all_posts.html", {
#         #     "posts" : list(Post.objects.all())
#         # })
#
#         all_posts = Post.objects.all().order_by("-date")
#         return render(request, "blog/all_posts.html", {
#             "posts" : all_posts,
#         })
#     except:
#         raise Http404()

class PostsView(ListView):
    template_name = "blog/all_posts.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "posts"


# def post_detail(request, slug):
#
#     # for post in all_posts:
#     #     if slug == post['slug']:
#     #         spc_post = post
#
#     # spc_post = next(post for post in list(Post.objects.all()) if slug == post.slug)
#
#     spc_post = get_object_or_404(Post, slug=slug)
#
#     return render(request, "blog/post_detail.html", {
#         "post": spc_post,
#         "post_tags": spc_post.tags.all()
#     })


# class PostDetailView(DetailView):
#     template_name = "blog/post_detail.html"
#     model = Post
#
#     def get_context_data(self, **kwargs):
#         post_contexts = super().get_context_data()
#         post_contexts['post_tags'] = self.object.tags.all()
#         post_contexts['comment_form'] = CommentForm()
#         return post_contexts


class PostDetailView(View):
    def is_stored_post(self, request, post):
        stored_posts = request.session.get("stored_posts")
        if stored_posts is not None:
            return post.id in stored_posts
        return False

    def get(self, request, slug):
        # all_posts = Post.objects.all()
        # post = None
        # for post in all_posts:
        #     if post.slug == slug:
        #         post = post

        # post = next(post for post in all_posts if post.slug == slug)

        # post = get_object_or_404(Post, slug=slug)

        post = Post.objects.get(slug=slug)
        context = {
            "post": post,
            "post_tags": post.tags.all(),
            "comment_form": CommentForm(),
            "comments": post.comments.all().order_by('-id'),
            "is_in_session": self.is_stored_post(request, post)
        }
        return render(request, "blog/post_detail.html", context)

    def post(self, request, slug):
        comment_form = CommentForm(request.POST)
        post = Post.objects.get(slug=slug)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse("post-detail-page", args=[slug]))

        context = {
            "post": post,
            "post_tags": post.tags.all(),
            "comment_form": comment_form,
            "comments": post.comments.all().order_by('-id'),
            "is_in_session": self.is_stored_post(request, post)
        }
        return render(request, "blog/post_detail.html", context)


class ReadLaterView(View):
    def get(self, request):
        stored_posts = request.session.get("stored_posts")
        context = {}
        if stored_posts is None or len(stored_posts) == 0:
            context["posts"] = []
            context["has_posts"] = False
        else:
            posts = Post.objects.filter(id__in=stored_posts)
            context["posts"] = posts
            context["has_posts"] = True

        return render(request, "blog/stored_posts.html", context)


    def post(self, request):
        stored_posts = request.session.get("stored_posts")

        if stored_posts is None:
            stored_posts = []

        post_id = int(request.POST["post_id"])
        if post_id not in stored_posts:
            stored_posts.append(post_id)
        else:
            stored_posts.remove(post_id)

        request.session["stored_posts"] = stored_posts

        return HttpResponseRedirect("/")