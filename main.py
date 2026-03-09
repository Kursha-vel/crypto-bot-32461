import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
import asyncio
import aiohttp
import json

TOKEN = os.environ.get("TELEGRAM_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Приветствую! Этот бот показывает курс Bitcoin и Ethereum каждые 12 часов. Ожидайте обновлений...")

async def send_crypto_price(context: ContextTypes.DEFAULT_TYPE):
    async with aiohttp.ClientSession() as session:
        async with session.get("https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD") as response:
            bitcoin_data = await response.json()
            bitcoin_price = bitcoin_data["USD"]
        
        async with session.get("https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD") as response:
            ethereum_data = await response.json()
            ethereum_price = ethereum_data["USD"]
        
        for chat_id in context.application.chat_ids:
            await context.bot.send_message(chat_id=chat_id, text=f"Курс Bitcoin: {bitcoin_price} USD\nКурс Ethereum: {ethereum_price} USD")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    
    app.job_queue.run_repeating(send_crypto_price, interval=43200, first=0)
    
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()