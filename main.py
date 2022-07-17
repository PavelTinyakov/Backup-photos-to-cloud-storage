from pprint import pprint

from vkphotos import VkPhotos
from yadisk import YandexDisk
from tokens import TOKEN_VK, TOKEN_YA


def main(token_vk, token_ya, vk_owner_id, number_photos=100):
    vk = VkPhotos(token=token_vk)
    ya = YandexDisk(token=token_ya)

    photos = vk.get_max_size_photos(owner_id=vk_owner_id, count=number_photos)
    ya.upload_files_to_disk(photos, vk_owner_id=vk_owner_id)


if __name__ == '__main__':
    main(token_vk=TOKEN_VK, token_ya=TOKEN_YA, vk_owner_id=51936827)

