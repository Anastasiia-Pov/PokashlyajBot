from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
# from database.requests import stat_by_age

from config import tg_url, git_url
from app.localization import (support_command_conntact_dev,
                              support_command_git_dev)


# chosing the language
lang_btn = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Русский'),
     KeyboardButton(text='English')]],
                                resize_keyboard=True,
                                input_field_placeholder="Выберите язык системы\nSelect language of the chat-bot",
                                one_time_keyboard=True)


# /help
help_btn = {'ru': ReplyKeyboardMarkup(keyboard=[
                  [KeyboardButton(text='Информация о проекте')],
                  [KeyboardButton(text='Сообщить об ошибке')]],
                  resize_keyboard=True,
                  input_field_placeholder="Выберите пункт меню"),
            'en': ReplyKeyboardMarkup(keyboard=[
                [KeyboardButton(text='Info about the project')],
                [KeyboardButton(text='Report an error')]],
                resize_keyboard=True,
                input_field_placeholder="Choose an option below...")}


# /help для админов
admin_help_btn = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Статистика')],
    [KeyboardButton(text='Информация о проекте')],
    [KeyboardButton(text='Сообщить об ошибке')]],
    resize_keyboard=True,
    input_field_placeholder="Выберите пункт меню...")


stat_btn = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='по возрасту',
                          callback_data='по возрасту')],
    [InlineKeyboardButton(text='по региону',
                          callback_data='по региону')]])


settings_tg = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Telegram',
                          url=tg_url)],
    [InlineKeyboardButton(text='Github',
                          url=git_url)]])


# клавиатура выбора пола при регистрации
gender_btn = {'ru': ReplyKeyboardMarkup(keyboard=[
                    [KeyboardButton(text='Женщина'), KeyboardButton(text='Мужчина')]],
                    resize_keyboard=True,
                    input_field_placeholder="Выберите пункт меню...",
                    one_time_keyboard=True),
              'en': ReplyKeyboardMarkup(keyboard=[
                    [KeyboardButton(text='Female'), KeyboardButton(text='Male')]],
                    resize_keyboard=True,
                    input_field_placeholder="Choose option below...",
                    one_time_keyboard=True)}


# клавиатура для выбора региона при регистрации
region_btn = {'ru': ReplyKeyboardMarkup(keyboard=[
                    [KeyboardButton(text='Азиатский регион')],
                    [KeyboardButton(text='Европа'), KeyboardButton(text='Латинская Америка')],
                    [KeyboardButton(text='Россия'), KeyboardButton(text='США')]],
                    resize_keyboard=True,
                    input_field_placeholder="Выберите пункт меню...",
                    one_time_keyboard=True),
              'en': ReplyKeyboardMarkup(keyboard=[
                    [KeyboardButton(text='Asia')],
                    [KeyboardButton(text='Europe'),
                     KeyboardButton(text='Latin America')],
                    [KeyboardButton(text='Russia'), KeyboardButton(text='USA')]],
                    resize_keyboard=True,
                    input_field_placeholder="Choose option below...",
                    one_time_keyboard=True)}


change_data = {'ru': InlineKeyboardMarkup(inline_keyboard=[
                     [InlineKeyboardButton(text='Да',
                                           callback_data='Да')],
                     [InlineKeyboardButton(text='Нет',
                                           callback_data='Нет')]]),
               'en': InlineKeyboardMarkup(inline_keyboard=[
                     [InlineKeyboardButton(text='Yes',
                                           callback_data='Да')],
                     [InlineKeyboardButton(text='No',
                                           callback_data='Нет')]])}


choose_section = {'ru': InlineKeyboardMarkup(inline_keyboard=[
                        [InlineKeyboardButton(text='Имя',
                                              callback_data='name')],
                        [InlineKeyboardButton(text='Возраст',
                                              callback_data='age')],
                        [InlineKeyboardButton(text='Пол',
                                              callback_data='gender')],
                        [InlineKeyboardButton(text='Регион',
                                              callback_data='region')]]),
                  'en': InlineKeyboardMarkup(inline_keyboard=[
                        [InlineKeyboardButton(text='Name',
                                              callback_data='name')],
                        [InlineKeyboardButton(text='Age',
                                              callback_data='age')],
                        [InlineKeyboardButton(text='Gender',
                                              callback_data='gender')],
                        [InlineKeyboardButton(text='Region',
                                              callback_data='region')]])}
