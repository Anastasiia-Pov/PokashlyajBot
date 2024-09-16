import logging
import os
from pathlib import Path
import pickle
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
from aiogram.filters import ChatMemberUpdatedFilter, KICKED
from aiogram.types import ChatMemberUpdated, CallbackQuery
from aiogram.filters import BaseFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import asyncio
import soundfile as sf
from app import localization
import app.keyboards as kb
import database.requests as rq
from config import admin_id, support_chat, model_path, absolute_path_csvs, voice_messages_path
from sub_processes.diagrams import make_graph_age, make_graph_region
from research_on_features.extract_gemaps import (convert_oga_to_wav,
                                                 opensmile_extractor,
                                                 transform_func)
from app.FSMs import (Register, CoughRecording, ChangeName, ChangeAge,
                      ChangeGender, ChangeRegion)
# from app.middlewares import TestMiddleware

log = logging.getLogger(__name__)
router = Router()

# Cписок администраторов бота
admin_ids: list[int] = [int(admin_id)]
# Middleware
# router.message.middleware(TestMiddleware())


# получение информации о языке пользователя из БД
async def get_lang_from_db(user_id):
    language = await rq.get_lang(user_id)
    language = language.first()
    return language


# Команда "/start"
# Command "/start"
@router.message(Command('start'))
async def start(message: Message):
    await rq.set_lang(message.from_user.id, 'Русский')
    await message.answer(
        localization.start_command.format(message.from_user.username)
                         )


# Хэндлер, который сработает, если пользователь захочет прервать регистрацию
@router.message(Command('cancel'))
async def process_cancel_command_state(message: Message, state: FSMContext):
    language = await get_lang_from_db(message.from_user.id)
    await message.answer(
        text=localization.cancel_command[language])
    # Сбрасываем состояние и очищаем данные, полученные внутри состояний
    await state.clear()


# Хэндлер для выбора языка бота:
# Handler to choose bot's language:
@router.message(Command('change_language'))
async def change_language(message: Message):
    await message.answer(text='''Выберите язык в меню ниже\n
Select langiage in the menu below''',
                         reply_markup=kb.lang_btn)


# Хэндлер для смены языка на русский
# Handler to change language into Russian
@router.message(F.text == 'Русский')
async def user_info_ru(message: Message):
    await rq.set_lang(message.from_user.id,
                      'Русский')
    user_lang = await rq.get_lang(message.from_user.id)
    await message.answer(f"""Вы сменили язык бота.
Вы можете изменить свой выбор с помощью команды /change_language.\n
Ваш язык системы: {''.join(user_lang.all())}""")


# Хэндлер для смены языка на английский
# Handler to change language into English
@router.message(F.text == 'English')
async def user_info_en(message: Message):
    await rq.set_lang(message.from_user.id,
                      'English')
    user_lang = await rq.get_lang(message.from_user.id)
    await message.answer(f"""You've changed the bot language.
You can always update it by calling /change_language command.\n
The language of the system: {''.join(user_lang.all())}""")


# Команда "/info"
# Command "/info"
@router.message(Command(commands=['info']))
async def process_start_command(message: Message):
    language = await get_lang_from_db(message.from_user.id)
    await message.answer(localization.info_command[language], parse_mode='html')


# Команда "/support"
# ПРОБЛЕМА С ЦИКЛИЧНОСТЬЮ ИМПОРТОВ
@router.message(Command(commands=['support']))
async def support(message: Message):
    language = await get_lang_from_db(message.from_user.id)
    await message.answer(text=localization.support_command[language],
                         reply_markup=kb.settings_tg)


# Команда "/help"
# Command "/help"
@router.message(Command('help'))
async def help_btn(message: Message):
    language = await get_lang_from_db(message.from_user.id)
    if message.from_user.id in admin_ids:
        await message.answer(text=localization.help_command[language],
                             reply_markup=kb.admin_help_btn)
    else:
        await message.answer(text=localization.help_command[language],
                             reply_markup=kb.help_btn[language])


