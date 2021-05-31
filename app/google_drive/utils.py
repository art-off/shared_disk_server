from app import app, db

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from .responses.file import File
from .auth_utils import get_credentials

from typing import Optional, Any


def get_files(user_token: str, folder: str) -> (Optional[str], Optional[str], list[File]):
    try:
        service = __get_service(user_token)
        # из-за этой строчки все это в try
        results = service.files().list(q=f'"{folder}" in parents').execute()
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


def __get_service(user_token: str) -> Any:
    credentials = get_credentials(user_token)
    service = build('drive', 'v3', credentials=credentials)
    return service
