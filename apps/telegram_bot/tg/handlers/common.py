import logging

from telegram import Update, Message
from telegram.ext import ConversationHandler, CallbackQueryHandler

from apps.telegram_bot.core.custom_handlers import CommandHandlerCustom
from apps.telegram_bot.core.routers import Router
from apps.telegram_bot.tg.elements import common
from apps.telegram_bot.core.context import CustomContext

logger = logging.getLogger(__name__)


common_router = Router()


@common_router.register_handler(
    class_handler=CommandHandlerCustom,
    command='help',
    description='Справка',
    show_command=True,
)
async def handle_help(update: Update, context: CustomContext) -> None:
    """Send a message when the command /help is issued."""
    if not update.message:
        raise ValueError()
    msg = common.HelpMessage()
    await update.message.reply_text(msg.text, msg.parse_mode)


async def error_handler(update: Update, context: CustomContext) -> None:
    """Логирует ошибку и отправляет уведомление пользователю."""
    error_msg = f'⚠️ Произошла ошибка: {context.error}'
    logging.error(context.error, exc_info=context.error)

    # Пытаемся отправить сообщение пользователю
    if update and update.effective_chat:
        try:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=error_msg)
        except Exception as e:
            logging.error('Не удалось отправить сообщение пользователю!', exc_info=e)


async def timeout_handle(update: Update, context: CustomContext) -> int:
    if update.callback_query:
        await update.callback_query.edit_message_reply_markup()

    return ConversationHandler.END


@common_router.register_handler(
    class_handler=CallbackQueryHandler,
    pattern=common.IGNORE.rejex,
)
async def ignore_callback(update: Update, context: CustomContext) -> None:
    if update.callback_query:
        await update.callback_query.answer()


@common_router.register_handler(
    class_handler=CommandHandlerCustom,
    command='start',
    description='Старт телеграм бота',
    show_command=True,
)
async def handle_start(update: Update, context: CustomContext) -> None:
    if update.effective_message and update.effective_user:
        msg = common.StartMessage(update.effective_user.full_name)
        await update.effective_message.reply_text(msg.text)


@common_router.register_handler(
    class_handler=CallbackQueryHandler,
    pattern=common.MENU_CLOSE.rejex,
)
async def menu_close(update: Update, context: CustomContext) -> None:
    if update.callback_query and update.callback_query.message:
        chat_id = update.callback_query.message.chat.id
        message_id = update.callback_query.message.message_id

        await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
    elif update.effective_message:
        await update.effective_message.delete()


@common_router.register_handler(
    class_handler=CallbackQueryHandler,
    pattern='.*',
)
async def unknown_callback(update: Update, context: CustomContext) -> int:
    if not update.callback_query or not update.callback_query.message:
        return ConversationHandler.END

    message = update.callback_query.message
    if not isinstance(message, Message):  # Проверяем, что это доступное сообщение
        return ConversationHandler.END

    try:
        await message.edit_reply_markup()
        msg = common.BadCallbackMessage()
        await message.reply_text(msg.text, parse_mode=msg.parse_mode)
    except Exception as e:
        logging.error(f'Error in unknown_callback: {e}')

    return ConversationHandler.END
