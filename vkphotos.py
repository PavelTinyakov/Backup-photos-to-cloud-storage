from datetime import datetime
import re

import requests


class VkPhotos:
    _base_url = 'https://api.vk.com/method/'

    def __init__(self, token: str):
        self.base_params = {'access_token': token, 'v': '5.131'}

    def _get_photos_info(self, owner_id: int, count: int, album_id: str) -> dict:
        url = self._base_url + 'photos.get'
        params = {
            'owner_id': owner_id,
            'album_id': album_id,
            'photo_sizes': 1,
            'extended': 1,
            'count': count
        }
        response = requests.get(url, params={**self.base_params, **params})
        response.raise_for_status()
        photos_info = response.json()
        if photos_info.get('error'):
            raise Exception(f'Error code {photos_info["error"]["error_code"]} -> {photos_info["error"]["error_msg"]}')
        return photos_info

    def get_max_size_photos(self, owner_id: int, count: int, album_id: str) -> list[dict]:
        photos_info = self._get_photos_info(owner_id, count, album_id)
        size_type = ('w', 'z', 'y', 'r', 'q', 'p', 'o', 'x', 'm', 's')
        owner_photos = []
        for photo in photos_info['response']['items']:
            for type_photo in size_type:
                filter_photo = self.filter_photos_by_size(photo, type_photo)
                if filter_photo:
                    owner_photos.append({
                        'file_name': self.generate_file_name(photo, owner_photos, filter_photo[0]['url']),
                        'size': filter_photo[0]['type'],
                        'origin_url': filter_photo[0]['url']
                    })
                    break
        return owner_photos

    @staticmethod
    def filter_photos_by_size(photo: dict, type_photo: str) -> list:
        return list(filter(lambda x: x['type'] == type_photo, photo['sizes']))

    @staticmethod
    def generate_file_name(photo: dict, owner_photos: list[dict], url: str) -> str:
        file_name = str(photo['likes']['count'])
        if any([i['file_name'][:-4] == file_name for i in owner_photos]):
            file_name += f'_{datetime.utcfromtimestamp(int(photo["date"])).strftime("%Y-%m-%d")}'
        found = re.search(r'\.(\w{3})\Z|\.(\w{3})\?', url).groups()
        format_photo = found[1] if not found[0] else found[0]
        file_name += f'.{format_photo}'
        return file_name
