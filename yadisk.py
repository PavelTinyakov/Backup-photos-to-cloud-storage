import requests
from datetime import datetime


class YandexDisk:
    _base_url = 'https://cloud-api.yandex.net/v1/disk/'

    def __init__(self, token):
        self.token = token
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }

    def _create_folder(self, vk_owner_id: int) -> str:
        url = self._base_url + 'resources'
        base_folder = '/VK_photos_upload'
        response_base_folder = requests.get(url, headers=self.headers, params={'path': base_folder})
        response_base_folder.raise_for_status()
        if response_base_folder.status_code == 404:
            requests.put(url, headers=self.headers, params={'path': base_folder})
        folder_name = f'ID{vk_owner_id}_{datetime.now().strftime("%y%m%d_%H-%M-%S")}'
        path = f'{base_folder}/{folder_name}'
        requests.put(url, headers=self.headers, params={'path': path})
        return path

    def upload_files_to_disk(self, photos: list[dict], vk_owner_id: int):
        path = self._create_folder(vk_owner_id)
        url = self._base_url + 'resources/upload'
        for photo in photos:
            params = {
                'url': photo["url"],
                'path': f'{path}/{photo["file_name"]}',
                'disable_redirects': 'true'
            }
            response = requests.post(url, params=params, headers=self.headers)
            response.raise_for_status()
