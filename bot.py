import os
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

BOT_TOKEN = os.environ.get("BOT_TOKEN")

def start(update: Update, context):
    keyboard = [[KeyboardButton("📍 傳送我的位置", request_location=True)]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text(
        "👋 歡迎使用租屋搜尋助手！\n\n請點下方按鈕傳送您的位置，我會幫您搜尋附近20公里內的租屋資訊。",
        reply_markup=reply_markup
    )

def handle_location(update: Update, context):
    lat = update.message.location.latitude
    lon = update.message.location.longitude

    update.message.reply_text("🔍 正在搜尋附近租屋資訊，請稍候...")

    msg = (
        f"📍 已收到您的位置（{lat:.4f}, {lon:.4f}）\n\n"
        f"以下是附近租屋搜尋連結：\n\n"
        f"🏠 591租屋網\n"
        f"https://rent.591.com.tw/?geo={lat},{lon}&radius=20\n\n"
        f"🏡 樂屋網\n"
        f"https://www.rakuya.com.tw/search/rental?lat={lat}&lng={lon}&distance=20\n\n"
        f"🔎 好房網\n"
        f"https://rent.housefun.com.tw/search/?lat={lat}&lng={lon}\n\n"
        f"🗺️ Google地圖租屋搜尋\n"
        f"https://www.google.com/maps/search/租屋/@{lat},{lon},12z"
    )

    update.message.reply_text(msg)

def main():
    updater = Updater(BOT_TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.location, handle_location))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
