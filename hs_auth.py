import urllib2
from urllib import urlencode
import json

def authenticate_with_hs(email, password):
  base_link = "https://www.hackerschool.com/auth"
  request = urllib2.Request(base_link)

  data = {"email": email, "password": password}
  request.add_data(urlencode(data))

  try:
    response = urllib2.urlopen(request)
    return json.load(response)
  except HTTPError:
    return None

if __name__ == '__main__':
  import sys
  _, email, password = sys.argv
  print authenticate_with_hs(email, password)
