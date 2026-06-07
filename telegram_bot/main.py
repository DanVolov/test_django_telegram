import os
import sys
import django

# КРИТИЧНО: очистить переменные прокси ДО ВСЕХ импортов
for var in list(os.environ.keys()):
    if 'proxy' in var.lower() or 'socks' in var.lower():
        print(f"Удаляю переменную: {var} = {os.environ[var]}")
        del os.environ[var]

# Добавляем путь к Django проекту
django_project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'django_telegram'))
sys.path.insert(0, django_project_path)

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')
django.setup()

import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.request import HTTPXRequest
import httpx
from asgiref.sync import sync_to_async
from site_form.models import SiteModel

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = "8783968299:AAEAGuziNF2gFmbjZbk-cMlZYDQ7sfYfZTY"


class CustomHTTPXRequest(HTTPXRequest):
    def _build_client(self) -> httpx.AsyncClient:
        return httpx.AsyncClient(
            timeout=httpx.Timeout(timeout=30.0),
            limits=httpx.Limits(
                max_connections=32,
                max_keepalive_connections=32,
            ),
            trust_env=False,
        )


def get_all_forms_data():
    """Получение всех форм из БД - СИНХРОННАЯ функция"""
    forms = SiteModel.objects.all()
    # Собираем все данные ВНУ ЭТОЙ функции
    data = []
    for form in forms:
        data.append({
            'name': form.name,
            'surname': form.surname,
            'text': form.text,
            'date': form.date.strftime('%d.%m.%Y %H:%M:%S')
        })
    return data


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    try:
        # Получаем все данные в синхронном контексте
        forms_data = await sync_to_async(get_all_forms_data)()
        count = len(forms_data)

        message = f'Всего записей в БД: {count}\n'
        # Если есть данные, выводим их
        if count > 0:
            for i, form in enumerate(forms_data, 1):
                message += f"""
{i}.
Имя: {form['name']}
Фамилия: {form['surname']}
Текст: {form['text']}
Дата: {form['date']}
"""

        await update.message.reply_text(message)
    except Exception as e:
        logger.error(f"Ошибка в start: {e}", exc_info=True)
        await update.message.reply_text("❌ Произошла ошибка при получении данных")


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик ошибок"""
    logger.error(msg="Exception:", exc_info=context.error)


def main():
    """Главная функция запуска бота"""
    try:
        logger.info("🚀 Запуск бота...")

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