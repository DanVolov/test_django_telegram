import os
import sys

# КРИТИЧНО: очистить переменные прокси ДО ВСЕХ импортов
for var in list(os.environ.keys()):
    if 'proxy' in var.lower() or 'socks' in var.lower():
        print(f"Удаляю переменную: {var} = {os.environ[var]}")
        del os.environ[var]

import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.request import HTTPXRequest
import httpx


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = "8783968299:AAEAGuziNF2gFmbjZbk-cMlZYDQ7sfYfZTY"  # Замените на ваш токен


class CustomHTTPXRequest(HTTPXRequest):
    """Кастомный HTTPXRequest без поддержки переменных окружения для прокси"""

    def _build_client(self) -> httpx.AsyncClient:
        """Создание клиента без чтения переменных окружения для прокси"""
        return httpx.AsyncClient(
            timeout=httpx.Timeout(timeout=30.0),
            limits=httpx.Limits(
                max_connections=32,
                max_keepalive_connections=32,
            ),
            trust_env=False,  # КРИТИЧНО: отключить чтение переменных окружения
        )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    await update.message.reply_text('hi')


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик ошибок"""
    logger.error(msg="Exception:", exc_info=context.error)


def main():
    """Главная функция запуска бота"""
    try:
        logger.info("🚀 Запуск бота...")

        # Использование кастомного HTTPXRequest для обоих типов запросов
        request = CustomHTTPXRequest()

        app = Application.builder().token(TOKEN).request(request).get_updates_request(request).build()

        app.add_handler(CommandHandler("start", start))
        app.add_error_handler(error_handler)

        logger.info("✅ Бот успешно запущен!")
        app.run_polling(allowed_updates=Update.ALL_TYPES)

    except Exception as e:
        logger.error(f"❌ Ошибка запуска бота: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()