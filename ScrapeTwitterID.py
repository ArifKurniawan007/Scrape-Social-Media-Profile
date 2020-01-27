from bs4 import BeautifulSoup
from datetime import datetime
from dateutil import parser
import requests

def main_twitter(username):
    url = 'https://twitter.com/{}'.format(username)
    r = requests.get(url=url)

    soup = BeautifulSoup(r.content, 'html.parser')
    mydivs = soup.findAll("input", {"class": "json-data"})
    text = mydivs[0].get('value').replace('false','False').replace('true','True').replace('null','None')
    text = eval(text)
    result = {'ID':text['profile_user']['id_str'],
              'FullName':text['profile_user']['name'],
              'UserName':text['profile_user']['screen_name'],
              'Location':text['profile_user']['location'],
              'Follower':"{:,}".format(text['profile_user']['followers_count']).replace(',','.'),
              'Following':"{:,}".format(text['profile_user']['friends_count']).replace(',','.'),
              'Statuses':"{:,}".format(text['profile_user']['statuses_count']).replace(',','.'),
              'Join':datetime.strftime(parser.parse(text['profile_user']['created_at']), "%d %B %Y "),
              'profile_image_url':str(text['profile_user']['profile_image_url']).replace("\\","").replace("_normal","_reasonably_small")}
    return result

# if __name__ == '__main__':
#     main_twitter('bkngoid')
