from database.models import async_session
from database.models import User, User_lang, Cough_sounds
from sqlalchemy import select, update, delete, text


# язык бота пользователя:
async def set_lang(tg_id, lang):
    async with async_session() as session:
        user_language = {'Русский': 'ru', 'English': 'en'}
        user = await session.scalar(select(User_lang).where(User_lang.user_id == tg_id))
        if not user:
            set_lang = User_lang(user_id=tg_id,
                                 lang=user_language[lang])
            session.add(set_lang)
            await session.commit()
        elif user:
            user.lang = user_language[lang]
            await session.commit()


# подтягивание инфы о языке бота пользователя из БД:
async def get_lang(tg_id):
    async with async_session() as session:
        stmt = select(User_lang.lang).where(User_lang.user_id == tg_id)
        res = session.scalars(stmt)
        return await res


# Первичная регистрация пользователя:
async def set_user(user_tg_id, user_name, user_age, user_gender, user_region):
    async with async_session() as session:
        user_info = User(tg_id=user_tg_id,     # заполение поля id в телеграм
                         name=user_name,       # заполение поля name
                         age=user_age,         # заполение поля age
                         gender=user_gender,
                         region=user_region)   # заполение поля region
        session.add(user_info)
        await session.commit()


# Проверка пользователя: есть ли его tg_id в БД
async def check_user(user_tg_id):
    async with async_session() as session:
        flag = False
        user = await session.scalar(select(User).where(User.tg_id == user_tg_id))
        if user:
            flag = True
            return flag


async def get_user_info(user_tg_id):
    async with async_session() as session:
        query = select(User).where(User.tg_id == user_tg_id)
        result = await session.execute(query)
        user = result.scalar_one()
        return (user.name, user.age, user.gender, user.region)


# Получение статистики по возрасту:
async def stat_by_age():
    async with async_session() as session:
        stmt = select(User.age)
        res = session.scalars(stmt)
        return await res


# Получение статистики по региону:
async def stat_by_region():
    async with async_session() as session:
        stmt = select(User.region)
        res = session.scalars(stmt)
        return await res


# Запись в таблицу Cough_sounds
async def add_new_recording(tg_id, file_path):
    async with async_session() as session:
        set_new_voice = Cough_sounds(user_id=tg_id,
                                     sound=file_path)
        session.add(set_new_voice)
        await session.commit()


class UpdateUserInfo:
    async def change_name_func(user_tg_id, new_value):
        async with async_session() as session:
            result = await session.execute(select(User).filter(User.tg_id == user_tg_id))
            record = result.scalar_one_or_none()
            record.name = new_value
            await session.commit()

    async def change_age_func(user_tg_id, new_value):
        async with async_session() as session:
            result = await session.execute(select(User).filter(User.tg_id == user_tg_id))
            record = result.scalar_one_or_none()
            record.age = new_value
            await session.commit()

    async def change_gender_func(user_tg_id, new_value):
        async with async_session() as session:
            result = await session.execute(select(User).filter(User.tg_id == user_tg_id))
            record = result.scalar_one_or_none()
            record.gender = new_value
            await session.commit()

    async def change_region_func(user_tg_id, new_value):
        async with async_session() as session:
            result = await session.execute(select(User).filter(User.tg_id == user_tg_id))
            record = result.scalar_one_or_none()
            record.region = new_value
            await session.commit()
