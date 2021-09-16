from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload,MediaFileUpload
from googleapiclient.discovery import build
from pprint import pprint
import io


SCOPES = ['https://www.googleapis.com/auth/drive']

SERVICE_ACCOUNT_FILE = '_____.json'


credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('drive', 'v3', credentials=credentials)

# results = service.files().list(pageSize=10,
#                                fields="nextPageToken, files(id, name, mimeType)").execute()

results = service.files().list(pageSize=10,
                               fields="nextPageToken, files(id, name, mimeType)").execute()
nextPageToken = results.get('nextPageToken')
while nextPageToken:
        nextPage = service.files().list(pageSize=10,
                                        fields="nextPageToken, files(id, name, mimeType, parents)",
                                        pageToken=nextPageToken).execute()
        nextPageToken = nextPage.get('nextPageToken')
        results['files'] = results['files'] + nextPage['files']
pprint(len(results.get('files')))


resultss = service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name, mimeType, parents, createdTime, permissions, quotaBytesUsed)").execute()

# pprint(resultss.get('files'))


folder_id = '0B5GKNJPzW728TXZqVGx5cU5PRDQ'
name = 'Script_2.py'
file_path = 'https://scontent-arn2-1.cdninstagram.com/v/t51.2885-15/64639459_188931085432282_8969799728223764862_n.jpg?_nc_cat=109&ccb=1-5&_nc_sid=8ae9d6&_nc_ohc=kHOoiGvtUCIAX_KRyYa&_nc_ht=scontent-arn2-1.cdninstagram.com&edm=ANo9K5cEAAAA&oh=1e1eaa9909200926a1f78681165c5e49&oe=6146EED6'
file_metadata = {
                'name': name,
                'parents': [folder_id]
            }
# media = MediaFileUpload(file_path, resumable=True)
# r = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
# pprint(r)


# file_metadata = {'name': 'photo.jpg'}
media = MediaFileUpload(file_path, mimetype='image/jpeg')
file = service.files().create(body=file_metadata,
                                    media_body=media,
                                    fields='id').execute()
print('File ID: %s' % file.get('id'))