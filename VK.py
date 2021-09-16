import configparser
import time
from pprint import pprint
import os
import requests
import datetime
# import yadisk
import json
from collections import Counter


class VkUser:
    jjson = None
    url = 'https://api.vk.com/method/'
    photo_link = []

    def __init__(self, token, version, user):
        self.params = {
            'user_id': user,
            'access_token': token,
            'v': version
        }

    def _get_user_name(self):
        user_dict = {}
        url = self.url + "users.get"
        response = requests.get(url, params=self.params).json()

        for item in response['response']:
            user_id = item['id']
            first_name = item['first_name']
            last_name = item['last_name']

            user_dict[user_id] = {"first_name": first_name, "last_name": last_name}
        return user_dict
        # pprint(user_dict)

    def get_photos(self):
        links = []
        users = {}
        users_name = self._get_user_name()

        for _id, _user in users_name.items():
            first_name = _user["first_name"]
            last_name = _user["last_name"]

            get_photo_url = self.url + 'photos.get'
            photo_params = {
                # 'user_id': '1',
                'album_id': 'profile',
                'extended': 1,
                'count': 1000,
                'rev': 0,
                'photo_sizes': 1
            }

            res = requests.get(get_photo_url, params={**self.params, **photo_params}, timeout=5).json()
            ressult_json = res['response']['items']
            # pprint(ressult_json)

            for item in ressult_json:
                likes = item['likes']['count']
                sizes = item['sizes']
                photo = sizes[-1]['type']
                max_size_url = sizes[-1]['url']
                for i in max_size_url:
                    if i in self.photo_link:
                        continue
                    else:
                        self.photo_link.append(max_size_url)

                # pprint(self.photo_link)

                times = item['date']
                times = datetime.datetime.fromtimestamp(times).strftime("%d-%m-%Y_%H_%M_%S")

                users.setdefault("results", dict())
                users["id"] = _id
                users["first_name"] = first_name
                users["last_name"] = last_name
                users["user_name"] = self.params['user_id']
                self.jjson = users

                if f"{likes}.jpg" not in users["results"]:

                    users["results"][f"{likes}.jpg"] = {"photo_type": photo, "photo_url": max_size_url}
                else:
                    users["results"][f"{likes}_{times}.jpg"] = {"photo_type": photo, "photo_url": max_size_url}

            # file_name = f"files/{self.params['user_id']}/{self.params['user_id']}-{first_name} {last_name}-{_id}.json"

            # if not os.path.exists(os.path.dirname(file_name)):
            #     os.makedirs(os.path.dirname(file_name))
            #
            # with open(file_name, 'w') as f:
            #   json.dump(users, f, indent=2, ensure_ascii=False)
            # with open(file_name) as file:
            #     self.jjson = json.load(file)
            #     pprint(self.jjson)



with open('token.txt', 'r') as file_object:
    token = file_object.read().strip()
vk_client = VkUser(token=token, version=5.131, user=int(input('введите ID - ')))
vk_client.get_photos()
vk_client._get_user_name()
# vk_client.link_foto()




class YaUploaders:

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


    # def upload_for_net(self, file_pass: str):
    def upload_for_net(self):
        upload_url = self.url + "resources/upload"
        results = vk_client.jjson["results"]
        first_name = vk_client.jjson['first_name']
        last_name = vk_client.jjson['last_name']
        id_ = vk_client.jjson['id']
        user_name = vk_client.jjson['user_name']

        path = self.get_folders(["VK", f"{user_name}-{first_name} {last_name}-{id_}"])

        for item in results:
            url_path = results[item]["photo_url"]
            file_name = item

            params = {
                "path": f"{path}{file_name}",
                "url": url_path
            }

            response = requests.post(url=upload_url, headers=self._get_headers(), params=params, timeout=5)

            if response.status_code == 202:
                print(f"файл {file_name} заружен")
        print("Загрузка завершена")


        # for i in file_pass:
        #     time.sleep(3)
        #     upload_url = self.url + "resources/upload"
        #     headers = {**self._get_headers()}
        #     params = {'path': file, 'url': i}
        #     r = requests.post(url=upload_url, params=params, headers=headers)
        #     res = r.json()
        #     pprint(res)

if __name__ == '__main__':
    # sdt = []
    # sdt.append(set(vk_client.photo_link))
    # dd = "photo_url"
    # for dd in "requestsPy-main/files/120657568/120657568-Валерия Таскаева-120657568.json":


    # dounload_path = [i for i in sdt]

    # file = ('qwe')



    with open('YA_token', 'r') as file_object:
        TOKEN = file_object.read().strip()
    token = TOKEN
    uploaders = YaUploaders(token)
    # result = uploader.upload_for_net(*sdt)
    results = uploaders.upload_for_net()










