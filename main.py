from __future__ import annotations
from typing import Any, Awaitable, Callable, Dict

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.types import (Message, CallbackQuery, InlineKeyboardMarkup,
                           InlineKeyboardButton, PhotoSize,
                           TelegramObject, User)
from aiogram.fsm.storage.redis import RedisStorage, Redis
from config import Config, load_config
from lexicon import LEXICON_RU, LEXICON_EN
from main_button import set_main_menu

config: Config = load_config()
BOT_TOKEN: str = config.tg_bot.token

redis = Redis(host='localhost')
storage = RedisStorage(redis=redis) 

# Создаем объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=storage)

# Создаем "базу данных" пользователей
users_db: dict[int, dict[str, str | int | bool]] = {}


# Создаём словарь для выбора перевода
_translations = {
    'default': 'en',
    'ru': LEXICON_RU,
    'en': LEXICON_EN
}

# Добавляем полученный словарь в данные к диспетчеру
dp['_translations'] = _translations


# Cоздаем класс, наследуемый от StatesGroup, для группы состояний нашей FSM
class FSMFillForm(StatesGroup):
    fill_name = State()
    fill_age = State()
    fill_gender = State()
    upload_photo = State()
    fill_education = State()
    fill_wish_news = State()


# Создаём общую внешнюю мидлварь для выбора языка текстов
@dp.update.outer_middleware()
async def translate_middleware(
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable],
        event: TelegramObject,
        data: Dict[str, Any]
):
    user: User = data.get('event_from_user')

    if user is None:
        return await handler(event, data)

    user_lang = user.language_code
    translate = data.get('_translations')

    i18n = translate.get(user_lang)
    if i18n is None:
        data['i18n'] = translate[translate['default']]
    else:
        data['i18n'] = i18n

    return await handler(event, data)


# Этот хэндлер будет срабатывать на команду /start вне состояний
# и предлагать перейти к заполнению анкеты, отправив команду /fillform
@dp.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message, i18n: dict[str, str], bot: Bot, state: FSMContext):
    await set_main_menu(bot)
    await message.answer(text=i18n.get('/start'))


# Этот хэндлер будет срабатывать на команду "/cancel" в состоянии
# по умолчанию и сообщать, что эта команда работает внутри машины состояний
@dp.message(Command(commands=['cancel']), StateFilter(default_state))
async def process_cancel_command(message: Message, i18n: dict[str, str]):
    await message.answer(text=i18n.get('/cancel'))


# Этот хэндлер будет срабатывать на команду "/cancel" в любых состояниях,
# кроме состояния по умолчанию, и отключать машину состояний
@dp.message(Command(commands=['cancel']), ~StateFilter(default_state))
async def process_cancel_state_command(message: Message, i18n: dict[str, str], state: FSMContext):
    await message.answer(text=i18n.get('/cancel~'))
    # Сбрасываем состояние и очищаем данные, полученные внутри состояний
    await state.clear()


# Этот хэндлер будет срабатывать на команду /fillform
# и переводить бота в состояние ожидания ввода имени
@dp.message(Command(commands=['fillform']), StateFilter(default_state))
async def process_fillform_command(message: Message, state: FSMContext, i18n: dict[str, str]):
    await message.answer(text=i18n.get('/fillform'))
    # Устанавливаем состояние ожидания ввода имени
    await state.set_state(FSMFillForm.fill_name)


# Этот хэндлер будет срабатывать, если введено корректное имя
# и переводить в состояние ожидания ввода возраста
@dp.message(StateFilter(FSMFillForm.fill_name), F.text.isalpha())
async def process_name_set(message: Message, state: FSMContext, i18n: dict[str, str]):
    # Cохраняем введенное имя в хранилище по ключу "name"
    await state.update_data(name=message.text)
    await message.answer(text=i18n.get('thank_name'))
    # Устанавливаем состояние ожидания ввода возраста
    await state.set_state(FSMFillForm.fill_age)


# Этот хэндлер будет срабатывать, если во время ввода имени
# будет введено что-то некорректное
@dp.message(StateFilter(FSMFillForm.fill_name))
async def warning_name_set(message: Message, i18n: dict[str, str]):
    await message.answer(text=i18n.get('not_name'))


# Этот хэндлер будет срабатывать, если введен корректный возраст
# и переводить в состояние выбора пола
@dp.message(StateFilter(FSMFillForm.fill_age),
            lambda x: x.text.isdigit() and 4 <= int(x.text) <= 120)
