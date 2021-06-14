import json
from django.shortcuts import render
from django.utils import timezone
from .models import Post
from .forms import PostForm
from django.shortcuts import redirect
from django.core.files.storage import FileSystemStorage
from pathlib import Path
import requests


import os, sys
import subprocess
import tempfile
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def upload_to_ipfs(filepath):
    PINATA_BASE_URL = 'https://api.pinata.cloud/'
    endpoint = 'pinning/pinFileToIPFS'
    # Change this to upload a different file
    #filepath = './img/pug.png'
    #filepath = fpath
    #filename = filepath.split('/')[-1:][0]
    filename = filepath
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




def post_new(request):
    print("File values in file dictionary:", request.FILES)
    #if request.method == "POST" and request.FILES['nftimagefile']:
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        uploaded_nft_file = request.FILES['nftimagefile']
        print("uploaded NFT Filename is ")
        print(uploaded_nft_file)
        #file1 = open("UploadFileName.txt", "w+")
        #fs = FileSystemStorage()
        #uploaded_file_name = fs.save(uploaded_nft_file.name, uploaded_nft_file)
        #print("Saved file name")
        #print (uploaded_file_name)

        #if form.is_valid():
            #post = form.save(commit=False)

        #ptitle = request.POST['title']
        #ptext = request.POST['text']
        #pimage = uploaded_file_name
        #print(type(pimage))
        #print("image name is")
        #print(uploaded_file_name)

        #file_temp = tempfile.NamedTemporaryFile()

        currentdir = os.getcwd()
        #os.chdir('uploads')
        #imageipfs = upload_to_ipfs(uploaded_nft_file)

        #imgpath = os.path.join(currentdir,"uploads",uploaded_nft_file)
        #imgpath = currentdir +"/" +  uploaded_file_name
        #imgpath = currentdir + "/uploads/" + file_temp

        #imgpath = os.path.join(currentdir,"uploads",pimage)
        #print(imgpath)
        #imageipfs = upload_to_ipfs(imgpath)
        #print(imageipfs)
        os.chdir('nft-mix')
        #os.system('brownie run scripts/simple_collectible/deploy_create.py --network rinkeby')
        os.chdir(currentdir)
        #fstr = os.path.join(os.path.dirname(__file__), "nft-mix/metadata/temp.json")
        #subprocess.call('C:/Users/Mihir/Desktop/blockchain/projects/djangogirls/djangogirls/nft-mix/nft.sh')
        #subprocess.call("cd C:/Users/Mihir/Desktop/blockchain/projects/djangogirls/djangogirls/nft-mix;nft.sh")
        #subprocess.call(['sh','C:/Users/Mihir/Desktop/blockchain/projects/djangogirls/djangogirls/nft-mix/nft.sh'])
        f = open('nft-mix/metadata/temp.json')
        #f = open('C:/Users/mihir/Desktop/djangogirls/nft-mix/metadata/temp.json')
        dict = json.load(f)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            #post.ipfspath = dict["image"]
            #post.openseaurl = dict["openseaurl"]
            #print(post.ipfspath)
            post.save()
            #imgpath = os.path.join(currentdir,"uploads",uploaded_nft_file)
            #print("final image path after postsave")
            #print(imgpath)
            #imageipfs = upload_to_ipfs(imgpath)
            #print(imageipfs)
            return redirect('deploy')
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def deploy(request):
    #posts = Post.objects.last()


    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
        post = posts.last()
        print ("last post titel")
        print(post.title)
        print(post.nftimagefile)

        currentdir = os.getcwd()

        imgpath = os.path.join(currentdir,uploaded_nft_file)
        imageipfs = upload_to_ipfs(post.nftimagefile)


        #imgpath = currentdir +"/" +  uploaded_file_name
        #imgpath = currentdir + "/uploads/" + file_temp

        #imgpath = os.path.join(currentdir,"uploads",pimage)
        #print(imgpath)
        #imageipfs = upload_to_ipfs(imgpath)
        #print(imageipfs)
        os.chdir('nft-mix')
        #os.system('brownie run scripts/simple_collectible/deploy_create.py --network rinkeby')
        os.chdir(currentdir)
        #fstr = os.path.join(os.path.dirname(__file__), "nft-mix/metadata/temp.json")
        #subprocess.call('C:/Users/Mihir/Desktop/blockchain/projects/djangogirls/djangogirls/nft-mix/nft.sh')
        #subprocess.call("cd C:/Users/Mihir/Desktop/blockchain/projects/djangogirls/djangogirls/nft-mix;nft.sh")
        #subprocess.call(['sh','C:/Users/Mihir/Desktop/blockchain/projects/djangogirls/djangogirls/nft-mix/nft.sh'])
        f = open('nft-mix/metadata/temp.json')
        #f = open('C:/Users/mihir/Desktop/djangogirls/nft-mix/metadata/temp.json')
        dict = json.load(f)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            #post.ipfspath = dict["image"]
            #post.openseaurl = dict["openseaurl"]
            #print(post.ipfspath)
            post.save()
            #imgpath = os.path.join(currentdir,"uploads",uploaded_nft_file)
            print("final image path after postsave")
            print(imgpath)
            #imageipfs = upload_to_ipfs(imgpath)
            #print(imageipfs)
            return redirect('deploy')
    else:
        form = PostForm()
    return render(request, 'blog/deploy.html', {'posts': posts})
    #return render(request, 'blog/post_edit.html', {'form': form})


def write_filename_json(filename):
    collectible_metadata = sample_metadata.metadata_template
    metadata_file_name = (
        "./metadata/"
        +
        "temp.json"
        )
    print("Creating Metadata file: " + metadata_file_name)
    collectible_metadata["name"] = "shitzu"
    collectible_metadata["description"] = "An adorable {} pup!".format(
        collectible_metadata["name"]
    )
         #   image_to_upload = None
         #   if os.getenv("UPLOAD_IPFS") == "true":
         #       image_path = "./img/{}.png".format(
          #          breed.lower().replace('_', '-'))
          #      image_to_upload = upload_to_ipfs(image_path)
        #    image_to_upload = (
         #       breed_to_image_uri[breed] if not image_to_upload else image_to_upload
         #   )
    collectible_metadata["image"] = ipfspath
    collectible_metadata["openseaurl"] = openseaurl

    with open(metadata_file_name, "w+") as file:
        json.dump(collectible_metadata, file)
         #   if os.getenv("UPLOAD_IPFS") == "true":
          #      upload_to_ipfs(metadata_file_name)


# Create your views here.
