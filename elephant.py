# coding: utf-8
from __future__ import unicode_literals
import random

alise_number = 0
status = 0
forms_of_can = ["умеешь", "создан", "делаешь", "делать", "правила", "помощь"]
numbers_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
# Функция для непосредственной обработки диалога.
def handle_dialog(request, response, user_storage):
    global alise_number, status, forms_of_can, numbers_list
    if request.is_new_session or status == 0 or (status == 2 and str(request.command.lower()) == "да"):
        alise_number = 0
        # Это новый пользователь.
        # Инициализируем сессию и поприветствуем его.

        user_storage = {
            'suggests': [
                "однозначное",
                "двузначное",
                "трёхзначное",
                "четырёхзначное"
            ]
        }

        buttons, user_storage = get_suggests(user_storage)
        response.set_text('Я загадываю число, а Вы пытаетесь его отгадать. После Вашей попытки я говорю, сколько цифр угадано без совпадения с их позициями в моём числе (коровы) и не угадано (быки). Какое число загадать?')
        response.set_buttons(buttons)
        status = 1
        return response, user_storage

    for i in str(request.command.lower()).split():
        if i in forms_of_can:
            alise_number = 0
            # Это новый пользователь.
            # Инициализируем сессию и поприветствуем его.

            user_storage = {
                'suggests': [
                    "однозначное",
                    "двузначное",
                    "трёхзначное",
                    "четырёхзначное"
                ]
            }

            buttons, user_storage = get_suggests(user_storage)
            response.set_text('Я загадываю число, а Вы пытаетесь его отгадать. После Вашей попытки я говорю, сколько цифр угадано без совпадения с их позициями в моём числе (коровы) и не угадано (быки). Какое число загадать?')
            response.set_buttons(buttons)
            status = 1
            return response, user_storage


    #if str(request.command.lower()) in forms_of_can:
        #£response.set_text('Я загадываю число, а Вы пытаетесь его отгадать. После Вашей попытки я говорю, сколько цифр угадано без совпадения с их позициями в моём числе (коровы) и не угадано (быки). Какое число загадать?')

    if status == 2:
        response.set_text('Окей.')
        status = -1
        return response, user_storage


    # Обрабатываем ответ пользователя.
    if str(request.command.lower()) in ['сдаюсь', 'не знаю']:
        response.set_text('На самом деле всё очень просто. Я загадала число {}.'.format(str(alise_number)))
        return response, user_storage

    if str(request.command.lower()) == 'однозначное':
        response.set_text('Хорошо, число загадано. Поехали!')
        alise_number = random.randint(1, 9)
        return response, user_storage

    if str(request.command.lower()) == 'двузначное':
        response.set_text('Хорошо, число загадано. Поехали!')
        alise_number = random.randint(10, 99)
        return response, user_storage

    if str(request.command.lower()) == 'трёхзначное':
         response.set_text('Хорошо, число загадано. Поехали!')
         alise_number = random.randint(100, 999)
         return response, user_storage

    for i in str(request.command.lower()):
        if i not in numbers_list:
            response.set_text('Кажется, Вы ввели что-то не то. Скажите число, а я отвечу, сколько в нём быков и коров, или запросите правила игры.')
            status = 1
            return response, user_storage

    if len(str(request.command.lower())) != len(str(alise_number)):
        response.set_text('Количество цифр в Вашем числе не совпадает с моим. Назовите число ещё раз.')
        return response, user_storage

    if str(request.command.lower()) == str(alise_number):
        response.set_text('Верно. Загаданное число: {}. Хотите сыграть ещё раз?'.format(alise_number))
        status = 2
        user_storage = {
            'suggests': [
                "да",
                "нет"
            ]
        }

        buttons, user_storage = get_suggests(user_storage)

        response.set_buttons(buttons)
        return response, user_storage



    bull = cow = 0
    for i in range(len(str(request.command.lower()))):
        if str(request.command.lower())[i] == str(alise_number)[i]:
            bull += 1

    flag = [0] * 10
    for i in range(len(str(request.command.lower()))):
        for j in range(len(str(request.command.lower()))):
            if str(request.command.lower())[i] == str(alise_number)[j] and flag[int(str(alise_number)[i])] == 0:
                flag[int(str(alise_number)[i])] = 1
                cow += 1

    response.set_text('Быков: {}, коров: {}.'.format(str(bull), str(cow - bull)))
    status = 1

    return response, user_storage


# Функция возвращает две подсказки для ответа.
def get_suggests(user_storage):
    # Выбираем две первые подсказки из массива.
    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in user_storage['suggests']
    ]


    ####
    return suggests, user_storage
