from aiogram import Dispatcher, types
from commands.db import get_name, getstatus, url_name
from commands.basic.status.db import *
from commands.main import win_luser
import config as cfg


async def status_list(message):
    name = await get_name(message.from_user.id)
    await message.answer(f'''{name}, доступные статусы в игре:

1️⃣ Standart VIP:
- Повышенный процент в банке
- Увеличенный шанс победы в играх
- Увеличен процент в депозите до 8%
- Уменьшен налог при снятии депозита до 4.5%
- Увеличен лимит передачи другим игрокам до 300.000.000.000.000$ в сутки
- Красивая отметка в профиле
- Возможность установить более длинный ник
- Время до получения ежедневного бонуса уменьшено в два раза
- Увеличена максимальная энергия до 25
- Увеличено количество открываемых кейсов до 20

2️⃣ Gold VIP:
- Увеличен шанс в играх
- Увеличен процент в депозите до 10%
- Уменьшен налог при снятии депозита до 3.5%
- Возможность установить ещё длинее ник
- Уникальный золотой ежедневный бонус
- Увеличен лимит передачи другим игрокам до 750.000.000.000.000$ в сутки
- Увеличена максимальная энергия до 50
- Увеличено количество открываемых кейсов до 40

3️⃣ Platinum VIP:
- Увеличен лимит передачи другим игрокам до 1.000.000.000.000.000$ в сутки
- Повышенный процент выигрыша в играх
- Увеличен процент в депозите до 12%
- Уменьшен налог при снятии депозита до 3%
- Увеличена максимальная энергия до 75
- Красивая отметка в профиле
- Опыт и добыча увеличена в два раза
- Увеличено количество открываемых кейсов до 60

4️⃣ Администратор:
- Выдача денег в сутки - 150.000.000.000.000
- Увеличен процент в депозите до 15%
- Уменьшен налог при снятии депозита до 2.5%
- Возможность просматривать профили других игроков
- Максимальная энергия увеличенная до 100
- Красивая отметка в профиле
- Увеличен лимит передачи другим игрокам до 30.000.000.000.000.000$ в сутки
- Увеличено количество открываемых кейсов до 250''')


async def donat_list(message):
    user_id = message.from_user.id
    url = await url_name(user_id)
    ecoins = await getecoins(user_id)
    adm_us = cfg.admin_username.replace('@', '')
    await message.answer(f'''{url}, наш магазин:

💵 Текущий курс: 1 RUB = 1 B-Coin
💸 Валюта: 1 B-Coin можно обменять на 2.000.000.000.000.000$

🪙 Обмен коинов на валюту: Обменять [количество]

🏆 Привилегии:
1️⃣ Standart VIP | 250 B-Coin
2️⃣ Gold VIP | 500 B-Coin
3️⃣ Platinum VIP | 750 B-Coin
4️⃣ Admin Status | 1.500 B-Coin

🔝Покупка: Купить привилегию [номер]

⚡️ Энергия:
    - 20 энергии | 15 B-Coin 
     🔝 Покупка: Купить флягу 1
    - 60 энергии | 35 B-Coin
     🔝 Покупка: Купить флягу 2

🚧 Лимит:
 - 350.000.000.000.000 | 100 B-Coin
🔝 Покупка: Купить лимит 1

- 3e18 | 1000 B-Coin
🔝 Покупка: Купить лимит 2

- 1e20 | 3000 B-Coin
🔝 Покупка: Купить лимит 3

- 2e21 | 6500 B-Coin
🔝 Покупка: Купить лимит 4

💰Ваш баланс: {ecoins} B-Coin
📲 Пополнить баланс: <a href="t.me/{adm_us}">{cfg.admin_username}</a>''', disable_web_page_preview=True)


async def my_status(message):
    user_id = message.from_user.id
    url = await url_name(user_id)
    status = await getstatus(user_id)
    privileges = {
        0: "к сожалению вы не владеете какими либо привилегиями",
        1: "🏆 Статус: Standart VIP\n🏦 Процент вклада: 8%\n💸 Лимит передачи: 300.000.000.000.000$/сутки",
        2: "🏆 Статус: Gold VIP\n🏦 Процент вклада: 10%\n💸 Лимит передачи: 750.000.000.000.000$/сутки",
        3: "🏆 Статус: Platinum VIP\n🏦 Процент вклада: 12%\n💸 Лимит передачи: 1.000.000.000.000.000$/сутки",
        4: "🏆 Статус: Администратор\n🏦 Процент вклада: 15%\n💸 Лимит передачи: 30.000.000.000.000.000$/сутки"
    }

    await message.answer(f'{url}, информация о привилегии:\n{privileges[status]}\nПодробнее об плюшках можно узнать введя команду "Статусы"')


