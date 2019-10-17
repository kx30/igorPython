import urllib.request

import firebase_admin
from bs4 import BeautifulSoup
from firebase_admin import credentials, firestore

cred = credentials.Certificate('./gson.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

url = urllib.request.urlopen("http://kalyan-expert.ru/tabak-dlya-kalyana-sebero.html")
bs = BeautifulSoup(url, 'html.parser')

titles = []
tastes = []
descriptions = []


def main():
    div = bs.find('div', {'class': 'item-page-bg'})
    ul = div.find('ul')
    description = ''
    hookah_urls = []
    n = 0
    title = "Sebero"
    list = []

    for item in div.find_all('p'):
        if item.find('strong'):
            continue
        description += item.get_text() + '\n'

    print(description.strip())

    for item in ul.find_all('li'):
        hookah_urls.append(item.get_text())

    for i in hookah_urls:
        titles.append(i.split('-')[0].strip())
        tastes.append(i.replace('Sebero', '').split('-')[0].strip())
        descriptions.append(i.split('-')[1].strip().capitalize())

        list.append(({
            'title': titles[n],
            'taste': tastes[n],
            'description': descriptions[n],
            'popularity': 0
        }))

        try:
            doc_ref = db.collection('tobacco').document(title)
            doc_ref.update({
                'title': title,
                'description': description,
                'image': ''
            })
        except Exception as e:
            print('Error: ' + str(e))
        n += 1

    for item in list:
        print(item)

    try:
        doc_ref = db.collection('tobacco').document(title)
        doc_ref.update({
            'list tobacco': list,
        })
    except Exception as e:
        print('Error: ' + str(e))


if __name__ == '__main__':
    main()