# help ReplyKeyboardMarkup - Информация о проекте
@router.message(F.text == 'Информация о проекте')
@router.message(F.text == 'Info about the project')
async def project_info(message: Message):
    language = await get_lang_from_db(message.from_user.id)
    await message.answer(localization.project_info[language],
                         parse_mode='html')


# help ReplyKeyboardMarkup - Сообщить об ошибке
@router.message(F.text == 'Сообщить об ошибке')
@router.message(F.text == 'Report an error')
async def report_error(message: Message):
    language = await get_lang_from_db(message.from_user.id)
    await message.answer(localization.report_error[language].format(support_chat))


# Показать пользователю информацию, указанную при регистрации
@router.message(Command('registered_info'))
async def user_info(message: Message):
    res = await rq.check_user(message.from_user.id)
    gender_en = {'Ж': 'Female',
                 'М': 'Male'}
    regions_en = {'Азиатский регион': 'Asia',
                  'Европа': 'Europe',
                  'Латинская Америка': 'Latin America',
                  'Россия': 'Russia',
                  'США': 'USA'}
    if res:
        language = await get_lang_from_db(message.from_user.id)
        user_info = await rq.get_user_info(message.from_user.id)
        name, age, gender, region = user_info
        await message.answer(text=localization.db_info[language].format(name,
                                                                        age,
                                                                        gender if language == 'ru' else gender_en[gender],
                                                                        region if language == 'ru' else regions_en[region]),
                             parse_mode='html')
    else:
        await message.answer(text=localization.register_info_false[language])


# /help ReplyKeyboardMarkup - Статистика:
@router.message(F.text == 'Статистика')
async def statistics(message: Message):
    await message.answer("Какая статистика Вас интересует?",
                         reply_markup=kb.stat_btn)


# InlineKeyboardButton - по возрасту:
@router.callback_query(F.data == 'по возрасту')
async def stat_by_age(callback: CallbackQuery):
    all_users = await rq.stat_by_age()
    res_photo = make_graph_age(all_users.all())
    diagram = FSInputFile('sub_processes/age.png')
    await callback.answer()
    await callback.message.answer(text='Cтатистика пользователей по возрасту:')
    await callback.bot.send_photo(chat_id=callback.message.chat.id,
                                  photo=diagram)


# InlineKeyboardButton - по региону:
@router.callback_query(F.data == 'по региону')
async def stat_by_region(callback: CallbackQuery):
    all_users = await rq.stat_by_region()
    res_photo = make_graph_region(all_users.all())
    diagram = FSInputFile('sub_processes/region.png')
    await callback.answer()
    await callback.message.answer(text='Cтатистика пользователей по региону:')
    await callback.bot.send_photo(chat_id=callback.message.chat.id,
                                  photo=diagram)


# Изменить информацию пользователю, указанную при регистрации
@router.message(Command('change_register_data'))
async def change_user_info(message: Message):
    res = await rq.check_user(message.from_user.id)
    language = await get_lang_from_db(message.from_user.id)
    if not res:
        await message.answer(localization.register_info_false[language])
    else:
        await user_info(message)
        language = await get_lang_from_db(message.from_user.id)
        await message.answer(text=localization.change_user_info[language],
                             reply_markup=kb.change_data[language])


@router.callback_query(F.data.in_(['Да', 'Нет']))
async def change_data(callback: CallbackQuery):
    language = await get_lang_from_db(callback.message.chat.id)
    if callback.data == 'Yes' or callback.data == 'Да':
        await callback.message.delete()
        await callback.message.answer(localization.choose_data[language],
                                      reply_markup=kb.choose_section[language])
    else:
        await callback.message.answer(localization.no_changes[language])
        await callback.message.delete()


