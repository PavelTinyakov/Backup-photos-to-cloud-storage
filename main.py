from vkphotos import VkPhotos
from yadisk import YandexDisk
from tokens import TOKEN_VK, TOKEN_YA


def upload_files_vk_to_disk(token_vk: str, token_ya: str, vk_owner_id: int, number_photos: int = 5,
                            album_id: str = 'profile', upload_log: bool = True) -> None:
    vk = VkPhotos(token=token_vk)
    ya = YandexDisk(token=token_ya)
    photos = vk.get_max_size_photos(owner_id=vk_owner_id, count=number_photos, album_id=album_id)
    ya.upload_files_to_disk(photos=photos, vk_owner_id=vk_owner_id, upload_log=upload_log)


if __name__ == '__main__':
    upload_files_vk_to_disk(token_vk=TOKEN_VK, token_ya=TOKEN_YA, vk_owner_id=51936827)
