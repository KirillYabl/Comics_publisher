import requests


def load_image(url, path):
    """Load image by url to file.
    Params
    --------------------------------------------
    :param url: str
      Url with image.
    :param path: str
      Path, where image will be saved.
    --------------------------------------------
    """
    response = requests.get(url)

    # check HTTPError
    response.raise_for_status()
    # some sites can return 200 and write error in body
    if 'error' in response:
        raise requests.exceptions.HTTPError(response['error'])

    with open(path, 'wb') as f:
        f.write(response.content)


def get_last_xkcd_num():
    """Load num of last xkcd comic on now.

    :return: str, num of last xkcd comic
    """
    url = 'https://xkcd.com/info.0.json'
    response = requests.get(url)
    # check HTTPError
    response.raise_for_status()
    # some sites can return 200 and write error in body
    if 'error' in response:
        logging.error(f'Error in response body. Url: {url}')
        raise requests.exceptions.HTTPError(response['error'])
    return response.json()['num']