async def buy_status(message: types.Message):
    user_id = message.from_user.id
    url = await url_name(user_id)
    ecoins = await getecoins(user_id)
    rwin, rloser = await win_luser()
    status = await getstatus(user_id)

    try:
        u = int(message.text.split()[2])
    except:
        await message.answer(f'{url}, вы не ввели число имущества или привелегии которое хотите купить {rloser}')
        return

    sttaus_list = {
        1: ("Standart VIP", 250),
        2: ("Gold VIP", 500),
        3: ("Platinum VIP", 750),
        4: ("Admin Status", 1500)
    }

    data = sttaus_list.get(u, 'no')
    if data == 'no':
        await message.answer(f'{url}, данного доната не существует. Проверьте введеную вами цифру.')
        return

    if ecoins < data[1]:
        await message.answer(f'{url},к сожалению у вас недостаточно B-Coins для покупки данной привелегии, '
                             f'чтобы пополнить напишите команду "Донат" {rloser}')
        return

    if status > u:
        await message.answer(f'{url}, у вас уже есть этот или более высокий статус {rwin}.')
        return

    await buy_status_db(user_id, data[1], u)
    await message.answer(f'{url}, вы успешко купили статус "{data[0]}" за {data[1]} B-Coins {rwin}.')


async def exchange_value(message: types.Message):
    user_id = message.from_user.id
    url = await url_name(user_id)
    ecoins = await getecoins(user_id)
    rwin, rloser = await win_luser()

    try:
        u = int(message.text.split()[1])
    except:
        u = 1

    if u > 1000 or u <= 0:
        return

    if ecoins < u:
        await message.answer(f'На твоём счету {ecoins} B-Coins, чтобы пополнить введите - Донат {rloser}')
        return

    summ = u * 2000000000000000  # сумма денег за 1 B-Coin
    summ2 = '{:,}'.format(summ).replace(',', '.')

    await exchange_value_db(user_id, summ, u)
    await message.answer(f'{url}, вы обменяли {u} B-Coins на {summ2}$ {rwin}')


async def buy_limit(message: types.Message):
    user_id = message.from_user.id
    url = await url_name(user_id)
    ecoins = await getecoins(user_id)
    rwin, rloser = await win_luser()

    try:
        u = int(message.text.split()[2])
    except:
        await message.answer(f'{url}, вы не ввели число имущества или привелегии которое хотите купить {rloser}')
        return

    # номер лимита: (лимит, стоимость)
    limit_list = {
        1: (350000000000000, 100),
        2: (3000000000000000000, 1000),
        3: (100000000000000000000, 3000),
        4: (2000000000000000000000, 6500),
    }

    data = limit_list.get(u, 'no')

    if data == 'no':
        return

    if ecoins < data[1]:
        await message.answer(f'{url}, к сожалению у вас недостаточно B-Coins для покупки лимита,'
                             f' чтобы пополнить напишите команду "Донат" {rloser}')
        return

    summ2 = '{:,}'.format(data[0]).replace(',', '.')

    await buy_limit_db(user_id, data[0], data[1])
    await message.answer(f'{url}, вы увеличили свой лимит передачи на {summ2}$ за {data[1]} B-Coins {rwin}')


def reg(dp: Dispatcher):
    dp.register_message_handler(donat_list, lambda message: message.text.lower().startswith('донат'))
    dp.register_message_handler(status_list, lambda message: message.text.lower().startswith('статусы'))
    dp.register_message_handler(my_status, lambda message: message.text.lower().startswith('мой статус'))
    dp.register_message_handler(buy_status, lambda message: message.text.lower().startswith('купить привилегию'))
    dp.register_message_handler(exchange_value, lambda message: message.text.lower().startswith('обменять'))
    dp.register_message_handler(buy_limit, lambda message: message.text.lower().startswith('купить лимит'))