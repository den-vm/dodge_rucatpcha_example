import io
import logging
import zipfile
import json
from datetime import datetime

from API.API_StatCustomsGovRu import view_captcha, check_captcha, unload_file_zip
from API.API_UnlockInRuCaptcha import decode_captcha, result_decode

file_path = f"C://для_нЕкиты_DATTSVT_{datetime.now():%d-%m-%Y %H-%M}//"

if __name__ == '__main__':
    with open("settings_app.json") as file_read:
        settings_app = json.load(file_read)
        period = settings_app["period"]
    response = view_captcha()
    image = response['content']
    key_captcha = response['keyCaptcha']
    key_response_captcha = decode_captcha(image)
    result_decode_captcha = result_decode(key_response_captcha, 0)
    result_check_captcha = check_captcha(key_captcha, result_decode_captcha)
    if result_check_captcha != "ok":
        logging.debug("Неверный ответ на каптчу")
    else:
        print("\nНачинаем скачивать файл...")
        file = unload_file_zip(key_captcha, period)
        zip_file = zipfile.ZipFile(io.BytesIO(file))
        zip_file.extractall(file_path)
        print(f"\nФайл успешно скачен\n\nПуть файла: {file_path}{zip_file.filelist[0].filename}")
