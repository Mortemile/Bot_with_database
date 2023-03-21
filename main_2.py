import json
import random

from aiohttp import ClientSession

from db import SQLighter  # class database

from auth_data import token  # bot's token

from aiogram import Bot, Dispatcher, executor, types
import asyncio

# initialize bot
bot = Bot(token=token)
dp = Dispatcher(bot)

# initialize database
db = SQLighter('user.db')


# subscribe command
@dp.message_handler(commands='subscribe')
async def subscribe(message: types.Message):
    if not db.subscriber_exists(message.from_user.id):
        # add user with subscription
        db.add_subscriber(message.from_user.id, True)
    else:
        # refresh status
        db.update_subscription(message.from_user.id, True)

    await message.answer(
        "Вы успешно подписались на рассылку!\nОжидайте, ваше послание уже в пути ✌")


# unsubscribe command
@dp.message_handler(commands='unsubscribe')
async def unsubscribe(message: types.Message):
    if not db.subscriber_exists(message.from_user.id):
        # add user without subscription
        db.add_subscriber(message.from_user.id)
        await message.answer("Вы и так не подписаны.")
    else:
        # refresh status
        db.update_subscription(message.from_user.id, False)
        await message.answer("Вы успешно отписались от рассылки 🥲")


async def scheduled():
    async with ClientSession(trust_env=True) as session:
        while True:
            random.seed()
            wait_for = random.randint(1, 10)
            # print(wait_for)

            await asyncio.sleep(wait_for)

            headers = {
                'Content-Type': 'application/json'
            }

            # get list of subs with status = TRUE
            subscriptions = db.get_subscriptions()  # return this - [(2, '431733517', 1)]

            # send message
            for s in subscriptions:

                message = {
                    'chat_id': f'{s[1]}',
                    'text': 'test message'
                }

                API_URL = 'https://api.telegram.org/bot5646936515:AAEnCioBeqCOzjy7zbX4o9Kna9VWV3agdBM/sendMessage'

                async with session.post(API_URL, data=json.dumps(message), headers=headers) as resp:
                    try:
                        assert resp.status == 200
                    except:
                        print('Something went wrong :(')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(scheduled())  # set time

    executor.start_polling(dp, skip_updates=True)

    # schedule.every(4).seconds.do(scheduled)  # second variant
    # while True:
    #     schedule.run_pending()
