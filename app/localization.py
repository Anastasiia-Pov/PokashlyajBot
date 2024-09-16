
# Команда /start
start_command = """Привет, {0}.
Данный чат-бот - является пет-проектом.
Чтобы продолжить со мной общение, пройди, пожалуйста регистрацию - /register.
Если хотите сменить язык бота - /change_language.
Прочитать о боте более подробно, можно воспользовавшись командой - /info.
Чтобы связаться с разработчиком - /support.
Если нашли ошибку - /help -> Сообщить об ошибке.
Проанализировать свой кашель - /load_voice.
------------------------------------------------
Hello, {0}.
This chat-bot is a pet-project.
To continue, you need to register first - /register.
To change the language - /change_language.
To know more about the bot - /info.
To contact the developer - /support.
To report an error - /help -> Report an error.
To analyze your cough - /load_voice."""

# Команда /help
help_command = {'ru': 'Возникли вопросы?\nЧем могу помочь?',
                'en': 'Do you have any questions? How can I help you'}


# Команда /info
info_command = {'ru': '''Данный бот является пет-проектом для практики навыков разработки ТГ-Ботов на языке программирования Python и фреймворка aiogram3.\n
PokashlajBot - бот для определения респираторных заболевания. Для начала пользователю необходимо зарегистрироваться в системе, указать: имя, возраст, пол и регион проживания.
Затем станет доступна команда /load_voice, бот попросит пользователя записать голосовое сообщение с кашлем, которое затем будет проанализировано моделью машинного обучения и отображен результат анализа.
На данный момент, реализована только бинарная классификация записей, т.е., бот может ответить о том, здоровый или нездоровый у пользователя кашель.''',
                'en': '''This bot is a pet project to practice TG-Bot development skills in Python programming language and with the use of aiogram3 framework.\n
PokashlajBot is a bot for detecting respiratory diseases. To start, the user needs to register in the system, specify: name, age, gender and region of residence.
Then the command /load_voice will be available, the bot will ask the user to record a voice message with cough, which will then be analyzed by ML-model and the result of the analysis will be displayed.
At the moment, only binary classification of recordings is implemented, i.e. the bot can answer whether the user has a healthy or unhealthy cough.'''}


# Команда /register - если пользователь уже зарегистрирова
double_register = {'ru': '''Вы уже зарегистрированы в системе.
Повторная регистрация не нужна.''',
                   'en': '''You've already registered in our system.
There is no need to register for the second time.'''}
not_registered = {'ru': 'Для использования данной функции, пройдите, пожалуйста, регистрацию - /register',
                  'en': 'If you want to use this function, please register first - /register'}

# Команда /support
support_command = {'ru': "Хотите связаться с разработчиком?",
                   'en': 'Do you want to contact the developer?'}

#
support_command_conntact_dev = {'ru': 'Связь с разработчиком',
                                'en': 'Contact the developer'}
support_command_git_dev = {'ru': 'Github разработчика',
                           'en': "Dev's Github"}


# Кнопки статистики
stat_command = {'ru': "Какая статистика Вас интересует?",
                'en': "Which statistics are you interested in?"}
# Статистика по возрасту
stat_button_age = {'ru': 'по возрасту',
                   'en': 'by age'}
# Статистика по региону
stat_button_region = {'ru': 'по региону',
                      'en': 'by region'}

# Кнопки в разделе /help - Информация о проекте
# Buttrons in command /help - Info about project
project_info = {'ru': '''<b>TG-BOT на  aiogram3</b>
Данный бот релиазован в качестве пет-проекта, с целью изучения фреймворка aiogram на языке Python, версии 3.12.2.
Целью проекта было реализовать чат-бота для акустического анализа респираторных заболевайни (COVID-19, туберкулез, и др.).
Пользователь отправляет запись (голосовое сообщение) в чат бот, с использованием модели машинного обучения осуществляется анализ записи и результат анализа отправляется пользователю.

Более подробная информация представлена в гит-репозитории - https://github.com/Anastasiia-Pov/PokashlyajBot''',
                'en': """<b>TG-BOT on aiogram3</b>
This TG-Bot is considered as a pet-project to get acquainted with aiogram asynchronous framework written in Python.
The project is implemented in virtual environment with Python version 3.12.2.
The main idea of the project was to implement a chatbot for acoustic analysis of respiratory diseases (such as COVID-19, tuberculosis, etc.).
The user sends a recording (a voice message) in the chatbot, using a ML-model to analyze the recordings and a user gets back the result.

More info is presented on git-repository - https://github.com/Anastasiia-Pov/PokashlyajBot"""}

# Регистрация пользователя
# Указание имени
register_name = {'ru': "Как я могу к Вам обращаться?",
                 'en': "What's your name?"}
# Текст на случай ошибки при узазании имени
register_name_error = {'ru': 'То, что вы отправили не похоже на имя.\n'
                             'Пожалуйста, введите ваше имя.\n'
                             'Если вы хотите прервать заполнение анкеты - '
                             'отправьте команду /cancel',
                       'en': "What you've written doesn't lool like a name.\n"
                             "Please write you name.\n"
                             "If you want to stop registation - "
                             "send /cancel command"}

# Указание возраста
register_age = {'ru': "{0}, укажите свой возраст",
                'en': "{0}, what's your age?"}
# Текст на случай ошибки при узазании возраста
register_age_error = {'ru': 'То, что вы отправили не похоже на возраст.\n'
                            'Пожалуйста, введите ваше имя.\n'
                            'Если вы хотите прервать заполнение анкеты - '
                            'отправьте команду /cancel',
                      'en': "What you have written doesn't look like age.\n"
                            "Please write your age.\n"
                            "If you want to stop registation - "
                            "send /cancel command"}

