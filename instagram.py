import json
import os
from pprint import pprint
import re
import requests
# from google_auth_oauthlib.flow import *









class Instagram:
    asd = None
    jjsomn = None
    photo_link = []
    url = 'https://graph.instagram.com/me/media'
    with open('insta_token') as f:
        TKEN = f.readlines()
        def __init__(self):
            self.params = {
                'access_token': self.TKEN,
                'fields': 'id,caption,media_type,media_url,username,timestamp',
                'limit': 1000
            }


    def get_insta_data(self):
        user_dikt = []
        url = self.url


        req = requests.get(url=url, params={**self.params}).json()

        for data in req['data']:
            user_name = data['username']
            timestamp = data['timestamp']
            _id = data['id']
            user_dikt.append(user_name)
            return user_dikt

    def get_insta_photo(self):
        users = {}
        url = self.url
        name = self.get_insta_data()
        user_name = name[0]

        req = requests.get(url=url, params={**self.params}).json()

        for data in req['data']:
            timestamp = data['timestamp']
            _id = data['id']
            media_url = data['media_url']
            media_type = data['media_type']

            users.setdefault("results", dict())
            users["id"] = _id
            users["name"] = user_name
            users['times'] = timestamp
            users['media_url'] = media_url
            users['media_type'] = media_type
            self.jjsomn = users


            if F'{_id}.jpg' not in users['results']:
                users['results'][f'{_id}.jpg'] = {"name": user_name, 'id': _id,
                                                  'media_type': media_type, 'media_url': media_url}
            else:
                users['results'][f'{_id}.jpg'] = {"name": user_name,
                                                              'media_type': media_type, 'media_url': media_url}

        # file_name = f"files/{user_name}.json"

        # if not os.path.exists(os.path.dirname(file_name)):
        #     os.makedirs(os.path.dirname(file_name))

        # with open(file_name, 'w') as f:
        #     json.dump(users, f, indent=2, ensure_ascii=False)
        # with open(file_name) as file:
        #     self.jjsomn = json.load(file)
        #     pprint(self.jjsomn)



insta = Instagram()
insta.get_insta_data()
insta.get_insta_photo()




class YaUploader:

    url = "https://cloud-api.yandex.net/v1/disk/"
    def __init__(self, token: str):
        self.token = token

    def _get_headers(self):
        return {
            "Content-Type": "application/json",
            "Authorization": f"OAuth {self.token}"
        }

    def get_folders(self, folders: list):
        headers = self._get_headers()
        url = self.url + "resources"

        directs = ""

        for index, folder in enumerate(folders):
            if index == 0:
                params = {
                    "path": folder
                }

                response = requests.put(url, headers=headers, params=params, timeout=5)
                directs += f"{folder}/"

                if response.status_code == 201:
                    folders_name = f"Создана корневая папка {folder}"
                    print(folders_name)
            else:
                directs += f"{folders[index]}/"
                params = {
                    "path": directs
                }

                response = requests.put(url, headers=headers, params=params)

                if response.status_code == 201:
                    folders_name = f"Создана папка {folder} по пути {directs}"
                    print(folders_name)

        return directs

    def upload_for_net(self):
        upload_url = self.url + "resources/upload"
        results = insta.jjsomn["results"]
        name = insta.jjsomn['name']
        id_ = insta.jjsomn['id']

        path = self.get_folders(["INSTA", f"{name}-{id_}"])

        for item in results:
            url_path = results[item]["media_url"]
            file_name = item

            params = {
                "path": f"{path}{file_name}",
                "url": url_path
            }

            response = requests.post(url=upload_url, headers=self._get_headers(), params=params, timeout=5)

            if response.status_code == 202:
                print(f"{file_name} загружен")
        print("Загрузка завершена")

if __name__ == '__main__':

    with open('Ya_token', 'r') as file_object:
        TOKEN = file_object.read().strip()
    token = TOKEN
    uploader = YaUploader(token)
    result = uploader.upload_for_net()
