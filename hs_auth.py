import urllib2
import urllib
import json
import sys

def authenticate_with_hs(email, password):
    """
    Sends email and password to Hacker School's authentication page
    If login is successful, returns user's information
    Otherwise, returns "none"
    """
    base_link = "https://www.hackerschool.com/auth"
    request = urllib2.Request(base_link)

    data = {"email": email, "password": password}
    request.add_data(urllib.urlencode(data))

    try:
        response = urllib2.urlopen(request)
        return json.load(response)
    except urllib2.HTTPError:
        return None

if __name__ == '__main__':
    _, USER_EMAIL, USER_PASSWORD = sys.argv
    print authenticate_with_hs(USER_EMAIL, USER_PASSWORD)
