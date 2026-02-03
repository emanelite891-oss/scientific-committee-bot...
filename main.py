import os
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = os.getenv("BOT_TOKEN")

CHANNEL_USERNAME = "@HajjahUniversitystudents"

ADMINS = [7960489373, 7829681601, 5686534620]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.username != CHANNEL_USERNAME.replace("@", ""):
        return

    await update.message.reply_text(
        "مرحبًا 🌸\n"
        "هذا بوت اللجنة العلمية الدفعة الثانية_كلية الطب البشري_جامعة حجه\n\n"
        "من فضلك ارسل *اسم المادة* أولًا، ثم أرسل السؤال الذي تتذكره من الامتحان.",
        parse_mode="Markdown"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.username != CHANNEL_USERNAME.replace("@", ""):
        return

    text = update.message.text

    if "subject" not in context.user_data:
        context.user_data["subject"] = text
        await update.message.reply_text("✏️ الآن أرسل سؤالك.")
        return

    subject = context.user_data["subject"]

    for admin in ADMINS:
        await context.bot.send_message(
            chat_id=admin,
            text=f"📚 المادة: {subject}\n📩 السؤال:\n{text}"
        )

    context.user_data.clear()

    await update.message.reply_text(
        "🌸 شكرًا لك ، لقد تم ارسال رسالتك بنجاح الى المشرفات .. بالتوفيق 🤍"
    )


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()


if __name__ == "__main__":
    main()
