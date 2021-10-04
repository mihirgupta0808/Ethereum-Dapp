import json
from django.shortcuts import render
from django.utils import timezone
from .models import Post
#from .models import User
from django.contrib.auth.models import User
from .forms import PostForm
from .forms import ApproveForm
from django.shortcuts import redirect
from django.core.files.storage import FileSystemStorage
from pathlib import Path
import requests
from . import sample_metadata
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
#from .forms import SignUpForm
#from simple_decorators.apps.blog.models import Entry
#from simple_decorators.apps.blog.forms import EntryForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q
from django.http import HttpResponse
from notifications.signals import notify

import os, sys
import subprocess
import tempfile

@login_required
def post_list(request):
    if request.user.is_superuser:
        posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date').filter(is_approved=True)
    else:
        posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date').filter(
            is_approved=True).filter(author=request.user)

    #posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def upload_to_ipfs(filepath):
    PINATA_BASE_URL = 'https://api.pinata.cloud/'
    endpoint = 'pinning/pinFileToIPFS'
    # Change this to upload a different file
    #filepath = './img/pug.png'
    #filepath = fpath
    filename = filepath.split('/')[-1:][0]
    headers = {'pinata_api_key': 'd2983ade6a3c5114e663',
            'pinata_secret_api_key': 'cf9ce308202e972da08a69345ff0ee4dbd2c167743f122fe8b1fcdec0be2e61f'}


    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        response = requests.post(PINATA_BASE_URL + endpoint,
                                files={"file": (filename, image_binary)},
                                headers=headers)
        ipfs_hash = response.json()['IpfsHash']
        print(response.json())

    image_uri = "https://ipfs.io/ipfs/{}?filename={}".format(
                ipfs_hash, filename)
    print(image_uri)




    return image_uri

def write_tempjason(imgipfs,ptitle,ptext):

    collectible_metadata = sample_metadata.metadata_template
    metadata_file_name = "contract.json"

    print("Creating Metadata file: " + metadata_file_name)
    collectible_metadata["name"] = ptitle
    collectible_metadata["description"] = ptext
         #   image_to_upload = None
         #   if os.getenv("UPLOAD_IPFS") == "true":
         #       image_path = "./img/{}.png".format(
          #          breed.lower().replace('_', '-'))
          #      image_to_upload = upload_to_ipfs(image_path)
        #    image_to_upload = (
         #       breed_to_image_uri[breed] if not image_to_upload else image_to_upload
         #   )
    collectible_metadata["image"] = imgipfs


    with open(metadata_file_name, "w+") as file:
        json.dump(collectible_metadata, file)
         #   if os.getenv("UPLOAD_IPFS") == "true":
          #      upload_to_ipfs(metadata_file_name)


@login_required
def post_new(request):
    print("File values in file dictionary:", request.FILES)
    if request.method == "POST" and request.FILES['nftimagefile']:
        uploaded_nft_file = request.FILES['nftimagefile']
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            print("hi")
            print("form validated")
            post = form.save(commit=False)

        fs = FileSystemStorage()
        uploaded_file_name = fs.save(uploaded_nft_file.name, uploaded_nft_file)
        ptitle = request.POST['title']
        ptext = request.POST['text']
        print("image name is")
        print(uploaded_file_name)
        currentdir = os.getcwd()
        #imgpath = os.path.join(currentdir, uploaded_file_name)

        #print(imgpath)
        imageipfs = upload_to_ipfs(uploaded_file_name)

        """
        write_tempjason(imageipfs,ptitle,ptext)
        #print(imageipfs)
        os.chdir('~/temp/nft-mix')
        #os.system('brownie run scripts/simple_collectible/deploy_create.py --network rinkeby')
        os.chdir(currentdir)

        f = open('nft-mix/metadata/temp.json')
        dict = json.load(f)

        """
        post.author = request.user
        post.created_date = timezone.now()
        #post.published_date = timezone.now()
        # post.ipfspath = dict["image"]
        post.ipfspath = imageipfs
        #post.openseaurl = dict["openseaurl"]
        print(post.ipfspath)

        post.save()

        record_number = post.pk

        subject = "New NFT Approval Request"
        body = ( "NFT Title    - " + str(ptitle) + "\n"
                 + "NFT Description    - " + str(ptext) + "\n"
                 + "NFT Author    - " + str(post.author) + "\n"
                 + "NFT FileName    - " + str(uploaded_file_name) + "\n"
                 + "NFT Record Number    - " +  str(record_number) + "\n"
                 + "NFT IPFS path    - " +  str(imageipfs) + "\n"
                 )

        #message = "\n".join(body.values())



        #messages.success(request, subject+body)
        superusers = User.objects.filter(is_superuser=True)
        messagedesc = subject + "NFT Record Number - " +  str(record_number) + "\n"

        notify.send(request.user, recipient=superusers, actor=request.user, verb='Message', description=messagedesc)

        return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


