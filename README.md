# Comics publisher

This program allow you posting xkcd comics in VK automatically!

Now you dont need lose you time and you can just reading comics!

### How to install

You need to create `.env` file and write in file parameters `VK_APP_TOKEN` and `GROUP_ID`.

`GROUP_ID` - id of your VK group, you can get your group id [on this website](http://regvk.com/id/)

`VK_APP_TOKEN` - secret token of you VK app. If you need this token you need:

1) [Create standalone VK APP](https://vk.com/apps?act=manage) - push `Create app` button.
2) Get your APP ID - start edit your app anf read APP ID in address bar
3) [Get token](https://vk.com/dev/implicit_flow_user) - you need add `photos`, `groups`, `wall` and `offline` in `scope` param. Also set `response_type=token`

Python3 should be already installed. 
Then use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
```
pip install -r requirements.txt
```

### How to use

Open command line (in windows `Win+R` and write `cmd` and `Ok`). Go to directory with program or just write in cmd:

`python <PATH TO PROGRAM>\make_xkcd_image_post.py [--from_group] [--vk_api_version VK_API_VERSION]`

`from_group` - flag, if used then author of post is group (optional)

`vk_api_version` - version of VK API. Default 5.101 (optional)

### Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).
