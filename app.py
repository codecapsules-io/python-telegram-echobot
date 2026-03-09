from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import asyncio
import os

TOKEN = os.getenv("BOT_TOKEN")
URL = os.getenv("URL")

app = Flask(__name__)

def _build_ptb():
    ptb = Application.builder().token(TOKEN).build()

    async def start(update: Update, context):
        await update.message.reply_text("Hi! I respond by echoing messages. Give it a try!")

    async def echo(update: Update, context):
        await update.message.reply_text(update.message.text)

    ptb.add_handler(CommandHandler("start", start))
    ptb.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    return ptb

ptb_app = _build_ptb() if TOKEN else None


@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), ptb_app.bot)
    asyncio.run(ptb_app.process_update(update))
    return "ok"


@app.route("/setwebhook", methods=["GET", "POST"])
def set_webhook():
    success = asyncio.run(ptb_app.bot.set_webhook(f"{URL}webhook"))
    return "webhook setup ok" if success else "webhook setup failed"


@app.route("/")
def index():
    return "Hello, welcome to the telegram bot index page"