@router.callback_query(F.data.in_(['name', 'age', 'gender', 'region']))
async def change_section(callback: CallbackQuery, state: FSMContext):
    language = await get_lang_from_db(callback.message.chat.id)
    section = callback.data
    if section == 'name':
        await callback.message.answer(localization.name_change[language])
        await state.set_state(ChangeName.changed_name)
        await callback.answer()
    elif section == 'age':
        await callback.message.answer(localization.age_change[language])
        await state.set_state(ChangeAge.changed_age)
        await callback.answer()
    elif section == 'gender':
        await callback.message.answer(localization.gender_change[language],
                                      reply_markup=kb.gender_btn[language])
        await state.set_state(ChangeGender.changed_gender)
        await callback.answer()
    elif section == 'region':
        await callback.message.answer(localization.region_change[language],
                                      reply_markup=kb.region_btn[language])
        await state.set_state(ChangeRegion.changed_region)
        await callback.answer()


# Изменение данных - изменение имени пользователем
@router.message(ChangeName.changed_name, F.text.isalpha())
async def change_name(message: Message, state: FSMContext):
    '''Изменение имени зарегистрированного пользователя'''
    await state.update_data(changed_name=message.text)
    user_id = message.from_user.id
    data = await state.get_data()
    language = await get_lang_from_db(user_id)
    await state.update_data(changed_name=message.from_user.id)
    await rq.UpdateUserInfo.change_name_func(user_id, data['changed_name'])
    await message.answer(localization.successfull_changes[language])
    await state.clear()


# Изменение данных - изменение возраста пользователем
@router.message(ChangeAge.changed_age, F.text.isdigit())
async def change_age(message: Message, state: FSMContext):
    '''Изменение возраста зарегистрированного пользователя'''
    await state.update_data(changed_age=message.text)
    user_id = message.from_user.id
    data = await state.get_data()
    language = await get_lang_from_db(user_id)
    await state.update_data(changed_age=message.from_user.id)
    await rq.UpdateUserInfo.change_age_func(user_id, data['changed_age'])
    await message.answer(localization.successfull_changes[language])
    await state.clear()


# Изменение данных - изменение пола пользователем на женский
@router.message(ChangeGender.changed_gender, F.text == 'Female')
@router.message(ChangeGender.changed_gender, F.text == 'Женщина')
async def change_gender_female(message: Message, state: FSMContext):
    '''Изменение пола зарегистрированного пользователя'''
    language = await get_lang_from_db(message.from_user.id)
    await state.update_data(changed_gender='Ж')
    user_id = message.from_user.id
    data = await state.get_data()
    await rq.UpdateUserInfo.change_gender_func(user_id, data['changed_gender'])
    await message.answer(localization.successfull_changes[language])
    await state.clear()


# Изменение данных - изменение пола пользователем на мужской
@router.message(ChangeGender.changed_gender, F.text == 'Мужчина')
@router.message(ChangeGender.changed_gender, F.text == 'Male')
async def change_gender_male(message: Message, state: FSMContext):
    '''Изменение пола зарегистрированного пользователя'''
    language = await get_lang_from_db(message.from_user.id)
    await state.update_data(changed_gender='М')
    user_id = message.from_user.id
    data = await state.get_data()
    await rq.UpdateUserInfo.change_gender_func(user_id, data['changed_gender'])
    await message.answer(localization.successfull_changes[language])
    await state.clear()


@router.message(ChangeRegion.changed_region, F.text == 'Азиатский регион')
@router.message(ChangeRegion.changed_region, F.text == 'Asia')
async def change_region_asia(message: Message, state: FSMContext):
    language = await get_lang_from_db(message.from_user.id)
    await state.update_data(changed_region='Азиатский регион')
    user_id = message.from_user.id
    data = await state.get_data()
    await rq.UpdateUserInfo.change_region_func(user_id, data['changed_region'])
    await message.answer(localization.successfull_changes[language])
    await state.clear()


@router.message(ChangeRegion.changed_region, F.text == 'Европа')
@router.message(ChangeRegion.changed_region, F.text == 'Europe')
async def change_region_europe(message: Message, state: FSMContext):
    language = await get_lang_from_db(message.from_user.id)
    await state.update_data(changed_region='Европа')
    user_id = message.from_user.id
    data = await state.get_data()
    await rq.UpdateUserInfo.change_region_func(user_id, data['changed_region'])
    await message.answer(localization.successfull_changes[language])
    await state.clear()


