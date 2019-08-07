import argparse
import logging
import os
import random

import dotenv
import requests

import common_functions as cf
from vk_auto_post import VKAutoPost


def get_xkcd_comic_meta():
    """Load xkcd comic image and get meta information about comic
    :return: dict, comic meta information
    """
    # get random comic if from 1 to last comic on now
    comic_id = random.randint(1, cf.get_last_xkcd_num())

    url = f'http://xkcd.com/{comic_id}/info.0.json'
    response = requests.get(url)
    cf.raise_response_errors(response)

    comic_meta = response.json()

    return comic_meta


def main():
    doc = '''
              This program allow you posting xkcd comics in VK automatically!
              Usage: python make_xkcd_image_post.py [from_group] [api_version]
              '''

    logging.basicConfig(format='%(asctime)s  %(name)s  %(levelname)s  %(message)s', level=logging.INFO)

    parser = argparse.ArgumentParser(description=doc, formatter_class=argparse.RawTextHelpFormatter)
    # optional args
    parser.add_argument('--from_group', action='store_true',
                        help='True if author of post is group else False. Default True (optional)', default=True)
    parser.add_argument('--vk_api_version', help='Version of VK API. Default "5.101" (optional)', default='5.101')
    args = parser.parse_args()

    logging.debug('Start posting on group wall random xkcd comic with description')
    FROM_GROUP = str(int(args.from_group))
    logging.debug('In params parsed')

    vk_poster_logger = logging.getLogger('vk_poster')

    logging.debug('Get env parameters')
    dotenv.load_dotenv()
    VK_APP_TOKEN = os.getenv('VK_APP_TOKEN')
    GROUP_ID = os.getenv('GROUP_ID')
    logging.debug('Env parameters was got')

    comic_meta = get_xkcd_comic_meta()
    img_num = comic_meta["num"]
    logging.debug(f'Got xkcd comic meta information. Comic num: {img_num}')

    img_name = f'comic_{img_num}.png'
    img_url = comic_meta['img']

    cf.load_image(img_url, img_name)
    logging.debug('Loaded comic image in local')

    logging.debug('Starting post photo')
    vk_poster = VKAutoPost(VK_APP_TOKEN, GROUP_ID, args.vk_api_version)

    vk_poster.post_img_on_wall(comic_meta['alt'], FROM_GROUP, img_name)

    logging.debug('Ending posting on group wall random xkcd comic with description')


if __name__ == '__main__':
    main()
