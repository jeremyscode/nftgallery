from flask import Blueprint, render_template, request, flash
import os
import requests
import logging

ALCHEMY_API_KEY = os.getenv('ALCHEMY_API_KEY')

logger = logging.getLogger(__name__)

home = Blueprint('home', __name__)


def get_nfts_from_collection(collection_address, next_token=0):
    """
    Returns NFT data from give collection address
    """
    if next_token > 0:
        # Get next page
        url = f"https://eth-mainnet.alchemyapi.io/nft/v2/{ALCHEMY_API_KEY}/getNFTsForCollection/" \
              f"?contractAddress={collection_address}&withMetadata=true&startToken={next_token}"
        data = requests.get(url).json()
        # print(data)
        # nextToken
        return data
    else:
        url = f"https://eth-mainnet.alchemyapi.io/nft/v2/{ALCHEMY_API_KEY}/getNFTsForCollection/" \
              f"?contractAddress={collection_address}&withMetadata=true"
        data = requests.get(url).json()
        # print(data)
        # nextToken
        return data


def get_nfts(owner_address, collection_address=None):
    """
    dfddfd
    """
    if collection_address:
        # Return owner's NFTs in Collection
        url = f"https://eth-mainnet.alchemyapi.io/nft/v2/{ALCHEMY_API_KEY}/getNFTs/" \
              f"?owner={owner_address}&contractAddresses%5B%5D={collection_address}"
        data = requests.get(url).json()
        return data
    else:
        # Just return all NFTs in owner's wallet
        url = f"https://eth-mainnet.alchemyapi.io/nft/v2/{ALCHEMY_API_KEY}/getNFTs/" \
              f"?owner={owner_address}"
        data = requests.get(url).json()
        return data


# Basic site routes
@home.route('/', methods=['GET'])
def index_get():
    """ Just a GET request """
    nft_list = []
    return render_template('index.html', nft_list=nft_list)


@home.route('/<nft_collection>/<int:next_token>', methods=['POST'])
@home.route('/', methods=['POST'])
def index_post(nft_collection=None, next_token=0):
    """ POST request """
    owner_address = request.form.get('owner_address')
    collection = request.form.get('collection_address')
    checkbox = request.form.get('checkbox')
    nft_list = []
    if next_token > 0:
        nft_list = get_nfts_from_collection(collection_address=nft_collection, next_token=next_token)
        if len(nft_list['nfts']) > 0:
            if 'nextToken' in nft_list.keys():
                next_token = nft_list['nextToken']
                next_token = int(next_token, 16)
                return render_template(
                    'index.html',
                    nft_list=nft_list,
                    next_token=next_token
                )
            else:
                # Not enough tokens for pagination
                return render_template(
                    'index.html',
                    nft_list=nft_list,
                    next_token=next_token
                )
        else:
            # no nfts returned
            return render_template('index.html', nft_list=nft_list)
    else:
        if checkbox == 'on':
            nft_list = get_nfts_from_collection(collection)
            # print(nft_list)
            if len(nft_list['nfts']) > 0:
                if 'nextToken' in nft_list.keys():
                    next_token = nft_list['nextToken']
                    next_token = int(next_token, 16)
                    return render_template(
                        'index.html',
                        nft_list=nft_list,
                        next_token=next_token
                    )
                else:
                    # Not enough tokens for pagination
                    return render_template(
                        'index.html',
                        nft_list=nft_list,
                        next_token=next_token
                    )
            else:
                # no nfts returned
                return render_template('index.html', nft_list=nft_list)
        else:
            # Checkbox is not checked
            if owner_address == '':
                # No owner address given
                flash("Need an owner address skippy.")
                return render_template('index.html', nft_list=nft_list)
            else:
                nft_list = get_nfts(
                    owner_address=owner_address,
                    collection_address=collection
                )
                if len(nft_list) > 0:
                    return render_template('index.html', nft_list=nft_list)
                else:
                    # no nfts returned
                    return render_template('index.html', nft_list=nft_list)
