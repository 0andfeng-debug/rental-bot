import os
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN")

user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[KeyboardButton("📍 傳送我的位置", request_location=True)]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "👋 歡迎使用租屋搜尋助手！\n\n請點下方按鈕傳送您的位置。",
        reply_markup=reply_markup
    )

async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lat = update.message.location.latitude
    lon = update.message.location.longitude
    user_id = update.message.from_user.id
    user_data[user_id] = {"lat": lat, "lon": lon}

    keyboard = [
        [InlineKeyboardButton("💰 不限金額", callback_data=f"budget_0_{lat}_{lon}")],
        [InlineKeyboardButton("💵 5000以下", callback_data=f"budget_5000_{lat}_{lon}")],
        [InlineKeyboardButton("💵 5000～8000", callback_data=f"budget_8000_{lat}_{lon}")],
        [InlineKeyboardButton("💵 8000～12000", callback_data=f"budget_12000_{lat}_{lon}")],
        [InlineKeyboardButton("💵 12000～20000", callback_data=f"budget_20000_{lat}_{lon}")],
        [InlineKeyboardButton("💵 20000以上", callback_data=f"budget_99999_{lat}_{lon}")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("📍 已收到位置！\n\n請選擇租金範圍：", reply_markup=reply_markup)

async def handle_budget(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data.split("_")
    budget = data[1]
    lat = data[2]
    lon = data[3]

    budget_labels = {
        "0": "不限金額",
        "5000": "5000以下",
        "8000": "5000～8000",
        "12000": "8000～12000",
        "20000": "12000～20000",
        "99999": "20000以上",
    }
    budget_label = budget_labels.get(budget, "不限")

    # 591 金額對應
    price_map = {
        "0": "",
        "5000": "&price=0%2C5000",
        "8000": "&price=5000%2C8000",
        "12000": "&price=8000%2C12000",
        "20000": "&price=12000%2C20000",
        "99999": "&price=20000%2C",
    }
    price_param = price_map.get(budget, "")

    msg = (
        f"🔍 搜尋條件：{budget_label}｜位置：({float(lat):.4f}, {float(lon):.4f})\n\n"

        f"🏠 *591租屋網*\n"
        f"https://rent.591.com.tw/?kind=0&region=1{price_param}\n\n"

        f"🏡 *樂屋網*\n"
        f"https://www.rakuya.com.tw/search/rental\n\n"

        f"💬 *Facebook社團搜尋（高雄租屋）*\n"
        f"https://www.facebook.com/search/groups/?q=高雄租屋\n\n"

        f"💬 *Dcard租屋版*\n"
        f"https://www.dcard.tw/f/rental\n\n"

        f"🏛️ *租屋補助查詢（內政部）*\n"
        f"https://www.moi.gov.tw/cl.aspx?n=15413\n\n"

        f"🏛️ *高雄市租屋補助*\n"
        f"https://www.kmhud.gov.tw/rent-subsidy\n\n"

        f"🗺️ *Google地圖搜尋附近租屋*\n"
        f"https://www.google.com/maps/search/租屋/@{lat},{lon},13z"
    )

    await query.edit_message_text(msg, parse_mode='Markdown')

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.LOCATION, handle_location))
    app.add_handler(CallbackQueryHandler(handle_budget, pattern="^budget_"))
    app.run_polling()
