import logging
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils import executor
import random

API_TOKEN = '7920118786:AAFQUvlwLez1cb2LadF4q-dkaWMW8sRQYy0'  

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Логирование ошибок
logging.basicConfig(level=logging.INFO)

user_data = {}

clothing_items = [
    # Обязательные элементы верхней одежды
    {"type": "Верхняя одежда", "item": "Рубашка-поло", "gender": "М/Ж", "temperature": "любая", "body_type": "любой", "groups": [1]},
    {"type": "Верхняя одежда", "item": "Майка приталенная", "gender": "Ж", "temperature": "любая", "body_type": ["Песочные часы", "Прямоугольник", "Груша"], "groups": [2,3]},
    {"type": "Верхняя одежда", "item": "Приталенная футболка", "gender": "Ж", "temperature": "любая", "body_type": "любой", "groups": [2,3]},
    {"type": "Верхняя одежда", "item": "Свободная футболка", "gender": "М/Ж", "temperature": "любая", "body_type": "любой", "groups": [2,3,4]},
    {"type": "Верхняя одежда", "item": "Приталенный лонгслив", "gender": "М/Ж", "temperature": "любая", "body_type": ["Песочные часы", "Прямоугольник"], "groups": [2,3,4]},
    {"type": "Верхняя одежда", "item": "Свободный лонгслив", "gender": "М/Ж", "temperature": "любая", "body_type": "любой", "groups": [2,3,4]},
    {"type": "Верхняя одежда", "item": "Классическая рубашка", "gender": "М/Ж", "temperature": "любая", "body_type": "любой", "groups": [1]},
    {"type": "Верхняя одежда", "item": "Блузка", "gender": "Ж", "temperature": "любая", "body_type": "любой", "groups": [1]},
    {"type": "Верхняя одежда", "item": "Топ", "gender": "Ж", "temperature": "20-40", "body_type": ["Песочные часы", "Прямоугольник", "Груша"], "groups": [2,3]},
    {"type": "Верхняя одежда", "item": "Майка-борцовка", "gender": "М", "temperature": "20-40", "body_type": "любой", "groups": [2,3]},

    # Температурозависимые элементы верхней одежды
    {"type": "Верхняя одежда", "item": "Джемпер", "gender": "М/Ж", "temperature": "<20", "body_type": "любой", "groups": [1,4]},
    {"type": "Верхняя одежда", "item": "Свитер", "gender": "М/Ж", "temperature": "<20", "body_type": "любой", "groups": [4]},
    {"type": "Верхняя одежда", "item": "Пуловер", "gender": "М/Ж", "temperature": "<20", "body_type": "любой", "groups": [4]},
    {"type": "Верхняя одежда", "item": "Водолазка", "gender": "М/Ж", "temperature": "<20", "body_type": ["Песочные часы", "Прямоугольник", "Груша"], "groups": [4]},
    {"type": "Верхняя одежда", "item": "Худи", "gender": "М/Ж", "temperature": "<20", "body_type": "любой", "groups": [2,3]},
    {"type": "Верхняя одежда", "item": "Свитшот", "gender": "М/Ж", "temperature": "<20", "body_type": "любой", "groups": [3]},
    {"type": "Верхняя одежда", "item": "Кардиган", "gender": "М/Ж", "temperature": "<20", "body_type": "любой", "groups": [1]},
    {"type": "Верхняя одежда", "item": "Полупальто", "gender": "М/Ж", "temperature": "0-10", "body_type": "любой", "groups": [1,4]},
    {"type": "Верхняя одежда", "item": "Пальто Тренч", "gender": "М/Ж", "temperature": "0-10", "body_type": "любой", "groups": [1,3,4]},
    {"type": "Верхняя одежда", "item": "Пальто Дафклот", "gender": "М/Ж", "temperature": "0-10", "body_type": "любой", "groups": [3]},
    {"type": "Верхняя одежда", "item": "Удлиненная дубленка", "gender": "М/Ж", "temperature": "<0", "body_type": "любой", "groups": [3]},
    {"type": "Верхняя одежда", "item": "Дубленка Авиатор", "gender": "М/Ж", "temperature": "<0", "body_type": "любой", "groups": [1,4]},
    {"type": "Верхняя одежда", "item": "Джинсовая куртка", "gender": "М/Ж", "temperature": ">10", "body_type": "любой", "groups": [2,3]},
    {"type": "Верхняя одежда", "item": "Плащ Макинтош", "gender": "М/Ж", "temperature": "0-10", "body_type": "любой", "groups": [1,3,4]},
    {"type": "Верхняя одежда", "item": "Английский плащ", "gender": "М/Ж", "temperature": "0-10", "body_type": "любой", "groups": [1]},
    {"type": "Верхняя одежда", "item": "Плащ Губертус", "gender": "М", "temperature": "0-10", "body_type": "любой", "groups": [1,3,4]},
    {"type": "Верхняя одежда", "item": "Куртка Анорак", "gender": "М", "temperature": "11-20", "body_type": "любой", "groups": [2,3]},
    {"type": "Верхняя одежда", "item": "Бомбер", "gender": "М/Ж", "temperature": "11-20", "body_type": "любой", "groups": [2]},
    {"type": "Верхняя одежда", "item": "Ветровка", "gender": "М/Ж", "temperature": "11-20", "body_type": "любой", "groups": [2,3]},
    {"type": "Верхняя одежда", "item": "Косуха", "gender": "М/Ж", "temperature": "11-20", "body_type": "любой", "groups": [3]},
    {"type": "Верхняя одежда", "item": "Дубленка Парка", "gender": "М/Ж", "temperature": "<0", "body_type": "любой", "groups": [2,3]},
    {"type": "Верхняя одежда", "item": "Куртка Спенсер", "gender": "М/Ж", "temperature": "11-20", "body_type": "любой", "groups": [2,4]},
    {"type": "Верхняя одежда", "item": "Пиджак", "gender": "М/Ж", "temperature": "11-20", "body_type": "любой", "groups": [1,4]},
    {"type": "Верхняя одежда", "item": "Жакет", "gender": "Ж", "temperature": "11-20", "body_type": "любой", "groups": [1]},
    {"type": "Верхняя одежда", "item": "Жилет утепленный", "gender": "М/Ж", "temperature": "0-10", "body_type": "любой", "groups": [2,4]},
    {"type": "Верхняя одежда", "item": "Пуховик длинный", "gender": "М/Ж", "temperature": "<0", "body_type": "любой", "groups": [1,3,4]},
    {"type": "Верхняя одежда", "item": "Пуховик средней длины", "gender": "М/Ж", "temperature": "<0", "body_type": "любой", "groups": [1,3]},
    {"type": "Верхняя одежда", "item": "Пуховик укороченный", "gender": "Ж", "temperature": "<0", "body_type": "любой", "groups": [2,4]},
    {"type": "Верхняя одежда", "item": "Шуба", "gender": "Ж", "temperature": "<0", "body_type": "любой", "groups": [4]},
    {"type": "Верхняя одежда", "item": "Шинель", "gender": "М", "temperature": "0-10", "body_type": "любой", "groups": [1]},

    # Низ (без изменений)
    {"type": "Низ", "item": "Юбка-миди", "gender": "Ж", "temperature": "любая", "body_type": ["Груша", "Треугольник"], "groups": [1]},
    {"type": "Низ", "item": "Мини-юбка", "gender": "М/Ж", "temperature": "любая", "body_type": ["Песочные часы", "Прямоугольник"], "groups": [1]},
    {"type": "Низ", "item": "Юбка-макси", "gender": "Ж", "temperature": "любая", "body_type": ["Груша", "Треугольник"], "groups": [1,3]},
    {"type": "Низ", "item": "Юбка-карандаш", "gender": "Ж", "temperature": "любая", "body_type": ["Песочные часы", "Прямоугольник"], "groups": [1]},
    {"type": "Низ", "item": "Юбка-плиссе", "gender": "Ж", "temperature": "20-40", "body_type": ["Песочные часы", "Прямоугольник", "Треугольник"], "groups": [3]},
    {"type": "Низ", "item": "Брюки со стрелками", "gender": "М/Ж", "temperature": "любая", "body_type": "любой", "groups": [1,3]},
    {"type": "Низ", "item": "Брюки скинни", "gender": "Ж", "temperature": "любая", "body_type": ["Песочные часы", "Прямоугольник", "Треугольник"], "groups": [3]},
    {"type": "Низ", "item": "Брюки-карго", "gender": "М/Ж", "temperature": "любая", "body_type": "любой", "groups": [2,3]},
    {"type": "Низ", "item": "Брюко-палаццо", "gender": "М/Ж", "temperature": "любая", "body_type": "любой", "groups": [1,4]},
    {"type": "Низ", "item": "Брюки Кюлоты", "gender": "Ж", "temperature": "любая", "body_type": "любой", "groups": [4]},
    {"type": "Низ", "item": "Брюки-трубы", "gender": "М/Ж", "temperature": "любая", "body_type": "любой", "groups": [2,3,4]},
    {"type": "Низ", "item": "Джинсы-багги", "gender": "М", "temperature": "любая", "body_type": "любой", "groups": [2,4]},
    {"type": "Низ", "item": "Джинсы Скинни", "gender": "Ж", "temperature": "любая", "body_type": ["Песочные часы", "Прямоугольник", "Треугольник"], "groups": [2]},
    {"type": "Низ", "item": "Джинсы Бойфренды", "gender": "М/Ж", "temperature": "любая", "body_type": "любой", "groups": [3]},
    {"type": "Низ", "item": "Джинсы Мом", "gender": "Ж", "temperature": "любая", "body_type": ["Песочные часы", "Прямоугольник", "Треугольник"], "groups": [3]},
    {"type": "Низ", "item": "Джинсы-баллоны", "gender": "М/Ж", "temperature": "любая", "body_type": "любой", "groups": [4]},
    {"type": "Низ", "item": "Леггинсы", "gender": "Ж", "temperature": "20-40", "body_type": ["Песочные часы", "Прямоугольник"], "groups": [2]},
    {"type": "Низ", "item": "Спортивные штаны", "gender": "М/Ж", "temperature": "любая", "body_type": "любой", "groups": [2]},
    {"type": "Низ", "item": "Джинсовые шорты", "gender": "М/Ж", "temperature": "20-40", "body_type": ["Песочные часы", "Прямоугольник", "Треугольник"], "groups": [3]},
    {"type": "Низ", "item": "Шорты с завышенной талией", "gender": "Ж", "temperature": "20-40", "body_type": ["Песочные часы", "Прямоугольник", "Треугольник"], "groups": [3]},
    {"type": "Низ", "item": "Шорты-Капри", "gender": "М/Ж", "temperature": "20-40", "body_type": ["Песочные часы", "Прямоугольник", "Треугольник"], "groups": [3]},
    {"type": "Низ", "item": "Велосипедки", "gender": "Ж", "temperature": "20-40", "body_type": ["Песочные часы", "Прямоугольник", "Треугольник"], "groups": [2]},
    {"type": "Низ", "item": "Спортивные шорты", "gender": "М/Ж", "temperature": "20-40", "body_type": "любой", "groups": [2]},
    {"type": "Низ", "item": "Юбка со складками", "gender": "Ж", "temperature": "20-40", "body_type": "любой", "groups": [1,4]},

    # Платья
    {"type": "Платье", "item": "Платье-рубашка", "gender": "Ж", "temperature": "20-40", "body_type": "любой", "groups": [1,4]},
    {"type": "Платье", "item": "Платье-туника", "gender": "Ж", "temperature": "20-40", "body_type": "любой", "groups": [3]},
    {"type": "Платье", "item": "Платье Бэби-Долл", "gender": "Ж", "temperature": "20-40", "body_type": "любой", "groups": [3,4]},
    {"type": "Платье", "item": "Платье-майка", "gender": "Ж", "temperature": "20-40", "body_type": "любой", "groups": [2,3]},
    {"type": "Платье", "item": "Платье-тюльпан", "gender": "Ж", "temperature": "20-40", "body_type": "любой", "groups": [1]},
    {"type": "Платье", "item": "Сарафан", "gender": "Ж", "temperature": "20-40", "body_type": "любой", "groups": [3]},
    {"type": "Платье", "item": "Платье-свитер", "gender": "Ж", "temperature": "20-40", "body_type": "любой", "groups": [1,4]},
    {"type": "Платье", "item": "Коктейльное платье", "gender": "Ж", "temperature": "20-40", "body_type": "любой", "groups": [4]},
    {"type": "Платье", "item": "Платье Торсо", "gender": "Ж", "temperature": "20-40", "body_type": "любой", "groups": [1]},
    {"type": "Платье", "item": "Платье Жилет", "gender": "Ж", "temperature": "20-40", "body_type": "любой", "groups": [1,3]},
    {"type": "Платье", "item": "Платье-пачка", "gender": "Ж", "temperature": "20-40", "body_type": "любой", "groups": [2]},

    # Обувь
    {"type": "Обувь", "item": "Туфли-лодочки", "gender": "Ж", "temperature": "20-40", "body_type": "любой", "groups": [1,4]},
    {"type": "Обувь", "item": "Мюли", "gender": "Ж", "temperature": "20-40", "body_type": "любой", "groups": [1]},
    {"type": "Обувь", "item": "Сандалии", "gender": "Ж", "temperature": "20-40", "body_type": "любой", "groups": [3]},
    {"type": "Обувь", "item": "Мокасины", "gender": "М/Ж", "temperature": "20-40", "body_type": "любой", "groups": [1]},
    {"type": "Обувь", "item": "Гладиаторы", "gender": "Ж", "temperature": "20-40", "body_type": "любой", "groups": [3]},
    {"type": "Обувь", "item": "Кроксы", "gender": "М/Ж", "temperature": "20-40", "body_type": "любой", "groups": [2,3]},
    {"type": "Обувь", "item": "Балетки", "gender": "Ж", "temperature": "20-40", "body_type": "любой", "groups": [1]},
    {"type": "Обувь", "item": "Босоножки", "gender": "Ж", "temperature": "20-40", "body_type": "любой", "groups": [3]},
    {"type": "Обувь", "item": "Сланцы", "gender": "М", "temperature": "20-40", "body_type": "любой", "groups": [2]},
    {"type": "Обувь", "item": "Лоферы", "gender": "М/Ж", "temperature": "20-40", "body_type": "любой", "groups": [1,4]},
    {"type": "Обувь", "item": "Ботфорты", "gender": "Ж", "temperature": "20-40", "body_type": "любой", "groups": [1]},
    {"type": "Обувь", "item": "Сапоги-казаки", "gender": "Ж", "temperature": "<0", "body_type": "любой", "groups": [4]},
    {"type": "Обувь", "item": "Сапоги Ридинги", "gender": "Ж", "temperature": "<0", "body_type": "любой", "groups": [1]},
    {"type": "Обувь", "item": "Угги", "gender": "Ж", "temperature": "<0", "body_type": "любой", "groups": [4]},
    {"type": "Обувь", "item": "Берцы", "gender": "М", "temperature": "<0", "body_type": "любой", "groups": [2,3]},
    {"type": "Обувь", "item": "Кроссовки спортивные", "gender": "М/Ж", "temperature": "любая", "body_type": "любой", "groups": [2,3,4]},
    {"type": "Обувь", "item": "Кеды", "gender": "М/Ж", "temperature": ">0", "body_type": "любой", "groups": [2,3,4]},
    {"type": "Обувь", "item": "Оксфорды", "gender": "М", "temperature": ">0", "body_type": "любой", "groups": [1,4]},
    {"type": "Обувь", "item": "Броги", "gender": "М", "temperature": "любая", "body_type": "любой", "groups": [1]},
    {"type": "Обувь", "item": "Слиперы", "gender": "Ж", "temperature": ">0", "body_type": "любой", "groups": [1]},

    # Аксессуары
    {"type": "Аксессуары", "item": "Солнцезащитные очки", "gender": "М/Ж", "temperature": "любая", "body_type": "любой", "groups": [1,2,3,4]},
    {"type": "Аксессуары", "item": "Головной убор", "gender": "М/Ж", "temperature": "любая", "body_type": "любой", "groups": [1,2,3,4]},
    {"type": "Аксессуары", "item": "Сумка", "gender": "М/Ж", "temperature": "любая", "body_type": "любой", "groups": [1,2,3,4]},
    {"type": "Аксессуары", "item": "Шарф / платок", "gender": "М/Ж", "temperature": "любая", "body_type": "любой", "groups": [1,2,3,4]},
    {"type": "Аксессуары", "item": "Перчатки", "gender": "М/Ж", "temperature": "<20", "body_type": "любой", "groups": [1,2,3,4]},
    {"type": "Аксессуары", "item": "Бижутерия / украшения", "gender": "Ж", "temperature": "любая", "body_type": "любой", "groups": [1,2,3,4]},
]

