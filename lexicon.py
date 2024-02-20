LEXICON_RU = {
    '/start': 'Этот бот демонстрирует работу FSM\n\n'
              'Чтобы перейти к заполнению анкеты - '
              'отправьте команду /fillform',
    '/cancel': 'Отменять нечего. Вы вне машины состояний\n\n'
               'Чтобы перейти к заполнению анкеты - '
               'отправьте команду /fillform',
    '/cancel~': 'Вы вышли из машины состояний\n\n'
                'Чтобы снова перейти к заполнению анкеты - '
                'отправьте команду /fillform',
    '/fillform': 'Пожалуйста, введите ваше имя',
    'thank_name': 'Спасибо!\n\n А теперь введите ваш возраст',
    'not_name': 'То, что вы отправили не похоже на имя\n\n'
                'Пожалуйста, введите ваше имя\n\n'
                'Если вы хотите прервать заполнение анкеты - '
                'отправьте команду /cancel',
    'male_gender': 'Мужской ♂',
    'female_gender': 'Женский ♀',
    'unknown_gender': '🤷 Пока не ясно',
    'thank_age': 'Спасибо!\n\nУкажите ваш пол',
    'not_age': 'Возраст должен быть целым числом от 4 до 120\n\n'
               'Попробуйте еще раз\n\nЕсли вы хотите прервать '
               'заполнение анкеты - отправьте команду /cancel',
    'thank_gender': 'Спасибо! А теперь загрузите, пожалуйста, ваше фото',
    'not_gender': 'Пожалуйста, пользуйтесь кнопками '
                  'при выборе пола\n\nЕсли вы хотите прервать '
                  'заполнение анкеты - отправьте команду /cancel',
    'secondary_button': 'Среднее',
    'higher_button': 'Высшее',
    'no_edu_button': '🤷 Нету',
    'thank_photo': 'Спасибо!\n\nУкажите ваше образование',
    'not_photo': 'Пожалуйста, на этом шаге отправьте '
                 'ваше фото\n\nЕсли вы хотите прервать '
                 'заполнение анкеты - отправьте команду /cancel',
    'yes': 'Да',
    'no': 'Нет',
    'thank_edu': 'Спасибо!\n\nОстался последний шаг.\n'
                 'Хотели бы вы получать новости?',
    'not_edu': 'Пожалуйста, пользуйтесь кнопками при выборе образования\n\n'
               'Если вы хотите прервать заполнение анкеты - отправьте '
               'команду /cancel',
    'thank_news': 'Спасибо! Ваши данные сохранены!\n\n'
                  'Вы вышли из машины состояний',

}

LEXICON_EN = {
    '/start': 'This bot demonstrates the work of FSM\n\n'
              'To proceed to filling out the questionnaire - '
              'send the /fillform command',
    '/cancel': 'There is nothing to cancel. You are outside the state machine\n\n'
               'To proceed to filling out the questionnaire - '
               'send the /fillform command',
    '/cancel~': 'You have exited the state machine\n\n'
                'To go back to filling out the questionnaire - '
                'send the /fillform command',
    '/fillform': 'Please enter your name',
    'thank_name': 'Thank you!\n\n And now enter your age',
    'not_name': 'What you sent doesn\'t look like the name \n\n'
                'Please enter your name\n\n'
                'If you want to interrupt filling out the questionnaire - '
                'send the /cancel command',
    'male_gender': 'Male ♂',
    'female_gender': 'Female ♀',
    'unknown_gender': '🤷 It\'s not clear yet',
    'thank_age': 'Thanks!\n\nspecify your gender',
    'not_age': 'Age must be an integer from 4 to 120\n\n'
               'Try again\n\n If you want to interrupt '
               'filling out the questionnaire - send the command /cancel',
    'thank_gender': 'Thank you! And now, please upload your photo',
    'not_gender': 'Please use the buttons '
                  'when choosing a floor\n\nif you want to interrupt '
                  'filling out the questionnaire - send the command /cancel',
    'secondary_button': 'Secondary',
    'higher_button': 'Higher',
    'no_edu_button': 'No education',
    'thank_photo': 'Thank you!\n\nSpecify your education',
    'not_photo': 'Please send at this step '
                 'your photo\n\nIf you want to interrupt '
                 'filling out the questionnaire - send the command /cancel',
    'yes': 'Yes',
    'no': 'No',
    'thank_edu': 'Thank you!\n\nThe last step remains.\n'
                 'Would you like to receive news?',
    'not_edu': 'Please use the buttons when selecting education\n\n'
               'If you want to interrupt filling out the questionnaire, send it '
               'command /cancel',
    'thank_news': 'Thank you! Your data is saved!\n\n'
                  'You have exited the state machine',

}

# Создаём словарь для описания команд в кнопке Menu
LEXICON_COMMANDS = {
    '/start': 'Начало работы с ботом',
    '/cancel': 'Выйти из FSM',
    '/fillform': 'Войти в FSM',
    '/showdata': 'Показывает ваши данные'
}