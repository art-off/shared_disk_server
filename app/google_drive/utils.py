from app import app, db

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from .responses.file import File
from .auth_utils import get_credentials

from typing import Optional, Any


def __get_service(user_token: str) -> Any:
    credentials = get_credentials(user_token)
    service = build('drive', 'v3', credentials=credentials)
    return service


def create_folder(user_token, parent, folder_name):
    try:
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [parent],
        }
        file = __get_service(user_token).files().create(body=file_metadata,
                                                        fields='id').execute()
        return None, file.get('id')
    except:
        return 'credentials_is_not_valid', None


def get_files(user_token: str, folder: str) -> (Optional[str], Optional[str], list[File]):
    try:
        service = __get_service(user_token)
        # из-за этой строчки все это в try
        results = service.files().list(q=f'"{folder}" in parents and trashed=false').execute()
        files = results.get('files', [])
        next_page_token = results.get('nextPageToken', None)

        response_files = []
        for file in files:
            tmp = file['mimeType'].split('.')[-1]
            type = tmp if tmp == 'folder' else file['mimeType']
            response_files.append(File(file['id'],
                                       file['name'],
                                       file['kind'],
                                       type))

        return None, next_page_token, response_files
    except:
        return 'credentials_is_not_valid', None, None


def give_permissions(user_token, file_id, user_email):
    try:
        service = __get_service(user_token)
        user_permission = {
            'type': 'user',
            'role': 'writer',
            'emailAddress': user_email
        }
        result = service.permissions().create(
            fileId=file_id,
            body=user_permission,
            fields='id'
        ).execute()

        return None
    except:
        return 'credentials_is_not_valid'
