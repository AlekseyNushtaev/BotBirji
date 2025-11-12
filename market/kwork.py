import datetime
import time
import bs4
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import Chrome

from bot import bot
from words import words

kworks_links = {
    'https://kwork.ru/projects?c=28': 'Дизайн | Арт и иллюстрации',
    'https://kwork.ru/projects?c=24': 'Дизайн | Веб и мобильный дизайн',
    'https://kwork.ru/projects?c=90': 'Дизайн | Интерьер и экстерьер',
    'https://kwork.ru/projects?c=25': 'Дизайн | Логотип и брендинг',
    'https://kwork.ru/projects?c=286': 'Дизайн | Маркетплейс и соцсети',
    'https://kwork.ru/projects?c=272': 'Дизайн | Наружная реклама',
    'https://kwork.ru/projects?c=68': 'Дизайн | Обработка и редактирование',
    'https://kwork.ru/projects?c=27': 'Дизайн | Полиграфия',
    'https://kwork.ru/projects?c=270': 'Дизайн | Презентация и инфографика',
    'https://kwork.ru/projects?c=250': 'Дизайн | Промышленный дизайн',
    'https://kwork.ru/projects?c=79': 'Разработка и IT | Верстка',
    'https://kwork.ru/projects?c=80': 'Разработка и IT | Десктоп программирование',
    'https://kwork.ru/projects?c=38': 'Разработка и IT | Доработка и настройка сайта',
    'https://kwork.ru/projects?c=40': 'Разработка и IT | Игры',
    'https://kwork.ru/projects?c=39': 'Разработка и IT | Мобильные приложения',
    'https://kwork.ru/projects?c=255': 'Разработка и IT | Сервера и хостинг',
    'https://kwork.ru/projects?c=41': 'Разработка и IT | Скрипты и боты',
    'https://kwork.ru/projects?c=37': 'Разработка и IT | Создание сайта',
    'https://kwork.ru/projects?c=81': 'Разработка и IT | Юзабилити, тесты, помощь',
    'https://kwork.ru/projects?c=75': 'Тексты и переводы | Набор текста',
    'https://kwork.ru/projects?c=35': 'Тексты и переводы | Переводы',
    'https://kwork.ru/projects?c=74': 'Тексты и переводы | Продающие и бизнес-тексты',
    'https://kwork.ru/projects?c=73': 'Тексты и переводы | Тексты и наполнение сайта',
    'https://kwork.ru/projects?c=44': 'SEO и трафик | SEO аудиты, консультации',
    'https://kwork.ru/projects?c=43': 'SEO и трафик | Внутренняя оптимизация',
    'https://kwork.ru/projects?c=273': 'SEO и трафик | Продвижение сайта в топ',
    'https://kwork.ru/projects?c=71': 'SEO и трафик | Семантическое ядро',
    'https://kwork.ru/projects?c=59': 'SEO и трафик | Ссылки',
    'https://kwork.ru/projects?c=56': 'SEO и трафик | Статистика и аналитика',
    'https://kwork.ru/projects?c=72': 'SEO и трафик | Трафик',
    'https://kwork.ru/projects?c=108': 'Соцсети и реклама | E-mail маркетинг и рассылки',
    'https://kwork.ru/projects?c=113': 'Соцсети и реклама | Базы данных и клиентов',
    'https://kwork.ru/projects?c=49': 'Соцсети и реклама | Контекстная реклама',
    'https://kwork.ru/projects?c=112': 'Соцсети и реклама | Маркетплейсы и доски объявлений',
    'https://kwork.ru/projects?c=47': 'Соцсети и реклама | Реклама и PR',
    'https://kwork.ru/projects?c=46': 'Соцсети и реклама | Соцсети и SMM',
    'https://kwork.ru/projects?c=20': 'Аудио, видео, съемка | Аудиозапись и озвучка',
    'https://kwork.ru/projects?c=76': 'Аудио, видео, съемка | Видеоролики',
    'https://kwork.ru/projects?c=78': 'Аудио, видео, съемка | Видеосъемка и монтаж',
    'https://kwork.ru/projects?c=77': 'Аудио, видео, съемка | Интро и анимация логотипа',
    'https://kwork.ru/projects?c=23': 'Аудио, видео, съемка | Музыка и песни',
    'https://kwork.ru/projects?c=64': 'Бизнес и жизнь | Бухгалтерия и налоги',
    'https://kwork.ru/projects?c=262': 'Бизнес и жизнь | Обзвоны и продажи',
    'https://kwork.ru/projects?c=55': 'Бизнес и жизнь | Обучение и консалтинг',
    'https://kwork.ru/projects?c=84': 'Бизнес и жизнь | Персональный помощник',
    'https://kwork.ru/projects?c=265': 'Бизнес и жизнь | Подбор персонала',
    'https://kwork.ru/projects?c=114': 'Бизнес и жизнь | Продажа сайтов',
    'https://kwork.ru/projects?c=65': 'Бизнес и жизнь | Стройка и ремонт',
    'https://kwork.ru/projects?c=63': 'Бизнес и жизнь | Юридическая помощь',
}


async def parser_kwork(browser, res_old):
    result = []
    for link_cat in kworks_links.keys():
        browser.get(link_cat)
        print(kworks_links[link_cat])
        time.sleep(1)
        time.sleep(0.25)
        html = browser.page_source
        soup = bs4.BeautifulSoup(html, 'lxml')
        cards = soup.find_all(attrs={"class": 'want-card want-card--list want-card--hover'})
        for card in cards:
            link = 'https://kwork.ru' + card.find("a").get("href")
            if link not in res_old:
                try:
                    title = card.find("a").text.strip()
                except Exception:
                    title = ''
                try:
                    text = soup.find(attrs={"class": 'breakwords first-letter overflow-hidden'}).text.strip()
                except Exception:
                    text = ''
                try:
                    price = soup.find(attrs={"class": 'wants-card__right'}).text.strip()
                except Exception:
                    price = ''
                min_price = ''
                for p in price.split('Допустимый')[0]:
                    if p.isdigit():
                        min_price += p
                try:
                    min_price = int(min_price)
                except Exception:
                    min_price = 0
                category = kworks_links[link_cat].split(' | ')[0]
                podcategory = kworks_links[link_cat].split(' | ')[1]
                for word in words:
                    if category in ['Разработка и IT', 'SEO и трафик']:
                        if word in text or word in title:
                            await bot.send_message(1012882762, f"{category}\n\n{title}\n\n{text}\n\n{link}")
                            break
                result.append([title, link, category, podcategory, text, price])
                print(datetime.datetime.now())
                print([min_price, price, title, link, category, podcategory, text])

    return result


