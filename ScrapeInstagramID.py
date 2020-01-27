from bs4 import BeautifulSoup
import requests, re

def main_instagram(username):
    url = 'https://www.instagram.com/{}'.format(username)
    r = requests.get(url=url)
    soup = BeautifulSoup(r.content, 'html.parser')
    mydivs = soup.findAll("script", {"type": "text/javascript"})
    result = {}
    for i in mydivs:
        a = re.findall(r'"id"\:',str(i))
        if len(a) > 0:
            value = re.findall(r'\{\"config\":.*\}',str(i))
            value = eval(value[0].replace('false','False').replace('true','True').replace('null','None'))
            result = {'ID':str(value['entry_data']['ProfilePage'][0]['graphql']['user']['id']),
                      'Fullname':value['entry_data']['ProfilePage'][0]['graphql']['user']['full_name'],
                      'Username':value['entry_data']['ProfilePage'][0]['graphql']['user']['username'],
                      'profile_image_url':value['entry_data']['ProfilePage'][0]['graphql']['user']['profile_pic_url'],
                      'Biography':value['entry_data']['ProfilePage'][0]['graphql']['user']['biography'],
                      'Private':str(value['entry_data']['ProfilePage'][0]['graphql']['user']['is_private']).title()
                      }
            break

    mydivs = soup.findAll("meta", {"property":"og:description"})
    engage = re.findall(r"content\=.*\-", str(mydivs[0]))
    if len(engage) == 0:
        follower = "Sorry :("
        following = "Sorry :("
        post = "Sorry :("
    else:
        engage = engage[0].replace('content="',"").replace(" -","")
        follower = re.findall("[0-9].*Followers", engage)[0]
        following = re.findall("[0-9].*Following", engage.replace(follower+", ", ""))[0]
        post = engage.replace(follower+", "+following+", ", "")
    result.update({"Follower":follower.replace(" Followers","").replace(",","."),
                   'Following':following.replace(" Following","").replace(",","."),
                   'Statuses':post.replace(" Posts","").replace(",",".")})
    return result

# if __name__ == '__main__':
#     print(main_instagram('jokowi'))