@router.message(ChangeRegion.changed_region, F.text == 'Латинская Америка')
@router.message(ChangeRegion.changed_region, F.text == 'Latin America')
async def change_region_latin(message: Message, state: FSMContext):
    language = await get_lang_from_db(message.from_user.id)
    await state.update_data(changed_region='Латинская Америка')
    user_id = message.from_user.id
    data = await state.get_data()
    await rq.UpdateUserInfo.change_region_func(user_id, data['changed_region'])
    await message.answer(localization.successfull_changes[language])
    await state.clear()


@router.message(ChangeRegion.changed_region, F.text == 'Russia')
@router.message(ChangeRegion.changed_region, F.text == 'Россия')
async def change_region_russia(message: Message, state: FSMContext):
    language = await get_lang_from_db(message.from_user.id)
    await state.update_data(changed_region='Россия')
    user_id = message.from_user.id
    data = await state.get_data()
    await rq.UpdateUserInfo.change_region_func(user_id, data['changed_region'])
    await message.answer(localization.successfull_changes[language])
    await state.clear()


@router.message(ChangeRegion.changed_region, F.text == 'США')
@router.message(ChangeRegion.changed_region, F.text == 'USA')
async def change_region_usa(message: Message, state: FSMContext):
    language = await get_lang_from_db(message.from_user.id)
    await state.update_data(changed_region='США')
    user_id = message.from_user.id
    data = await state.get_data()
    await rq.UpdateUserInfo.change_region_func(user_id, data['changed_region'])
    await message.answer(localization.successfull_changes[language])
    await state.clear()


# Команда "/register"
# Регистрация пользователя: запуск
@router.message(Command('register'))
async def register_step_one(message: Message, state: FSMContext):
    '''Проверка на наличие tg_id в БД:
    при наличие выдаст сообщение о наличии регистрации,
    в противном случае начнется процесс регистрации'''
    res = await rq.check_user(message.from_user.id)
    language = await get_lang_from_db(message.from_user.id)
    if res:
        await message.answer(text=localization.double_register[language])
    else:
        await state.set_state(Register.fill_name)
        await message.answer(localization.register_name[language])


# Команда "/register"
@router.message(Register.fill_name, F.text.isalpha())
async def register_name(message: Message, state: FSMContext):
    '''Регистрация пользователя: ввод имени'''
    language = await get_lang_from_db(message.from_user.id)
    await state.update_data(fill_tg_id=message.from_user.id)
    await state.update_data(fill_name=message.text)
    await state.set_state(Register.fill_age)
    await message.answer(localization.register_age[language].format(message.text))


# Хэндлер на проверку введенного имени
@router.message(Register.fill_name)
@router.message(ChangeName.changed_name)
async def warning_not_name(message: Message):
    '''Если (введенное имя) строка состоит не только из букв -
    выведет сообщение об ошибке'''
    language = await get_lang_from_db(message.from_user.id)
    await message.answer(
        text=localization.register_name_error[language])


# Рестрация пользователя: ввод возраста
@router.message(Register.fill_age, F.text.isdigit())
async def register_age(message: Message, state: FSMContext):
    '''Регистрация пользователя: ввод возраста'''
    language = await get_lang_from_db(message.from_user.id)
    await state.update_data(fill_age=int(message.text))
    await state.set_state(Register.fill_gender)
    await message.answer(localization.register_gender[language],
                         reply_markup=kb.gender_btn[language])


# Проверка введенного возраста
@router.message(Register.fill_age)
@router.message(ChangeAge.changed_age)
async def warning_not_age(message: Message):
    '''Если введенный возраст содержит отличные от цифр символы -
    выведет сообщение об ошибке'''
    language = await get_lang_from_db(message.from_user.id)
    await message.answer(
        text=localization.register_age_error[language])