async def process_age_set(message: Message, state: FSMContext, i18n: dict[str, str]):
    await state.update_data(age=message.text)
    male_button = InlineKeyboardButton(
        text=i18n.get('male_gender'),
        callback_data='male_gender'
    )
    female_button = InlineKeyboardButton(
        text=i18n.get('female_gender'),
        callback_data='female_gender'
    )
    unknown_button = InlineKeyboardButton(
        text=i18n.get('unknown_gender'),
        callback_data='undefined_gender'
    )
    keyboard: list[list[InlineKeyboardButton]] = [
        [male_button, female_button],
        [unknown_button]
    ]
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    await message.answer(
        text=i18n.get('thank_age'),
        reply_markup=markup
    )
    await state.set_state(FSMFillForm.fill_gender)


# Этот хэндлер будет срабатывать, если во время ввода возраста
# будет введено что-то некорректное
@dp.message(StateFilter(FSMFillForm.fill_age))
async def warning_age_set(message: Message, i18n: dict[str, str]):
    await message.answer(text=i18n.get('not_age'))


# Этот хэндлер будет срабатывать на нажатие кнопки при
# выборе пола и переводить в состояние отправки фото
@dp.callback_query(StateFilter(FSMFillForm.fill_gender),
                   F.data.in_(['male_gender', 'female_gender', 'undefined_gender']))
async def process_gender_press(callback: CallbackQuery, state: FSMContext, i18n: dict[str, str]):
    # Cохраняем пол (callback.data нажатой кнопки) в хранилище,
    # по ключу "gender"
    await state.update_data(gender=i18n.get(callback.data))
    # Удаляем сообщение с кнопками, потому что следующий этап - загрузка фото
    # чтобы у пользователя не было желания тыкать кнопки
    await callback.message.delete()
    await callback.message.answer(text=i18n.get('thank_gender'))
    # Устанавливаем состояние ожидания загрузки фото
    await state.set_state(FSMFillForm.upload_photo)


# Этот хэндлер будет срабатывать, если во время выбора пола
# будет введено/отправлено что-то некорректное
@dp.message(StateFilter(FSMFillForm.fill_gender))
async def warning_gender_set(message: Message, i18n: dict[str, str]):
    await message.answer(text=i18n.get('not_gender'))


# Этот хэндлер будет срабатывать, если отправлено фото
# и переводить в состояние выбора образования
@dp.message(StateFilter(FSMFillForm.upload_photo),
            F.photo[-1].as_('largest_photo'))
async def process_photo_set(message: Message,
                            state: FSMContext,
                            i18n: dict[str, str],
                            largest_photo: PhotoSize):
    # Cохраняем данные фото (file_unique_id и file_id) в хранилище
    # по ключам "photo_unique_id" и "photo_id"
    await state.update_data(
        photo_unique_id=largest_photo.file_unique_id,
        photo_id=largest_photo.file_id
    )
    # Создаем объекты инлайн-кнопок
    secondary_button = InlineKeyboardButton(
        text=i18n.get('secondary_button'),
        callback_data='secondary'
    )
    higher_button = InlineKeyboardButton(
        text=i18n.get('higher_button'),
        callback_data='higher'
    )
    no_edu_button = InlineKeyboardButton(
        text=i18n.get('no_edu_button'),
        callback_data='no_edu'
    )
    # Добавляем кнопки в клавиатуру (две в одном ряду и одну в другом)
    keyboard: list[list[InlineKeyboardButton]] = [
        [secondary_button, higher_button],
        [no_edu_button]
    ]
    # Создаем объект инлайн-клавиатуры
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    # Отправляем пользователю сообщение с клавиатурой
    await message.answer(
        text=i18n.get('thank_photo'),
        reply_markup=markup
    )
    # Устанавливаем состояние ожидания выбора образования
    await state.set_state(FSMFillForm.fill_education)


# Этот хэндлер будет срабатывать, если во время отправки фото
# будет введено/отправлено что-то некорректное
@dp.message(StateFilter(FSMFillForm.upload_photo))
async def warning_photo_set(message: Message, i18n: dict[str, str]):
    await message.answer(text=i18n.get('not_photo'))


# Этот хэндлер будет срабатывать, если выбрано образование
# и переводить в состояние согласия получать новости
@dp.callback_query(StateFilter(FSMFillForm.fill_education),
                   F.data.in_(['secondary', 'higher', 'no_edu']))
