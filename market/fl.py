import datetime
import time
import bs4

from bot import bot
from words import words


async def parser_fl(browser, res_old):
    browser.get('https://www.fl.ru/projects/')
    time.sleep(2.5)
    time.sleep(0.25)
    html = browser.page_source
    soup = bs4.BeautifulSoup(html, 'lxml')
    cards = soup.find_all(attrs={"data-id": 'qa-lenta-1'})
    result = []
    for card in cards:
        link = 'https://www.fl.ru' + card.find("a").get("href")
        date = card.find(attrs={"class": 'text-gray-opacity-4 text-7 mr-16'}).text.strip()
        if 'Только' in date or ('час' not in date and 'минут' in date):
            flag = True
        else:
            flag = False
        if link not in res_old and flag:
            browser.get(link)
            time.sleep(0.5)
            time.sleep(0.25)
            html = browser.page_source.replace('<br>', '\n')
            soup = bs4.BeautifulSoup(html, 'lxml')
            try:
                title = soup.find(attrs={"class": 'text-1 d-flex align-items-center'}).text.strip()
            except Exception:
                title = ''
            try:
                text = soup.find(attrs={"class": 'text-5 b-layout__txt_padbot_20'}).text.strip()
            except Exception:
                try:
                    text = soup.find(attrs={"class": 'text-5 b-layout__txt_padbot_20 wizard__editor'}).text.strip()
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
                    price = soup.find(attrs={"class": 'text-8 text-md-4'}).find("span").text.strip()
                except Exception:
                    price = ''
            min_price = ''
            for p in price.split('—')[0]:
                if p.isdigit():
                    min_price += p
            try:
                min_price = int(min_price)
            except Exception:
                min_price = 0
            try:
                category = soup.find_all(attrs={"data-id": 'category-spec'})[0].text.strip()
            except Exception:
                try:
                    category = soup.find(attrs={"class": 'text-5 mb-4 b-layout__txt_padbot_20'}).text.strip()
                except Exception:
                    category = ''
            try:
                podcategory = soup.find_all(attrs={"data-id": 'category-spec'})[1].text.strip()
            except Exception:
                podcategory = ''
            for word in words:
                if word in text or word in title:
                    await bot.send_message(1012882762, f"{category}\n\n{title}\n\n{text}\n\n{link}")
                    break
            result.append([title, link, category, podcategory, text, price])
            print(datetime.datetime.now())
            print([min_price, price, title, link, category, podcategory, text])
    return result