# Рестрация пользователя: ввод пола
@router.message(Register.fill_gender, F.text == 'Female')
@router.message(Register.fill_gender, F.text == 'Женщина')
async def register_gender_female(message: Message, state: FSMContext):
    '''Регистрация пользователя: ввод пола'''
    language = await get_lang_from_db(message.from_user.id)
    await state.update_data(fill_gender='Ж')
    await state.set_state(Register.fill_region)
    await message.answer(localization.register_region[language],
                         reply_markup=kb.region_btn[language])


# Рестрация пользователя: ввод пола
@router.message(Register.fill_gender, F.text == 'Мужчина')
@router.message(Register.fill_gender, F.text == 'Male')
async def register_gender_male(message: Message, state: FSMContext):
    '''Регистрация пользователя: ввод пола'''
    language = await get_lang_from_db(message.from_user.id)
    await state.update_data(fill_gender='М')
    await state.set_state(Register.fill_region)
    await message.answer(localization.register_region[language],
                         reply_markup=kb.region_btn[language])


# Хэндлер
# если пол будет введен с клавиатуры
@router.message(Register.fill_gender, F.text)
@router.message(ChangeGender.changed_gender, F.text)
async def warning_not_gender(message: Message):
    language = await get_lang_from_db(message.from_user.id)
    await message.answer(
        text=localization.register_gender_error[language])


# Обработка region_btn(ReplyKeyboardMarkup) - Азиатский регион:
@router.message(Register.fill_region, F.text == 'Азиатский регион')
@router.message(Register.fill_region, F.text == 'Asia')
async def register_region_asia(message: Message, state: FSMContext):
    language = await get_lang_from_db(message.from_user.id)
    await state.update_data(fill_region='Азиатский регион')
    # создаем объект Person для добавления в БД
    data = await state.get_data()
    await message.answer(localization.end_registration[language])
    await rq.set_user(data['fill_tg_id'],
                      data['fill_name'],
                      data['fill_age'],
                      data['fill_gender'],
                      data['fill_region'])
    await state.clear()


# Обработка region_btn(ReplyKeyboardMarkup) - Европа:
@router.message(Register.fill_region, F.text == 'Европа')
@router.message(Register.fill_region, F.text == 'Europe')
async def register_region_europe(message: Message, state: FSMContext):
    language = await get_lang_from_db(message.from_user.id)
    await state.update_data(fill_region='Европа')
    data = await state.get_data()
    await message.answer(localization.end_registration[language])
    await rq.set_user(data['fill_tg_id'],
                      data['fill_name'],
                      data['fill_age'],
                      data['fill_gender'],
                      data['fill_region'])
    await state.clear()


# Обработка region_btn(ReplyKeyboardMarkup) - Латинская Америка:
@router.message(Register.fill_region, F.text == 'Латинская Америка')
@router.message(Register.fill_region, F.text == 'Latin America')
async def register_region_latinam(message: Message, state: FSMContext):
    language = await get_lang_from_db(message.from_user.id)
    await state.update_data(fill_region='Латинская Америка')
    data = await state.get_data()
    await message.answer(localization.end_registration[language])
    await rq.set_user(data['fill_tg_id'],
                      data['fill_name'],
                      data['fill_age'],
                      data['fill_gender'],
                      data['fill_region'])
    await state.clear()


# Обработка region_btn(ReplyKeyboardMarkup) - Россия:
@router.message(Register.fill_region, F.text == 'Россия')
@router.message(Register.fill_region, F.text == 'Russia')
async def register_region_russia(message: Message, state: FSMContext):
    language = await get_lang_from_db(message.from_user.id)
    await state.update_data(fill_region='Россия')
    data = await state.get_data()
    await message.answer(localization.end_registration[language])
    await rq.set_user(data['fill_tg_id'],
                      data['fill_name'],
                      data['fill_age'],
                      data['fill_gender'],
                      data['fill_region'])
    await state.clear()