def weather_check(city):
    try:
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&lang=ru&appid=79d1ca96933b0328e1c7e3e7a26cb347'
        weather_data = requests.get(url).json()
        temperature = weather_data['main']['temp']
        temperature_feels = weather_data['main']['feels_like']
        wind_speed = weather_data['wind']['speed']
        cloud_cover = weather_data['weather'][0]['description']
        humidity = weather_data['main']['humidity']

        return (f'Температура воздуха: {temperature}°C\n'
                f'Ощущается как: {temperature_feels}°C\n'
                f'Ветер: {wind_speed} м/с\n'
                f'Облачность: {cloud_cover}\n'
                f'Влажность: {humidity}%'), temperature_feels
    except KeyError:
        return "Не удалось получить информацию о погоде. Проверьте название города.", None

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await show_main_menu(message)

async def show_main_menu(message: types.Message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = KeyboardButton("Создать образ")
    item2 = KeyboardButton("Определить цветотип")
    item3 = KeyboardButton("Определить тип фигуры")
    markup.add(item1, item2, item3)
    await message.reply(
        "Привет!\n Я — ваш цифровой стилист, готовый помочь вам создать идеальный образ! Независимо от повода, будь то важная встреча, вечеринка или просто прогулка по городу, я здесь, чтобы вдохновить вас и предложить стильные решения.\n Давайте вместе найдем ваш уникальный стиль и подчеркнем вашу индивидуальность!",
        reply_markup=markup
    )

@dp.message_handler(lambda message: message.text == "Определить тип фигуры")
async def determine_body_type_start(message: types.Message):
    user_id = message.from_user.id
    user_data[user_id] = {'step': 'body_test_q1'}
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    q1_variants = ["Бедра", "Плечи", "Одной длины"]
    markup.add(*q1_variants)
    await message.reply("Какая часть тела у вас шире: бедра или плечи?", reply_markup=markup)

@dp.message_handler(lambda message: user_data.get(message.from_user.id, {}).get('step') == 'body_test_q1')
async def body_test_q1(message: types.Message):
    user_id = message.from_user.id
    answer = message.text.lower()

    if "бедра" in answer:
        await message.reply("Ваш тип фигуры ГРУША", reply_markup=ReplyKeyboardRemove())
        user_data[user_id]['step'] = 'weather'
        await message.reply("Приступим к созданию образа.\n Чтобы узнать погоду, отправьте мне свой город.")
    elif "плечи" in answer:
        await message.reply("Ваш тип фигуры ТРЕУГОЛЬНИК", reply_markup=ReplyKeyboardRemove())
        user_data[user_id]['step'] = 'weather'
        await message.reply("Приступим к созданию образа.\n Чтобы узнать погоду, введите с клавиатуры свой город (с заглавной буквы)")
    elif "одной длины" in answer:
        user_data[user_id]['step'] = 'body_test_q2'
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        q2_variants = ["Да", "Нет"]
        markup.add(*q2_variants)
        await message.reply("У вас ярко выраженная талия?", reply_markup=markup)
    else:
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        q1_variants = ["Бедра", "Плечи", "Одной длины"]
        markup.add(*q1_variants)
        await message.reply("Пожалуйста, выберите: Бедра, Плечи или Одной длины", reply_markup=markup)

@dp.message_handler(lambda message: user_data.get(message.from_user.id, {}).get('step') == 'body_test_q2')
async def body_test_q2(message: types.Message):
    user_id = message.from_user.id
    answer = message.text.lower()

    if "да" in answer:
        await message.reply("Ваш тип фигуры ПЕСОЧНЫЕ ЧАСЫ", reply_markup=ReplyKeyboardRemove())
        user_data[user_id]['step'] = 'weather'
        await message.reply("Приступим к созданию образа.\n Чтобы узнать погоду, введите с клавиатуры свой город (с заглавной буквы)")
    elif "нет" in answer:
        await message.reply("Ваш тип фигуры ПРЯМОУГОЛЬНИК", reply_markup=ReplyKeyboardRemove())
        user_data[user_id]['step'] = 'weather'
        await message.reply("Приступим к созданию образа.\n Чтобы узнать погоду, введите с клавиатуры свой город (с заглавной буквы)")
    else:
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        q2_variants = ["Да", "Нет"]
        markup.add(*q2_variants)
        await message.reply("Пожалуйста, выберите Да или Нет:", reply_markup=markup)

@dp.message_handler(lambda message: message.text == "Определить цветотип")
async def color_type(message: types.Message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    eyes_variants = ["Серые / светло-голубые", "Голубые / зеленые", "Карие / бирюзово-желтые", "Синие / темно-карие / светло-серые"]
    markup.add(*eyes_variants)
    user_data[message.from_user.id] = {'step': 'eyes'}
    await message.reply("Давайте узнаем ваш цветотип! Выберите свой цвет глаз:", reply_markup=markup)

@dp.message_handler(lambda message: user_data.get(message.from_user.id, {}).get('step') == 'eyes')
async def choose_eye_color(message: types.Message):
    user_id = message.from_user.id
    user_data[user_id]['eyes'] = message.text
    
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    skin_variants = ["Светлая, персикового оттенка", "Светло – розовая", "Смуглая", "Очень светлая"]
    markup.add(*skin_variants)
    user_data[user_id]['step'] = 'skin'
    await message.reply("Выберите свой цвет кожи:", reply_markup=markup)

@dp.message_handler(lambda message: user_data.get(message.from_user.id, {}).get('step') == 'skin')
async def choose_skin_color(message: types.Message):
    user_id = message.from_user.id
    user_data[user_id]['skin'] = message.text
    
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    hair_variants = ["Светло-русые / Золотистые", "Русые / Пепельный-блонд", "Каштановые / Рыжие", "Темные"]
    markup.add(*hair_variants)
    user_data[user_id]['step'] = 'hair'
    await message.reply("Выберите свой цвет волос:", reply_markup=markup)

@dp.message_handler(lambda message: user_data.get(message.from_user.id, {}).get('step') == 'hair')
async def choose_hair_color(message: types.Message):
    user_id = message.from_user.id
    user_data[user_id]['hair'] = message.text

    eyes = user_data[user_id].get('eyes')
    skin = user_data[user_id].get('skin')
    hair = user_data[user_id].get('hair')

    if "Золотистые" in hair or "Светлая" in skin:
        c_type = "Весна"
    elif "Темные" in hair or "Смуглая" in skin:
        c_type = "Осень"
    elif "Пепельный" in hair or "Серые" in eyes:
        c_type = "Зима"
    else:
        c_type = "Лето"
    
    user_data[user_id]['color_type'] = c_type

    await message.reply(f"Ваш цветотип: {c_type}\n\nТеперь давайте продолжим создавать образ!", reply_markup=ReplyKeyboardRemove())
    user_data[user_id]['step'] = 'weather'
    await message.reply("Приступим к созданию образа.\n Чтобы узнать погоду, введите с клавиатуры свой город (с заглавной буквы)")

@dp.message_handler(lambda message: message.text == "Создать образ")
async def create_outfit(message: types.Message):
    user_id = message.from_user.id
    if user_data.get(user_id) and user_data[user_id].get('color_type'):
        user_data[user_id]['step'] = 'weather'
        await message.reply("Приступим к созданию образа.\n Чтобы узнать погоду, введите с клавиатуры свой город (с заглавной буквы)")
    else:
        user_data[user_id] = {}
        user_data[user_id]['step'] = 'weather'
        await message.reply("Приступим к созданию образа.\n Чтобы узнать погоду, введите с клавиатуры свой город (с заглавной буквы)")

@dp.message_handler(lambda message: user_data.get(message.from_user.id, {}).get('step') == 'weather')
async def get_weather_and_color(message: types.Message):
    user_id = message.from_user.id
    city = message.text
    weather_info, temperature_feels = weather_check(city)
    await message.reply(weather_info)

    if temperature_feels is not None:
        user_data[user_id]['temperature'] = temperature_feels
        user_data[user_id]['step'] = 'gender'
        
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("Мужской", "Женский")
        await message.reply("Выберите ваш пол:", reply_markup=markup)
    else:
        user_data[user_id]['step'] = 'weather'
        await message.reply("Попробуйте ввести название города ещё раз.")



@dp.message_handler(lambda message: user_data.get(message.from_user.id, {}).get('step') == 'gender')
async def choose_gender_and_accessories(message: types.Message):
    user_id = message.from_user.id
    selected_gender = message.text
    if selected_gender == "Мужской":
        gender_code = "М"
    elif selected_gender == "Женский":
        gender_code = "Ж"
    else:
        gender_code = selected_gender
    
    user_data[user_id]['gender'] = gender_code
    user_data[user_id]['step'] = 'accessories'

    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    accessories_list = ["Солнцезащитные очки", "Головной убор", "Сумка", "Шарф / платок", "Перчатки", "Бижутерия / украшения"]
    markup.add(*accessories_list)
    await message.reply("Выберите аксессуары (можно выбрать до 3). Введите их в одном сообщении через запятую, например: 'Сумка, Бижутерия / украшения':", reply_markup=markup)


@dp.message_handler(lambda message: user_data.get(message.from_user.id, {}).get('step') == 'accessories')
async def choose_accessories_and_body(message: types.Message):
    user_id = message.from_user.id
    accessories = [acc.strip() for acc in message.text.split(',')]
    # Можно выбрать до 3 аксессуаров
    accessories = accessories[:3]
    user_data[user_id]['accessories'] = accessories
    user_data[user_id]['step'] = 'body_type'

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    body_types = ["Песочные часы", "Прямоугольник", "Груша / Овал", "Треугольник"]
    markup.add(*body_types)
    await message.reply("Выберите тип вашей фигуры:", reply_markup=markup)

@dp.message_handler(lambda message: user_data.get(message.from_user.id, {}).get('step') == 'body_type')
async def choose_body_and_season(message: types.Message):
    user_id = message.from_user.id
    user_data[user_id]['body_type'] = message.text
    user_data[user_id]['step'] = 'color_type'

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    seasons = ["Зима", "Осень", "Лето", "Весна"]
    markup.add(*seasons)
    await message.reply("Выберите ваш цветотип:", reply_markup=markup)

@dp.message_handler(lambda message: user_data.get(message.from_user.id, {}).get('step') == 'color_type')
@dp.message_handler(lambda message: user_data.get(message.from_user.id, {}).get('step') == 'color_type')
async def generate_outfit(message: types.Message):
    user_id = message.from_user.id
    color_type = message.text
    user_data[user_id]['color_type'] = color_type
    user_data[user_id]['step'] = 'completed'

    color_recommendations = {
        "Зима": "чёрный, белый, синий и изумрудный",
        "Осень": "пряные оттенки, оранжевый,  коричневый и зелёный.",
        "Весна": "персиковый, коралловый, светло-зелёный, белый",
        "Лето": "пастельные оттенки, серый, бледно-розовый и голубой"
    }
    recommended_colors = color_recommendations.get(color_type, "Любые цвета")

    gender = user_data[user_id].get('gender')
    temperature = user_data[user_id].get('temperature')
    color = user_data[user_id].get('color')
    chosen_accessories = user_data[user_id].get('accessories', [])
    body_type = user_data[user_id].get('body_type')

    if color_type in ["Зима", "Осень"]:
        allowed_groups = [1]
    elif color_type == "Весна":
        allowed_groups = [3]
    elif color_type == "Лето":
        allowed_groups = [4]
    else:
        allowed_groups = [2,3,4]

    def filter_items(clothing):
        if gender not in clothing['gender']:
            return False
        temp_condition = clothing['temperature']
        if temp_condition == "любая":
            temp_ok = True
        elif '<' in temp_condition:
            temp_limit = float(temp_condition.strip('<').strip())
            temp_ok = temperature < temp_limit
        elif '>' in temp_condition:
            temp_limit = float(temp_condition.strip('>').strip())
            temp_ok = temperature > temp_limit
        elif '-' in temp_condition:
            lower, upper = temp_condition.split('-')
            temp_ok = float(lower.strip()) <= temperature <= float(upper.strip())
        else:
            temp_ok = False
        if not temp_ok:
            return False
        if not any(g in allowed_groups for g in clothing['groups']):
            return False
        body_condition = clothing['body_type']
        if body_condition == "любой":
            return True
        elif isinstance(body_condition, list):
            return body_type in body_condition
        else:
            return False

    # Обязательные элементы
    must_appear_names = [
        "Рубашка-поло",
        "Майка приталенная",
        "Приталенная футболка",
        "Свободная футболка",
        "Приталенный лонгслив",
        "Свободный лонгслив",
        "Классическая рубашка",
        "Блузка",
        "Топ",
        "Майка-борцовка"
    ]
    must_appear_items = [c for c in clothing_items if c['type'] == "Верхняя одежда" and c['item'] in must_appear_names]
    must_appear_filtered = [i for i in must_appear_items if filter_items(i)]

    # Температурозависимые элементы
    temp_dependent_names = [
        "Джемпер", "Свитер", "Пуловер", "Водолазка", "Худи", "Свитшот", "Кардиган",
        "Полупальто", "Пальто Тренч", "Пальто Дафклот", "Удлиненная дубленка", "Дубленка Авиатор",
        "Джинсовая куртка", "Плащ Макинтош", "Английский плащ", "Плащ Губертус",
        "Куртка Анорак", "Бомбер", "Ветровка", "Косуха", "Дубленка Парка",
        "Куртка Спенсер", "Пиджак", "Жакет", "Жилет утепленный",
        "Пуховик длинный", "Пуховик средней длины", "Пуховик укороченный", "Шуба", "Шинель"
    ]
    temp_dependent_items = [c for c in clothing_items if c['type'] == "Верхняя одежда" and c['item'] in temp_dependent_names]
    temp_dependent_filtered = [i for i in temp_dependent_items if filter_items(i)]

    upper = None
    if must_appear_filtered:
        upper = random.choice(must_appear_filtered)

    additional_upper = None
    if temp_dependent_filtered:
        additional_upper = random.choice(temp_dependent_filtered)

    # Низ/Платье/Обувь
    lower_clothes = [item for item in clothing_items if item['type'] == "Низ" and filter_items(item)]
    dress_clothes = [item for item in clothing_items if item['type'] == "Платье" and filter_items(item)]
    dress = random.choice(dress_clothes) if dress_clothes else None
    if dress:
        lower = None
    else:
        lower = random.choice(lower_clothes) if lower_clothes else None

    shoes_clothes = [item for item in clothing_items if item['type'] == "Обувь" and filter_items(item)]
    shoes = random.choice(shoes_clothes) if shoes_clothes else None

    # Аксессуары: используем именно те, которые выбрал пользователь
    accessory_clothes = [item for item in clothing_items if item['type'] == "Аксессуары"]
    selected_accessories = []
    for acc_name in chosen_accessories:
        # Ищем точное совпадение по названию (регистр не важен)
        acc_item = next((a for a in accessory_clothes if a['item'].lower() == acc_name.lower()), None)
        if acc_item and filter_items(acc_item):
            selected_accessories.append(acc_item)

    outfit_message = "Готово! Ваш образ:\n"
    if upper:
        outfit_message += f"Верхняя одежда: {upper['item']}\n"
    if additional_upper:
        outfit_message += f"Верхняя одежда (по погоде): {additional_upper['item']}\n"
    if dress:
        outfit_message += f"Платье: {dress['item']}\n"
    elif lower:
        outfit_message += f"Низ: {lower['item']}\n"
    if shoes:
        outfit_message += f"Обувь: {shoes['item']}\n"
    if selected_accessories:
        accessories_list = ", ".join([acc['item'] for acc in selected_accessories])
        outfit_message += f"Аксессуары: {accessories_list}\n"
    
    # Добавляем рекомендацию по цветам
    outfit_message += f"\nРекомендуемые цвета для вашего цветотипа ({color_type}): {recommended_colors}"

    if not (upper or lower or dress):
        outfit_message += "К сожалению, не удалось подобрать подходящую одежду по вашим параметрам."

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Создать новый образ")

    await message.reply(outfit_message, reply_markup=markup)

    
@dp.message_handler(lambda message: message.text == "Создать новый образ")
async def restart_process(message: types.Message):
    await show_main_menu(message)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)