#!/usr/bin/python3
import os
import json
from brownie import SimpleCollectible, accounts, network, config
from dotenv import load_dotenv
from scripts.helpful_scripts import OPENSEA_FORMAT
from pathlib import Path
from metadata import sample_metadata

sample_token_uri = "https://ipfs.io/ipfs/Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json"
ipfspath = "https://ipfs.io/ipfs/QmSsYRx3LpDAb1GZQm7zZ1AuHZjfbPkD6J7s9r41xu1mf8?filename=pug.png"

load_dotenv()


def main():

    #deploy
    dev = accounts.add(config["wallets"]["from_key"])
    print(network.show_active())
    publish_source = True if os.getenv("ETHERSCAN_TOKEN") else False
    SimpleCollectible.deploy({"from": dev}, publish_source=publish_source)

   #createcollectible
    dev = accounts.add(config["wallets"]["from_key"])
    print(network.show_active())
    simple_collectible = SimpleCollectible[len(SimpleCollectible) - 1]
    token_id = simple_collectible.tokenCounter()
    transaction = simple_collectible.createCollectible(sample_token_uri, {"from": dev})
    transaction.wait(1)
    print(
          "Awesome! You can view your NFT at {}".format(
            OPENSEA_FORMAT.format(simple_collectible.address, token_id)
        )
    )
    openseaurl = OPENSEA_FORMAT.format(simple_collectible.address, token_id)

    # write metadata
    write_metadata(openseaurl)

    print('Please give up to 20 minutes, and hit the "refresh metadata" button')




def write_metadata(openseaurl):
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


# curl -X POST -F file=@metadata/rinkeby/0-SHIBA_INU.json http://localhost:5001/api/v0/add


#def upload_to_ipfs(filepath):
 #   with Path(filepath).open("rb") as fp:
  #      image_binary = fp.read()
   #     ipfs_url = (
    #        os.getenv("IPFS_URL")
     #       if os.getenv("IPFS_URL")
      #      else "http://localhost:5001"
       # )
       # response = requests.post(ipfs_url + "/api/v0/add",
        #                         files={"file": image_binary})
       # ipfs_hash = response.json()["Hash"]
       # filename = filepath.split("/")[-1:][0]
        #image_uri = "https://ipfs.io/ipfs/{}?filename={}".format(
        #    ipfs_hash, filename)
        #print(image_uri)
    #return image_uri

    #import requests
   # import os
    #from pathlib import Path

   # PINATA_BASE_URL = 'https://api.pinata.cloud/'
    # endpoint = 'pinning/pinFileToIPFS'
    # Change this to upload a different file
   # filepath = './img/pug.png'
   # filename = filepath.split('/')[-1:][0]
    # headers = {'pinata_api_key': os.getenv('PINATA_API_KEY'),
    #           'pinata_secret_api_key': os.getenv('PINATA_API_SECRET')}

    #with Path(filepath).open("rb") as fp:
     #    image_binary = fp.read()
      #  response = requests.post(PINATA_BASE_URL + endpoint,
       #                          files={"file": (filename, image_binary)},
        #                         headers=headers)
       # print(response.json())


