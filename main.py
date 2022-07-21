from vkphotos import VkPhotos
from yadisk import YandexDisk
from tokens import TOKEN_VK, TOKEN_YA


def upload_photos_vk_to_disk(token_vk: str, token_ya: str, vk_owner_id: int,
                             number_photos: int = 5, album_id: str = 'profile',
                             upload_log: bool = True, ya_base_folder: str = 'vk_photos_upload') -> None:
    """
    Функция сохраняет фотографии пользователя Vk в облачное хранилище Я.Диск.
    Для названий фотографий используется количество лайков, если количество лайков одинаково,
    то к названию добавляется дата загрузки.
    Фотографии на Я.Диск сохраняются в поддиректории с именем ID[id пользователя VK]_[ГГММДД]_[ЧЧ-ММ-СС]
    корневой директории '/VK_photos_upload'. Директории создаются программно.
    Информация по сохраненным фотографиям может быть сохранена в json-файл на локальной машине.
    Файл помещается в директорию ya_upload_log.
    Имя файла формируется в формате ID[id пользователя VK]_[ГГММДД]_[ЧЧ-ММ-СС].json

    :param token_vk: токен Vk. Подробнее https://dev.vk.com/api/access-token/implicit-flow-user
    :param token_ya: токен Я.Диск. Подробнее https://yandex.ru/dev/id/doc/dg/oauth/concepts/about.html
    :param vk_owner_id: id пользователя Vk.
    :param number_photos: по умолчанию значение 5. Кол-во фотографий для загрузки на Я.Диск.
    :param album_id: по умолчанию значение 'profile' (фотографии профиля). Возможные значения - 'wall', 'saved'.
    :param upload_log: по умолчанию значение True. Записывает в json-файл данные загруженных фотографий на Я.Диск.
    :param ya_base_folder: по умолчанию 'vk_photos_upload'. Имя базовой директории на Я.Диске для сохранения фото.
    :return: None
    """
    vk = VkPhotos(token=token_vk)
    ya = YandexDisk(token=token_ya)
    photos = vk.get_max_size_photos(owner_id=vk_owner_id, count=number_photos, album_id=album_id)
    ya.upload_files_to_disk(photos=photos, vk_owner_id=vk_owner_id, upload_log=upload_log,
                            ya_base_folder=ya_base_folder)


if __name__ == '__main__':
    upload_photos_vk_to_disk(token_vk=TOKEN_VK, token_ya=TOKEN_YA, vk_owner_id=1)
