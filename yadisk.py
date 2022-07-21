import json
from datetime import datetime

import requests
from tqdm import tqdm


class YandexDisk:
    _base_url = 'https://cloud-api.yandex.net/v1/disk/'

    def __init__(self, token):
        self.token = token
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }

    def _create_folder(self, vk_owner_id: int, ya_base_folder: str) -> str:
        url = self._base_url + 'resources'
        base_folder = f'/{ya_base_folder}'
        status_base_folder = requests.get(url, headers=self.headers, params={'path': base_folder}).status_code
        if status_base_folder == 404:
            requests.put(url, headers=self.headers, params={'path': base_folder})
        folder_name = f'ID{vk_owner_id}_{datetime.now().strftime("%y%m%d_%H-%M-%S")}'
        path = f'{base_folder}/{folder_name}'
        response = requests.put(url, headers=self.headers, params={'path': path})
        response.raise_for_status()
        return path

    def upload_files_to_disk(self, photos: list[dict], vk_owner_id: int, upload_log: bool, ya_base_folder: str) -> None:
        path = self._create_folder(vk_owner_id, ya_base_folder)
        url = self._base_url + 'resources/upload'
        pbar = tqdm(photos, ncols=100)
        for photo in pbar:
            pbar.set_description(f'Я.Диск. Загрузка фото {photo["file_name"]}')
            params = {
                'url': photo["origin_url"],
                'path': f'{path}/{photo["file_name"]}',
                'disable_redirects': 'true'
            }
            response = requests.post(url, params=params, headers=self.headers)
            response.raise_for_status()
        tqdm.write('Загрузка фотографий на Я.Диск завершена')
        if upload_log:
            file_name = f'{path.split("/")[-1]}.json'
            with open(f'ya_upload_log/{file_name}', 'w', encoding='utf-8') as file:
                json.dump({path: photos}, file, indent=1)
            tqdm.write(f'Данные загрузки записаны в файл {file_name}')
