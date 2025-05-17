import discord
from discord.ext import commands
import os
import config
import aiohttp
from io import BytesIO
import logging


bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

logging.basicConfig(level=logging.DEBUG, filename="logs.xml", filemode="w")

@bot.event
async def on_ready():
    """Событие запуска бота."""
    print(f"Бот {bot.user} запущен!")
    logging.debug(f"Bot {bot.user} is running!")
    
    await load_cogs()
    try:
        synced = await bot.tree.sync()
        print(f"Синхронизировано {len(synced)} команд: {synced}")
    except Exception as e:
        print(f"Ошибка синхронизации команд: {e}")


async def load_cogs():
    """Функция загрузки всех модулей (cogs)."""
    print("Загружаем модули...")
    logging.debug("Loading modules...")

    loaded_cogs = []
    failed_cogs = []

    for folder in os.listdir("./Modules"):
        cog_path = f"Modules.{folder}.main"
        if os.path.exists(f"./Modules/{folder}/main.py"):
            try:
                await bot.load_extension(cog_path)
                loaded_cogs.append(folder)
            except Exception as e:
                failed_cogs.append((folder, str(e)))

    print(f"Загруженные модули: {', '.join(loaded_cogs) if loaded_cogs else 'Нет'}")
    logging.info(f"Загруженные модули: {', '.join(loaded_cogs) if loaded_cogs else 'Нет'}")

    if failed_cogs:
        print("Не удалось загрузить следующие модули:")
        logging.critical("Не удалось загрузить следующие модули:")
        for cog, error in failed_cogs:
            print(f"- {cog}: {error}")
            logging.critical(f"- {cog}: {error}")


async def unload_cogs():
    """Функция выгрузки всех модулей (cogs)."""
    print("Выгружаем модули...")
    logging.debug("Выгружаем модули...")

    unloaded_cogs = []
    failed_cogs = []

    for folder in os.listdir("./Modules"):
        cog_path = f"Modules.{folder}.main"
        if os.path.exists(f"./Modules/{folder}/main.py"):
            try:
                await bot.unload_extension(cog_path)
                unloaded_cogs.append(folder)
            except Exception as e:
                failed_cogs.append((folder, str(e)))

    print(f"Выгруженные модули: {', '.join(unloaded_cogs) if unloaded_cogs else 'Нет'}")
    logging.info(f"Выгруженные модули: {', '.join(unloaded_cogs) if unloaded_cogs else 'Нет'}")
    if failed_cogs:
        print("Модули с ошибкой:")
        logging.critical("Модули с ошибкой:")
        for cog, error in failed_cogs:
            print(f"- {cog}: {error}")
            logging.critical(f"- {cog}: {error}")


@bot.command(name="reload", description="Перезагружает все модули бота")
@commands.has_role(config.SETTINGS["command_role"])
async def reload(interaction: discord.Interaction):
    """Команда для перезагрузки всех модулей."""
    await interaction.response.send_message("Перезагрузка модулей...")
    await unload_cogs()
    await load_cogs()
    await interaction.followup.send("Модули перезагружены!")


if __name__ == "__main__":
    try:
        bot.run(config.SETTINGS["TOKEN"])
    except Exception as e:
        print(f"Не удалось запустить бота: {e}")
        logging.critical(f"Не удалось запустить бота: {e}")