# Обработка region_btn(ReplyKeyboardMarkup) - США:
@router.message(Register.fill_region, F.text == 'США')
@router.message(Register.fill_region, F.text == 'USA')
async def register_region_usa(message: Message, state: FSMContext):
    language = await get_lang_from_db(message.from_user.id)
    await state.update_data(fill_region='США')
    data = await state.get_data()
    await message.answer(localization.end_registration[language])
    await rq.set_user(data['fill_tg_id'],
                      data['fill_name'],
                      data['fill_age'],
                      data['fill_gender'],
                      data['fill_region'])
    await state.clear()


# Хэндлер
# если регион будет введен с клавиатуры
@router.message(Register.fill_region, F.text)
@router.message(ChangeRegion.changed_region, F.text)
async def warning_not_region(message: Message):
    language = await get_lang_from_db(message.from_user.id)
    await message.answer(
        text=localization.register_region_error[language])


# Хэндлер для запуска нейронки:
# Сначала проверится регистрация пользователя, затем будет предложено записать сообщение
@router.message(Command('load_voice'))
async def load_voice(message: Message, state: FSMContext):
    '''Проверка на наличие tg_id в БД:
    при наличии пользователя в БД - продолжится процесс записи и анализа кашля,
    в противном случае будет предложено пройти регистрацию'''
    res = await rq.check_user(message.from_user.id)
    language = await get_lang_from_db(message.from_user.id)
    if res:
        await message.answer(localization.start_coughrecording_func[language])
        await state.set_state(CoughRecording.record_voice)
    else:
        await message.answer(localization.not_registered[language])


# Скачивание голосового сообщения пользователя
@router.message(CoughRecording.record_voice, F.voice)
async def process_voice(message: Message, state: FSMContext):
    language = await get_lang_from_db(message.from_user.id)
    # сохранение файла
    path = 'voice_messages/'
    file_id = message.voice.file_id
    file = await message.bot.get_file(file_id)
    file_path = file.file_path
    file_on_disk = Path(path, file_path.split('/')[-1])
    await message.bot.download_file(file_path, destination=file_on_disk)
    path_to_wav = await convert_oga_to_wav(file_on_disk)
    # добавление записи в таблицу о новом голосовом от пользователя
    await rq.add_new_recording(message.from_user.id, str(path_to_wav))
    # сообщение о получении голосового и запуске обработчика
    await message.answer(localization.user_sent_voice_mesage[language])
    # результат извлечения признаков - путь до csv-файла
    csv_path = os.path.join(absolute_path_csvs, str(file_on_disk).split('/')[-1].split('.')[0] + '.csv')
    # извлечение признаков и сохранение в csv-файл
    features_extraction = await opensmile_extractor(str(path_to_wav), csv_path)
    input_vector = await transform_func(csv_path)
    await asyncio.sleep(2)
    # ЗАПУСК КЛАССИФИКАТОРА
    with open(model_path, 'rb') as picklefile:
        saved_model = pickle.load(picklefile)
    result = int(saved_model.predict(input_vector)) # результат классификации
    await asyncio.sleep(2)
    if result == 0:
        await message.answer(localization.analysis_result_negative[language],
                             parse_mode='html')
    elif result == 1:
        await message.answer(localization.analysis_result_positive[language],
                             parse_mode='html')
    await state.clear()


# Хэндлер будет срабатывать на блокировку бота пользователем
@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=KICKED))
async def process_user_blocked_bot(event: ChatMemberUpdated):
    print(f'Пользователь {event.from_user.id} заблокировал бота')


# Хэндлер
# если введен текст с клавиатуры - бот попросит выбрать команду из меню
@router.message(F.text)
async def random_text(message: Message):
    language = await get_lang_from_db(message.from_user.id)
    await message.answer(localization.random_text_answer[language])


# Хэндлер
# если введен текст с клавиатуры - бот попросит выбрать команду из меню
@router.message(F.voice)
async def random_voice(message: Message):
    language = await get_lang_from_db(message.from_user.id)
    await message.answer(localization.random_voice_answer[language])