@user_passes_test(lambda u: u.is_superuser)
def post_approve(request):
    #print("File values in file dictionary:", request.FILES)
    posts = Post.objects.filter(created_date__lte=timezone.now()).order_by('created_date').filter(is_approved=False)
    #return render(request, 'blog/post_list.html', {'posts': posts})
    if request.method == "POST":
        form = ApproveForm(request.POST)
        if form.is_valid():
            print("hi")
            print("form validated")

        record_key = form.cleaned_data.get('record_number')
        print ("record key is")
        print(record_key)

        post = Post.objects.get(pk=record_key)
        print ("to approve")
        print (post.title)

        write_tempjason(post.ipfspath, post.title, post.text)
        currentdir = os.getcwd()
        os.chdir('/home/mihirgupta08/temp/nft-mix')
        os.system('/home/mihirgupta08/.virtualenvs/myvirtualenv/bin/brownie run scripts/simple_collectible/deploy_create.py --network rinkeby')
        os.chdir(currentdir)

        f = open('/home/mihirgupta08/temp/nft-mix/metadata/temp.json')
        # f = open('C:/Users/mihir/Desktop/djangogirls/nft-mix/metadata/temp.json')
        dictj = json.load(f)
        # if form.is_valid():
        # post = form.save(commit=False)

        # post = form.save(commit=False)

        #post.author = request.user
        post.published_date = timezone.now()
        post.is_approved = True
        messagedesc = post.title + "record num " + str(record_key) + " is approved\n"
        notify.send(request.user, recipient=post.author, actor=request.user, verb='Message', description=messagedesc)
        # post.ipfspath = dict["image"]
        #post.ipfspath = imageipfs
        post.openseaurl = dictj["openseaurl"]
        post.contractaddress = "https://rinkeby.etherscan.io/address/" + dictj["address"]
        print(post.ipfspath)
        post.save()
        return redirect('post_approve')
    else:
        form = ApproveForm()
    return render(request, 'blog/approve_list.html', {'form': form, 'posts': posts})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'blog/signup.html', {'form': form})


def messagechat(request):
    #try:
    users = User.objects.all()
    print(request.user)
    user = User.objects.get(username=request.user)

    if request.method == 'POST':
        print("hello in messagechat views.py")
        sender = User.objects.get(username=request.user)
        receiver = User.objects.get(id=request.POST.get('user_id'))
        print(sender)
        print(receiver)
        print(request.POST.get('message'))
        if sender != receiver:
            notify.send(sender, recipient=receiver, verb='Message', description=request.POST.get('message'))
        else:
            user.notifications.mark_all_as_read()
        return redirect('messagechat')
    else:
        #return HttpResponse("Invalid request  how ??")
        message = ""
    return render(request, 'blog/chat.html', {'users': users, 'user': user})
    #except Exception as e:
     #   print(e)
     #   return HttpResponse("Please login for sending messages")

#def login(request):
#    if request.method == 'POST':
#        form = UserCreationForm(request.POST)
#        if form.is_valid():
#            form.save()
#            username = form.cleaned_data.get('username')
#            raw_password = form.cleaned_data.get('password1')
#            user = authenticate(username=username, password=raw_password)
#            login(request, user)
#            return redirect('login')
#    else:
#        form = UserCreationForm()
#    return render(request, 'blog/signup.html', {'form': form})


# Create your views here.
