import install
import importlib
from aiogram import executor
from assets.filters import FilterAdmin
from assets.auto import automatisation
from commands.basic.ore.db import autokursbtc_new
from assets.modules import load_modules
from bot import dp


MODULES = [
    'commands.basic.property.main',
    'commands.admin.admin',
    'commands.entertaining.earnings.farm.main',
    'commands.entertaining.earnings.business.main',
    'commands.entertaining.earnings.garden.main',
    'commands.entertaining.earnings.generator.main',
    'commands.entertaining.earnings.tree.main',
    'commands.entertaining.earnings.quarry.main',
    'commands.basic.balance',
    'commands.basic.status.main',
    'commands.basic.ore.main',
    'commands.help',
    'commands.entertaining.rz',
    'commands.basic.top',
    'commands.entertaining.wedlock',
    'commands.clans.main',
    'commands.admin.promo',
    'commands.games.main',
    'commands.basic.bank.main',
    'commands.entertaining.case.main',
    'commands.entertaining.earnings.garden.potions',
    'commands.basic.transfer',
    'commands.main',
]


async def main(dp):
    load_modules(dp)
    await autokursbtc_new()
    await automatisation()


def reg_handlers():
    for module_path in MODULES:
        module = importlib.import_module(module_path)
        if hasattr(module, 'reg'):
            module.reg(dp)


def reg_filters():
    dp.filters_factory.bind(FilterAdmin)


if __name__ == '__main__':
    reg_filters()
    reg_handlers()
    executor.start_polling(dp, on_startup=main, skip_updates=True)
