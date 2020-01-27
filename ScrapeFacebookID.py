from bs4 import BeautifulSoup
import requests, re

def about_page(req_about):
    soups = BeautifulSoup(req_about.content, 'html.parser')
    created = soups.findAll("div",{"class":"_4bl9"})
    n = 0
    no = 1
    info_contact = []
    result = []
    for i in created:
        if n > 1:
            tes01 = re.findall(r'class=\"[\w\-\"]+', str(i))
            if len(tes01) > 0:
                teks = []
                for j in tes01:
                    aa = re.findall(r'\".*\"', j)
                    if len(aa) > 0:
                        aa = aa[0]
                        tes = i.findAll("div", {"class":aa.replace('"','')})
                        if len(tes) > 0:
                            teks.append(tes[0].text)
                if len(teks) == 1:
                    if ".com" in teks[0]:
                        info_contact.append(teks[0])
                    else:
                        if len(teks[0]) > 6 and len(teks[0]) < 50:
                            result.append({"{}".format(no):teks[0]})
                            no += 1
                elif len(teks) > 1:
                    if len(teks[0]) == 0:
                        if len(teks[1]) > 6 and len(teks[1]) < 50:
                            result.append({"{}".format(no):teks[1]})
                            no += 1
                    else:
                        result.append({"{}".format(no):" : ".join(teks)})
                        no += 1
        n += 1
    if len(info_contact) > 0:
        result.append({"{}".format(no): "info contact : "+", ".join(info_contact)})
    return result

def main_facebook_page(username):
    # username = "jokowi"
    url = 'https://facebook.com/{}'.format(username)
    about = 'https://www.facebook.com/pg/{}/about/?ref=page_internal'.format(username)
    req_url = requests.get(url=url)
    req_about = requests.get(url=about)

    soup = BeautifulSoup(req_url.content, 'html.parser')
    mydivs = soup.findAll("div", {"class": "_4bl9"})
    # print(mydivs)
    orang = {}
    for i in  mydivs:
        if "menyukai" in i.text:
            orang.update({"Likes":re.findall(r"[0-9\.\w]+", i.text)[0]})
        if "mengikuti" in i.text:
            orang.update({"Followers": re.findall(r"[0-9\.\w]+", i.text)[0]})

    myimg = soup.findAll("div", {"class":"uiScaledImageContainer _62ui"})
    img = re.findall(r"https?:\/\/?\S+ ?", str(myimg[0]))
    pageID = re.findall(r'"pageID\"\:\"\w+\"', str(soup.contents))
    username = re.findall(r'"username\"\:\"\w+\"', str(soup.contents))

    orang.update({"profile_image_url":img[0].replace('"','').replace("&amp;","&")})
    orang.update(eval(str({pageID[0]}).replace("'","")))
    orang.update(eval(str({username[0]}).replace("'","")))
    orang.update({"About":about_page(req_about)})
    return orang

def main_facebook_account(username):
    # username = "bejo.durunkrabi"
    # username = "dhiksa.kusnaraga"
    url = 'https://facebook.com/{}'.format(username)
    req_url = requests.get(url=url)
    soup = BeautifulSoup(req_url.content, 'html.parser')

    myname = soup.findAll("title", {"id":"pageTitle"})
    img = soup.findAll("div", {"class":"photoContainer"})
    img = re.findall(r"https?:\/\/?\S+ ?", str(img[0]))
    pageID = re.findall(r'"entity_id\"\:\"\w+\"', str(soup.contents))
    pageID = eval(str({pageID[0]}).replace("'",""))

    result = {"username":username,
              "Fullname":myname[0].text.replace(" | Facebook",""),
              "profile_image_url":img[1].replace('"','').replace("&amp;","&"),
              'pageID':pageID['entity_id'],
              'Likes':"Don't have it :)",
              "Followers":"Don't have it :)"}

    return result

def main_facebook(username):
    try:
        return main_facebook_page(username)
    except:
        return main_facebook_account(username)

# if __name__ == '__main__':
#     print(main_facebook('bejo.durunkrabi'))



