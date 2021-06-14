import json
import os
from django.shortcuts import render
from django.utils import timezone
from .models import Post
from .forms import PostForm
from django.shortcuts import redirect

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        print ("Calling brownie script")
        currentdir = os.getcwd()
        print(currentdir)
        os.chdir("C:/Users/mihir2/djangogirls/nft-mix")
        os.system("brownie run scripts/simple_collectible/deploy_create.py --network rinkeby")
        print ("executed brwonie script")
        os.chdir(currentdir)
        f = open('C:/Users/mihir2/djangogirls/nft-mix/metadata/temp.json')
        dict = json.load(f)
        if form.is_valid():
            #handle_uploaded_file(request.FILES['file'])
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.ipfspath = dict["image"]
            post.openseaurl = dict["openseaurl"]
            print(post.ipfspath)
            post.save()
            return redirect('post_list')
    else:        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def handle_uploaded_file(f):
    with open('myimage', 'wb+') as detination:
        for chunk in f.chunks():
            destination.write(chunk)

# Create your views here.