# Выбор пола
register_gender = {'ru': "Выберите, пожалуйста, свой пол",
                   'en': "Choose your gender"}
# Текст на случай ошибки при узазании региона вручную
register_gender_error = {'ru': 'Выберите пол из меню ниже.\n'
                               'Если вы хотите прервать заполнение анкеты - '
                               'отправьте команду /cancel',
                         'en': 'Choose gender from the menu below.\n'
                               "If you want to stop registation - "
                               "send /cancel command"}

# Выбор региона
register_region = {'ru': "Выберите, пожалуйста, свой регион",
                   'en': "Choose your region"}
# Текст на случай ошибки при узазании региона вручную
register_region_error = {'ru': 'Выберите регион из меню ниже.\n'
                               'Если вы хотите прервать заполнение анкеты - '
                               'отправьте команду /cancel',
                         'en': 'Choose region from the menu below.\n'
                               "If you want to stop registation - "
                               "send /cancel command"}

# Конец регистрации
end_registration = {'ru': "Спасибо! Регистрация завершена успешно!)",
                    'en': "Thank you! Registration completed successfully"}

# Saved data in DB after registration
db_info = {'ru': '''<b>Указанные данные</b>

Имя: {0}
Возраст: {1}
Пол: {2}
Регион: {3}''',
           'en': '''<b>Info you've written</b>

Name: {0}
Age: {1}
Gender: {2}
Region: {3}'''}

# Команда /cancel
cancel_command = {'ru': 'Вы вышли из машины состояний\n\n'
                        '- чтобы снова перейти к заполнению регистрационной анкеты - '
                        'отправьте команду /register\n'
                        '- чтобы посмотреть указанные ранее данные - '
                        'отправьте команду /registered_info\n'
                        '- чтобы изменить указанные ранее данные - '
                        'отправьте команду /change_registered_info',
                  'en': "You are out of FSM\n\n"
                        "- to complete registration - "
                        "send /register\n"
                        "- to view the previously specified data - "
                        "send /registered_info\n"
                        "- to change the previously specified data - "
                        "send /registered_info"}

# Любой случайный текст пользователя будет получать ответ:
random_text_answer = {'ru': '''Не совсем понимаю о чем вы.
Выберете команду из меню, чтобы мы могли продолжить общение''',
                      'en': """I don't quite understand what you mean.
Select a command from the menu so we can continue our conversation"""}

# Любое голосовое пользователя будет получать ответ:
random_voice_answer = {'ru': '''Если вы хотите приступить к анализу своего кашля нажмите команду /load_voice''',
                      'en': """if you want to analizy your cough, please sent /load_voice command"""}


report_error = {'ru': 'Сообщите нам о ней в группе поддержки: {0}',
                'en': 'You can report a bug by following this link {0}'}


placeholder = {'ru': 'Выберите пункт меню',
               'en': "Choose ftom the menu below"}

start_coughrecording_func = {'ru': 'Запишите, пожалуйста, голосовое сообщение с вашим кашлем.',
                             'en': 'Please, record a voice message with your cough.'}
user_sent_voice_mesage = {'ru': '''Спасибо, наша система приступила к анализу вашего кашля.
Пожалуйста, подождите, это может занять некоторое время.''',
                          'en': '''Thank you, our system have started to analyze you cough.
Please wait, it may take some time.'''}
waiting_message = {'ru': '''Анализ вашего кашля произведен успешно. Загружаем в систему для обработки.''',
                   'en': '''Your cough has been analyzed successfully. Loading into the system for processing.'''}

register_info_false = {'ru': 'Вас нет в нашей системе.',
                       'en': "We don't have any data about you in put system"}

change_user_info = {'ru': 'Вы хотите внести изменения в данные?',
                    'en': "Do you want to change some data"}

choose_data = {'ru': 'Какие данные вы хотите изменить?',
               'en': "What data do you want to update?"}
no_changes = {'ru': 'Хорошо. Вы можете внести изменения в любой момент по команде - /change_register_data',
              'en': 'Okay. You can change data anytime by calling comand - /change_register_data'}
name_change = {'ru': 'Давайте изменим имя. Как вас зовут?',
                         'en': "Let's change the name. What's your name?"}
age_change = {'ru': 'Давайте изменим возраст. Сколько вам лет?',
              'en': "Let's change the age. How old are you?"}
gender_change = {'ru': 'Давайте изменим пол. Выберите пол из меню ниже.',
                 'en': "Let's change the gender. Select a gender from the menu below."}
region_change = {'ru': 'Давайте изменим регион. Выберите регион из меню ниже.',
                 'en': "Let's change the region. Select a region from the menu below."}
successfull_changes = {'ru': 'Благодарю. Данные изменены.',
                       'en': "Thank you. Data has been changed."}


analysis_result_negative = {'ru': '''<b><i>В результате нашего анализа наша система классифицировала ваш кашель, как здоровый.
Но в любом случае, если у вас есть сомнения или вас что-то беспокоит, проконсультируйтесь со специалистом 👨‍⚕️</i></b>''',
                            'en': """<b><i>As a result of our analysis, our system has classified your cough as healthy.
But in any case, if you have doubts or are concerned about something, consult a specialist 👨‍⚕️</i></b>"""}

analysis_result_positive = {'ru': '''<b><i>В результате нашего анализа наша система классифицировала ваш кашель, как нездоровый.
Советуем проконсультироваться со специалистом 👨‍⚕️</i></b>''',
                            'en': """<b><i>As a result of our analysis, our system has classified your cough as unhealthy.
We advise you to consult a specialist 👨‍⚕️</i></b>"""}
