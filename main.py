
#




if __name__ == '__main__':
    while True:
        us = int(input('введите 1 для ВК'"\n"
                       'ввудите 2 для инсты'"\n"
                       'для выхода нажмите 0'"\n"
                       'введите необходимое значение - '))

        if us == 2:
            with open('Ya_token', 'r') as file_object:
                from instagram import *
                TOKEN = file_object.read().strip()
            token = TOKEN
            uploader = YaUploader(token)
            result = uploader.upload_for_net()
        elif us == 1:
            from VK import *
            with open('YA_token', 'r') as file_object:
                TOKEN = file_object.read().strip()
            token = TOKEN
            uploaders = YaUploaders(token)
            results = uploaders.upload_for_net()
        elif us == 0:
            exit(0)








