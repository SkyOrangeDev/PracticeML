from aiogram import Router, types
from aiogram.filters import Command
from bot.services.openai_service import OpenAIService
from bot.database.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

router = Router()
openai_service = OpenAIService()

@router.message(Command("start"))
async def cmd_start(message: types.Message, session: AsyncSession):
    user = await session.get(User, message.from_user.id)
    if not user:
        user = User(
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            is_admin=False
        )
        session.add(user)
        await session.commit()
    
    await message.answer(
        "Привет! Я ИИ-ассистент. Задайте мне вопрос, и я постараюсь помочь."
    )

@router.message(Command("help"))
async def cmd_help(message: types.Message):
    help_text = """
Доступные команды:
/start - Начать работу с ботом
/help - Показать это сообщение

Просто напишите мне сообщение, и я постараюсь помочь!
    """
    await message.answer(help_text)

@router.message()
async def handle_message(message: types.Message, session: AsyncSession):
    # Обновляем время последней активности пользователя
    user = await session.get(User, message.from_user.id)
    if user:
        user.last_activity = datetime.now()
        await session.commit()
    
    # Показываем индикатор набора сообщения
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action="typing"
    )
    
    # Генерируем ответ через OpenAI
    response = await openai_service.generate_response(message.text)
    
    if response:
        # Разбиваем длинные сообщения на части
        if len(response) > 4096:
            for i in range(0, len(response), 4096):
                await message.answer(response[i:i+4096])
        else:
            await message.answer(response)
    else:
        await message.answer(
            "Извините, произошла ошибка при обработке вашего запроса. "
            "Пожалуйста, попробуйте позже."
        ) 