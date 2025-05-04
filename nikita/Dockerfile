FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements (create this file first with dependencies)
COPY nikita/simple_tg_bot/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy bot files
COPY nikita/simple_tg_bot/ .

# Set environment variables from .env file at runtime
ENV TELEGRAM_TOKEN=""
ENV OPENAI_API_KEY=""

# Run the bot
CMD ["python", "bot.py"]