async def process_education_set(callback: CallbackQuery, state: FSMContext, i18n: dict[str, str]):
    # Cохраняем данные об образовании по ключу "education"
    await state.update_data(education=callback.data)
    # Создаем объекты инлайн-кнопок
    yes_news_button = InlineKeyboardButton(
        text=i18n.get('yes'),
        callback_data='yes_news'
    )
    no_news_button = InlineKeyboardButton(
        text=i18n.get('no'),
        callback_data='no_news'
    )
    # Добавляем кнопки в клавиатуру в один ряд
    keyboard: list[list[InlineKeyboardButton]] = [
        [yes_news_button, no_news_button]
    ]
    # Создаем объект инлайн-клавиатуры
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    # Редактируем предыдущее сообщение с кнопками, отправляя
    # новый текст и новую клавиатуру
    await callback.message.edit_text(
        text=i18n.get('thank_edu'),
        reply_markup=markup
    )
    # Устанавливаем состояние ожидания выбора получать новости или нет
    await state.set_state(FSMFillForm.fill_wish_news)


# Этот хэндлер будет срабатывать, если во время выбора образования
# будет введено/отправлено что-то некорректное
@dp.message(StateFilter(FSMFillForm.fill_education))
async def warning_education_set(message: Message, i18n: dict[str, str]):
    await message.answer(text=i18n.get('not_edu'))


# Этот хэндлер будет срабатывать на выбор получать или
# не получать новости и выводить из машины состояний
@dp.callback_query(StateFilter(FSMFillForm.fill_wish_news),
                   F.data.in_(['yes_news', 'no_news']))
async def process_wish_news_press(callback: CallbackQuery, state: FSMContext, i18n: dict[str, str]):
    # Cохраняем данные о получении новостей по ключу "wish_news"
    await state.update_data(wish_news=callback.data == 'yes_news')
    # Добавляем в "базу данных" анкету пользователя
    # по ключу id пользователя
    users_db[callback.from_user.id] = await state.get_data()
    # Завершаем машину состояний
    await state.clear()
    # Отправляем в чат сообщение о выходе из машины состояний
    await callback.message.edit_text(
        text=i18n.get('thank_news')
    )
    # Отправляем в чат сообщение с предложением посмотреть свою анкету
    await callback.message.answer(
        text='Чтобы посмотреть данные вашей '
             'анкеты - отправьте команду /showdata'
    )


# Этот хэндлер будет срабатывать, если во время согласия на получение
# новостей будет введено/отправлено что-то некорректное
@dp.message(StateFilter(FSMFillForm.fill_wish_news))
async def warning_not_wish_news(message: Message):
    await message.answer(
        text='Пожалуйста, воспользуйтесь кнопками!\n\n'
             'Если вы хотите прервать заполнение анкеты - '
             'отправьте команду /cancel'
    )


# Этот хэндлер будет срабатывать на отправку команды /showdata
# и отправлять в чат данные анкеты, либо сообщение об отсутствии данных
@dp.message(Command(commands='showdata'), StateFilter(default_state))
async def process_showdata_command(message: Message):
    # Отправляем пользователю анкету, если она есть в "базе данных"
    if message.from_user.id in users_db:
        await message.answer_photo(
            photo=users_db[message.from_user.id]['photo_id'],
            caption=f'Имя: {users_db[message.from_user.id]["name"]}\n'
                    f'Возраст: {users_db[message.from_user.id]["age"]}\n'
                    f'Пол: {users_db[message.from_user.id]["gender"]}\n'
                    f'Образование: {users_db[message.from_user.id]["education"]}\n'
                    f'Получать новости: {users_db[message.from_user.id]["wish_news"]}'
        )
    else:
        # Если анкеты пользователя в базе нет - предлагаем заполнить
        await message.answer(
            text='Вы еще не заполняли анкету. Чтобы приступить - '
            'отправьте команду /fillform'
        )


# Этот хэндлер будет срабатывать на любые сообщения, кроме тех
# для которых есть отдельные хэндлеры, вне состояний
@dp.message(StateFilter(default_state))
async def send_echo(message: Message):
    await message.reply(text='Извините, моя твоя не понимать')


if __name__ == '__main__':
    # dp.startup.register(set_main_menu)
    dp.run_polling(bot)
