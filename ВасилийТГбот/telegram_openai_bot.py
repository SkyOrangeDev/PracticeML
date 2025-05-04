import openai
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Set your OpenAI API key
openai.api_key = ''
def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text

    # Call OpenAI API
    response = openai.Completion.create(
        engine="gpt-4o-mini",
        prompt=user_message,
        max_tokens=150
    )

    # Extract the response text
    ai_response = response.choices[0].text.strip()

    # Send the response back to the user
    update.message.reply_text(ai_response)

# Define a function to start the bot
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Ку-ку')

def main() -> None:
    # Set your Telegram bot token
    updater = Updater("tg_token")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Register handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C
    updater.idle()

if __name__ == '__main__':
    main() 