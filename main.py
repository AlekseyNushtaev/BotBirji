import asyncio
import datetime
import time

from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import Chrome
from db.models import init_db
from db.util import add_orders_to_db, res_old_links, del_old_orders
from market.fl import parser_fl
from market.kwork import parser_kwork
from market.youdo import parser_youdo


async def main():
    await init_db()
    chrome_driver_path = ChromeDriverManager().install()
    browser_service = Service(executable_path=chrome_driver_path)
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument("window-size=1400,600")
    options.add_argument('--disable-dev-shm-usage')
    options.page_load_strategy = 'eager'
    browser = Chrome(service=browser_service, options=options)
    flag = True
    while True:
        start = datetime.datetime.now()
        await del_old_orders()
        res_old = await res_old_links()
        print(len(res_old))
        try:
            result_fl = await parser_fl(browser, res_old)
            await add_orders_to_db(result_fl, 'fl', flag)
        except Exception:
            time.sleep(30)
        try:
            result_kwork = await parser_kwork(browser, res_old)
            await add_orders_to_db(result_kwork, 'kwork', flag)
        except Exception:
            time.sleep(30)
        time.sleep(20)
        # result_youdo = parser_youdo(browser, res_old)
        # await add_orders_to_db(result_youdo, 'youdo', flag)
        delta = datetime.datetime.now() - start
        flag = False
        print(delta)



if __name__ == "__main__":
    start = datetime.datetime.now()
    asyncio.run(main())