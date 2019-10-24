from django.shortcuts import render,redirect,get_object_or_404
from .forms import PostForm,CommentForm
from .models import HashTag,Post,Comment
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
# Create your views here.
def index(req):
    posts = Post.objects.all()

    paginator = Paginator(posts,5)
    
    page = req.GET.get('page')
    posts = paginator.get_page(page)
    
    form = CommentForm()
    context ={
        'posts':posts,
        'form':form,
    }
    return render(req, 'posts/index.html',context)

def create(req):    
    if not req.user.is_authenticated:
        return redirect('accounts:login')
    if req.method =='POST':
        form = PostForm(req.POST,req.FILES) #이미지에 파일을 업로드!
        if form.is_valid():
            post = form.save(commit=False)
            post.user = req.user
            post.save()
            for word in post.content.split():
                if word.startswith("#"):
                    #hashtag 추가
                    hashtag = HashTag.objects.get_or_create(content=word)[0] #content에다가 워드를 추가해줌 get_or_create:워드에 해당하는 컨텐츠가 있으면 가져오고 없으면 새로 생성 중복방지
                    #(obj,True or False) 생성이 되면 True get으로 가져오면 False를 반환, 반환되는 obj만 가져오기 위해서 [0] 0번째 인덱스 추가
                    post.hashtags.add(hashtag)

            return redirect('posts:index')
    else:
        form = PostForm()
    context ={
        'form':form
    }

    return render(req, 'posts/form.html',context)

def hashtags(req,id):
    hashtag = get_object_or_404(HashTag,id=id)

    posts = hashtag.taged_post.all()
    comments = hashtag.taged_comment.all()
    form = CommentForm()
    context = {
        'posts':posts,
        'comments':comments,
        'form':form
    }
    return render(req, 'posts/index.html',context)


@login_required
def like_post(req,id):
  
    post = get_object_or_404(Post, id=id)
    user = req.user
    if user in post.like_users.all():
        post.like_users.remove(user)
    else:
        post.like_users.add(user)

    return redirect('posts:index')

def comment_create(req,id):
    if not req.user.is_authenticated:
        return redirect('accounts:login')
    post = get_object_or_404(Post, id=id)

    user = req.user
    if req.method == "POST":
        form = CommentForm(req.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = user
            comment.save()
            for word in comment.content.split():
                if word.startswith("#"):
                    #hashtag 추가
                    hashtag = HashTag.objects.get_or_create(content=word)[0]
                    comment.hashtags.add(hashtag)

            return redirect('posts:index')
    else:
        form = CommentForm()
    context = {
        'form':form
    }
    return render(req,'posts/index.html',context)


def like_comments(req,post_id,comment_id):
    if not req.user.is_authenticated:
        return redirect('accounts:login')
    comment = get_object_or_404(Comment, id=comment_id)
    user= req.user
    if user in comment.like_users.all():
        comment.like_users.remove(user)
    else:
        comment.like_users.add(user)
    return redirect('posts:index')

def delete(req,id):
    if not req.user.is_authenticated:
        return redirect('accounts:login')
    post = get_object_or_404(Post,id=id)
    if req.user == post.user:
        post.delete()
    else:
        pass
    return redirect('posts:index')


def update(req,id):
    if not req.user.is_authenticated:
        return redirect('accounts:login')
        
    post = get_object_or_404(Post,id=id)

    if req.user == post.user:

        if req.method == "POST":
            form = PostForm(req.POST, instance=post)
            if form.is_valid():
                p = form.save()
                p.hashtags.clear()
                for word in post.content.split():
                    if word.startswith("#"):
                        #hashtag 추가
                        hashtag = HashTag.objects.get_or_create(content=word)[0] #content에다가 워드를 추가해줌 get_or_create:워드에 해당하는 컨텐츠가 있으면 가져오고 없으면 새로 생성 중복방지
                        #(obj,True or False) 생성이 되면 True get으로 가져오면 False를 반환, 반환되는 obj만 가져오기 위해서 [0] 0번째 인덱스 추가
                        post.hashtags.add(hashtag)

                return redirect('posts:index')
        else:
            form = PostForm(instance=post)

        context = {
            'form':form
        }
        return render(req,'posts/form.html',context)
    else:
        return redirect('posts:index')


