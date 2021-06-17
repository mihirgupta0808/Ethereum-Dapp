#!/usr/bin/python3
import os
import subprocess
#from brownie import SimpleCollectible, accounts, network, config
#from dotenv import load_dotenv

#result = subprocess.run (['brownie', 'run scripts/simple_collectible/deploy_create.py --network rinkeby'], stdout=subprocess.PIPE)
#result.stdout

print ("calling brownie")
os.system ("brownie run scripts/simple_collectible/deploy_create.py --network rinkeby")
print ("after script execution")
