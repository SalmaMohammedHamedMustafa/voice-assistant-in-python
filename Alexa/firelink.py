# firelink.py

import webbrowser

#favorite website links
facebook_link = "https://www.facebook.com"
google_link = "https://www.google.com"
youtube_link = "https://www.youtube.com"
twitter_link = "https://www.twitter.com"


def firefox(url):
    """
    Opens the given links on firefox browser
    parameters:
    url
    return:
    None
    """
    webbrowser.get('firefox').open(url)
