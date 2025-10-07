from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import Chrome
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import openpyxl
import json
import requests
import bs4
import fake_headers
import time
import unicodedata
import datetime
import os
from pprint import pprint


dct_youdo = {
    'Виртуальный помощник': ['Работа с текстом, копирайтинг', 'Услуги переводчика', 'Поиск и обработка информации', 'Работа с числовыми данными', 'Подготовка презентаций', 'Расшифровка аудио- и видеозаписей', 'Размещение на рекламных площадках', 'Помощь SMM-специалиста', 'Реклама и продвижение в интернете', 'Обзвон по базе', 'Услуги личного помощника', 'Что-то другое'],
    'Компьютерная помощь': ['Ремонт компьютеров и ноутбуков', 'Установка и настройка операц. систем, программ', 'Удаление вирусов', 'Настройка интернета и Wi-Fi', 'Ремонт и замена комплектующих', 'Восстановление данных', 'Настройка и ремонт оргтехники', 'Консультация и обучение', 'Что-то другое'],
    'Мероприятия и промоакции': ['Помощь в проведении мероприятий', 'Раздача промо-материалов', 'Тайный покупатель', 'Разнорабочий', 'Промоутер', 'Тамада, ведущий, аниматор', 'Промо-модель', 'Мерчендайзеры', 'Комплектовщики', 'Что-то другое'],
    'Дизайн': ['Фирменный стиль, логотипы, визитки', 'Полиграфический дизайн', 'Иллюстрации, живопись, граффити', 'Дизайн сайтов и приложений', 'Интернет-баннеры, оформление соц.сетей', '3d-графика, анимация', 'Инфографика, презентации, иконки', 'Наружная реклама, стенды, pos-материалы', 'Архитектура, интерьер, ландшафт', 'Дизайн одежды', 'Что-то другое'],
    'Разработка ПО': ['Сайт под ключ', 'Разработка мобильных приложений', 'Программирование', 'Доработка и поддержка сайта', 'Доработка и настройка 1С', 'Создание лендингов', 'Верстка', 'Скрипты и боты', 'Что-то другое'],
    'Фото, видео и аудио': ['Фотосъемка', 'Видеосъемка', 'Запись аудио', 'Обработка фотографий', 'Создание видео под ключ', 'Модели для съемок', 'Монтаж и цветокоррекция видео', 'Оцифровка', 'Что-то другое'],
    'Установка и ремонт техники': ['Холодильники и морозильные камеры', 'Стиральные и сушильные машины', 'Посудомоечные машины', 'Электрические плиты и панели', 'Газовые плиты', 'Духовые шкафы', 'Вытяжки', 'Климатическая техника', 'Водонагреватели, бойлеры, котлы, колонки', 'Швейные машины', 'Пылесосы и очистители', 'Утюги и уход за одеждой', 'Кофемашины', 'СВЧ печи', 'Мелкая кухонная техника', 'Уход за телом и здоровьем', 'Строительная и садовая техника', 'Что-то другое'],
    'Красота и здоровье': ['Услуги косметолога', 'Эпиляция', 'Брови и ресницы', 'Услуги визажиста', 'Тату и пирсинг', 'Парикмахерские услуги', 'Ногтевой сервис', 'Массаж', 'Стилисты и имиджмейкеры', 'Психологи и психотерапевты', 'Услуги медсестры', 'Персональный тренер', 'Что-то другое'],
    'Юридическая и бухгалтерская помощь': ['Бухгалтерские услуги', 'Консультация специалиста по налогам', 'Нотариальные услуги', 'Оформление документов', 'Услуги адвоката', 'Регистрация, ликвидация компаний', 'Составление и подача жалоб, исков', 'Составление и проверка договоров', 'Юридическая консультация', 'Юридическое сопровождение', 'Тендеры', 'Делопроизводство и работа с кадрами', 'Что-то другое'],
    'Репетиторы и обучение': ['Русский язык и литература', 'Английский язык', 'Французский язык', 'Немецкий язык', 'Испанский язык', 'Другие иностранные языки', 'Математика и физика', 'Биология и химия', 'История и обществознание', 'География и экономика', 'Информатика и программирование', 'Подготовка к школе и младшие классы', 'Музыка, танцы, арт', 'Помощь студентам', 'Логопеды', 'Спорт', 'Автоинструкторы', 'Что-то другое']
}


def parser_youdo(browser, res_old):
    result = []
    browser.get(f'https://youdo.com/tasks-all-opened-all')
    time.sleep(3)
    time.sleep(0.25)
    html = browser.page_source
    soup = bs4.BeautifulSoup(html, 'lxml')
    cards = soup.find_all(attrs={"class": 'TasksList_contentWrapper__BOEQ_'})
    for card in cards:
        link = 'https://youdo.com' + card.find("a").get("href").split('?')[0]
        adress = card.find(attrs={"class": 'TasksList_address__CJuTy'}).text.strip()
        if link not in res_old and adress == 'Можно выполнить удаленно':
            res_old.append(link)
            browser.get(link)
            time.sleep(1)
            time.sleep(0.25)
            html = browser.page_source.replace('<br>', '\n')
            soup = bs4.BeautifulSoup(html, 'lxml')
            try:
                title = soup.find(attrs={"class": 'b-task-block b-task-block__header'}).find("h1").text.strip()
            except Exception:
                title = ''
            try:
                text = soup.find(attrs={"class": 'text-5 b-layout__txt_padbot_20'}).text.strip()
            except Exception:
                try:
                    text = soup.find(attrs={"itemprop": 'description'}).text.strip()
                    text_ = text.split('\n')
                    text = []
                    for t in text_:
                        if t.strip() != '':
                            text.append(t.strip())
                    text = '\n'.join(text)
                except Exception:
                    text = ''
            try:
                price = soup.find(attrs={"class": 'py-32 text-right unmobile flex-shrink-0 ml-auto mobile'}).find("span").text.strip()
            except Exception:
                try:
                    price = soup.find(attrs={"class": 'js-budget-text'}).find("span").text.strip()
                except Exception:
                    price = ''
            min_price = ''
            for p in price:
                if p.isdigit():
                    min_price += p
            try:
                min_price = int(min_price)
            except Exception:
                min_price = 0
            try:
                category = soup.find(attrs={"class": 'js-task-item--brief'}).find_all("li")[-2].text.strip()
                if category in dct_youdo.keys():
                    podcategory = 'Что-то другое'
                else:
                    podcategory = category
                    for item in dct_youdo.keys():
                        if category in dct_youdo[item]:
                            category = item
            except Exception:
                category = ''
            result.append([title, link, category, podcategory, text, price])
            print(datetime.datetime.now())
            print([min_price, price, title, link, category, podcategory, text])

    return result
