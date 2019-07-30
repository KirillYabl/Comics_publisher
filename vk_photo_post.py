import logging
import os

import requests


class VKAutoPost:
    """Poster photos in VK.
    Using VK API.

    For posting photo in VK you need to do 4 actions:
    1. Get address of server for download photo (method of class: _get_server_upload_image)
    2. Upload photo on server (method of class: upload_image_on_server)
    3. Save photo in group photoalbum (method of class: save_photo_in_group_album)
    4. Post photo from group photoalbum to wall (method of class: post_img_on_wall)

    Methods of this class realize this sequence.


    :param token: str, your app token which you must got with help of instruction https://vk.com/dev/implicit_flow_user
    :param group_id: str or int, id of your VK group
    :param api_version: str, version of VK API, need in every VK API methon
    :param logger: object of logger
    :param logger_handler: str, type of logger handlong
    """

    def __init__(self, token, group_id, api_version, logger=None):
        self.token = token
        self.group_id = group_id
        self.api_version = api_version
        self.logger = logger

        if logger is None:
            self.logger = logging.getLogger('VK autopost self log')
            handler = logging.NullHandler()
            self.logger.addHandler(handler)

        # urls of using methods of API
        self.server_upload_url = 'https://api.vk.com/method/photos.getWallUploadServer'
        self.save_photo_in_group_album_url = 'https://api.vk.com/method/photos.saveWallPhoto'
        self.wall_post_url = 'https://api.vk.com/method/wall.post'

        self.logger.debug('Initialize class params')

    def _get_server_upload_url(self):
        """Internal method which get server url for upload photo."""
        params = {
            'access_token': self.token,
            'v': self.api_version,
            'group_id': self.group_id
        }
        self.logger.debug('Getting server url for upload')
        response = requests.get(self.server_upload_url, params)

        # check HTTPError
        response.raise_for_status()
        # some sites can return 200 and write error in body
        if 'error' in response:
            self.logger.error(f'Error in response body. Url: {self.server_upload_url}')
            raise requests.exceptions.HTTPError(response['error'])

        self.upload_server_url = response.json()['response']['upload_url']

        self.logger.info('Got server url for upload')

    def _upload_image_on_server(self, image_name):
        """Internal method which upload image on server.

        :param image_name: str, image name (recommend give with path)
        """
        self._get_server_upload_url()
        self.logger.debug('Start upload image on server')
        self.logger.debug('Open image')

        image_file_descriptor = open(image_name, 'rb')
        self.logger.debug('Image opened')

        # upload image on server
        files = {'photo': image_file_descriptor}
        response = requests.post(self.upload_server_url, files=files)

        # check HTTPError
        response.raise_for_status()
        # some sites can return 200 and write error in body
        if 'error' in response:
            self.logger.error(f'Error in response body. Url: {self.upload_server_url}')
            raise requests.exceptions.HTTPError(response['error'])

        self.logger.info('Image was uploaded on server')
        image_file_descriptor.close()
        os.remove(image_name)
        self.logger.debug('Image was closed and removed')

        self.server = response.json()['server']
        self.photo = response.json()['photo']
        self.vk_hash = response.json()['hash']

    def _save_photo_in_group_album(self):
        """Internal method which saves photo in group photoalbum"""
        params = {
            'access_token': self.token,
            'v': self.api_version,
            'group_id': self.group_id,
            'photo': self.photo,
            'server': self.server,
            'hash': self.vk_hash
        }
        self.logger.debug('Start saving photo in group photoalbum')
        response = requests.post(self.save_photo_in_group_album_url, params)

        # check HTTPError
        response.raise_for_status()
        # some sites can return 200 and write error in body
        if 'error' in response:
            self.logger.error(f'Error in response body. Url: {self.save_photo_in_group_album_url}')
            raise requests.exceptions.HTTPError(response['error'])

        # parameters for posting photo on wall method
        self.attachments_owner_id = response.json()['response'][0]['owner_id']
        self.media_id = response.json()['response'][0]['id']
        self.logger.info('Photo was saved in group photoalbum')

    def _make_modif_params_for_photo_posting(self):
        """Internal method which make preparations for posting image on wall."""
        self.owner_id = f'-{self.group_id}'
        self.attachments = f'photo{self.attachments_owner_id}_{self.media_id}'

    def post_img_on_wall(self, message, from_group, image_name):
        """Posting photo to group wall with message

        :param message: str, signature for photo
        :param from_group: str or int, 1 if author of photo is group, 0 if user
        :param image_name: str, image name (recommend give with path)
        """
        self.logger.debug('Start posting photo on group wall')
        # preprocessing before posting
        self._upload_image_on_server(image_name)
        self._save_photo_in_group_album()
        self._make_modif_params_for_photo_posting()

        params = {
            'access_token': self.token,
            'v': self.api_version,
            'owner_id': self.owner_id,
            'from_group': from_group,
            'attachments': self.attachments,
            'message': message
        }

        response = requests.post(self.wall_post_url, params)
        # check HTTPError
        response.raise_for_status()
        # some sites can return 200 and write error in body
        if 'error' in response:
            self.logger.error(f'Error in response body. Url: {self.wall_post_url}')
            raise requests.exceptions.HTTPError(response['error'])

        self.logger.info('Photo was posted on wall')
