import os
import glob
import subprocess
import numpy as np
import pandas as pd
import soundfile as sf


# конвертируем .ogg файл голосового сообщения в wav-файл для последующей обработки opensmile
async def convert_oga_to_wav(filepath):
    voice_messages_path = 'voice_messages/'
    output_path = voice_messages_path + str(filepath).split('/')[-1].split('.')[0] + '.wav'
    data, samplerate = sf.read(filepath)
    sf.write(output_path, data, samplerate)
    return output_path


# извлечение вектора признаков с помощью opensmile
async def opensmile_extractor(file, save_csv_path):
    config = "opensmile-master/config/gemaps/v01b/GeMAPSv01b.conf"  # заполняемое поле: конфигурационный файл - файл с признаками из opensmile
    smilextract = 'opensmile-master/build/progsrc/smilextract/SMILExtract'  # абсолютный путь до файла экстрактора

    opensmile_cmd = [smilextract, '-C', config, '-I', file, '-csvoutput', save_csv_path]
    execution_result = subprocess.check_call(opensmile_cmd)


# преоразование записи в вектор для подачи на вход ml-модели
async def transform_func(file_path):
    np_features = pd.read_csv(file_path, sep=';')
    np_features.pop('name')
    np_features.pop('frameTime')
    np_features = np_features.to_numpy()
    return np_features.reshape(1, -1)
