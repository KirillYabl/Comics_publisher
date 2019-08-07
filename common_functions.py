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
    raise_response_errors(response)

    with open(path, 'wb') as f:
        f.write(response.content)


def raise_response_errors(response):
    """Check response for errors.
    raise error if some error in response

    :param response: requests response object
    """
    # check HTTPError
    response.raise_for_status()
    # some sites can return 200 and write error in body
    if 'error' in response.json():
        raise requests.exceptions.HTTPError(response.json()['error'])


def get_last_xkcd_num():
    """Load num of last xkcd comic on now.

    :return: str, num of last xkcd comic
    """
    url = 'https://xkcd.com/info.0.json'
    response = requests.get(url)
    raise_response_errors(response)
    return response.json()['num']
