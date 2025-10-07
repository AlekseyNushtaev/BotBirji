import datetime

from sqlalchemy import select, insert, update, delete

from db.models import Session, Order


async def res_old_links():
    res_old = []
    async with Session() as session:
        query = select(Order.link)
        results = await session.execute(query)
        for result in results.all():
            res_old.append(result[0])
    return res_old


async def add_orders_to_db(result, market, flag):
    async with Session() as session:
        for order in result:
            try:
                stmt = insert(Order).values(
                    market=market,
                    title=order[0],
                    link=order[1],
                    category=order[2],
                    podcategory=order[3],
                    text=order[4],
                    price=order[5],
                    time_start=datetime.datetime.now(),
                    flag=flag
                )
                await session.execute(stmt)
                await session.commit()
            except Exception as e:
                print(e)


async def del_old_orders():
    async with Session() as session:
        stmt = delete(Order).where(Order.time_start < datetime.datetime.now() - datetime.timedelta(days=3))
        await session.execute(stmt)
        await session.commit()
