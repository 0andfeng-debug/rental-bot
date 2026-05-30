import os
import requests
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[KeyboardButton("📍 傳送我的位置", request_location=True)]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "👋 歡迎使用租屋搜尋助手！\n\n請點下方按鈕傳送您的位置，我會幫您搜尋附近20公里內的租屋資訊。",
        reply_markup=reply_markup
    )

async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lat = update.message.location.latitude
    lon = update.message.location.longitude
    
    await update.message.reply_text("🔍 正在搜尋附近租屋資訊，請稍候...")
    
    # 產生各租屋平台的搜尋連結
    msg = f"""
📍 已收到您的位置（{lat:.4f}, {lon:.4f}）

以下是附近租屋搜尋連結：

🏠 **591租屋網**
https://rent.591.com.tw/?geo={lat},{lon}&radius=20

🏡 **樂屋網**
https://www.rakuya.com.tw/search/rental?lat={lat}&lng={lon}&distance=20

🔎 **好房網**
https://rent.housefun.com.tw/search/?lat={lat}&lng={lon}

🗺️ **Google地圖租屋搜尋**
https://www.google.com/maps/search/租屋/@{lat},{lon},12z

點選連結即可查看附近租屋資訊！
"""
    await update.message.reply_text(msg, parse_mode='Markdown')

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.LOCATION, handle_location))
    app.run_polling()
