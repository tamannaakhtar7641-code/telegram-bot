import logging
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CallbackQueryHandler, CommandHandler, filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = "8839361164:AAH_bC4B3d2reCilKhyvMsFjMwGebTYF1Bg"
REQUIRED_CHANNEL = "@YourChannelUsername"
ALL_CHANNELS_LINK = "https://t.me/addlist/F5fxxWGnll43MDY1"
PRIVATE_CHANNEL_ID = -100xxxxxxxxxx

DATABASE = {
    "cid": [],
    "hot": [],
    "natok": [],
    "bangla": [],
    "hindi": []
}

async def moderate_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message or not message.text:
        return
    if message.chat.type in ["group", "supergroup"]:
        text = message.text.lower()
        if "http://" in text or "https://" in text or "t.me/" in text or "@" in text:
            try:
                await message.delete()
            except Exception as e:
                print(f"Error: {e}")

async def auto_receive_from_private_channel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if message and message.chat.id == PRIVATE_CHANNEL_ID and message.video:
        caption = (message.caption or "").lower()
        file_id = message.video.file_id

        if "#cid" in caption:
            DATABASE["cid"].append(file_id)
        elif "#hot" in caption:
            DATABASE["hot"].append(file_id)
        elif "#natok" in caption:
            DATABASE["natok"].append(file_id)
        elif "#bangla" in caption:
            DATABASE["bangla"].append(file_id)
        elif "#hindi" in caption:
            DATABASE["hindi"].append(file_id)

async def check_subscription(user_id, context):
    try:
        member = await context.bot.get_chat_member(chat_id=REQUIRED_CHANNEL, user_id=user_id)
        if member.status in ["member", "administrator", "creator"]:
            return True
    except:
        pass
    return False

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not await check_subscription(user_id, context):
        keyboard = [
            [InlineKeyboardButton("📢 প্রধান চ্যানেলে জয়েন করুন", url=f"https://t.me/{REQUIRED_CHANNEL.replace('@', '')}")],
            [InlineKeyboardButton("📂 ১ ক্লিকে সব চ্যানেলের ফোল্ডার লিংক", url=ALL_CHANNELS_LINK)],
            [InlineKeyboardButton("🔄 জয়েন করে এখানে ক্লিক করুন", callback_data="check_join")]
        ]
        await update.message.reply_text(
            "⚠️ **সতর্কবাণী!**\n\nআমাদের বটের ভিডিও দেখতে হলে অবশ্যই আমাদের চ্যানেলে জয়েন থাকতে হবে। আগে চ্যানেলে জয়েন করুন তারপর নিচের বাটনে চাপ দিন 👇",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    keyboard = [
        [InlineKeyboardButton("🔥 ┋ হট ভিডিও কালেকশন ┋ 🔥", callback_data="hot_videos")],
        [InlineKeyboardButton("🕵️‍♂️ ┋ সিআইডি (CID) এপিসোড ┋ 🕵️‍♂️", callback_data="cid_videos")],
        [InlineKeyboardButton("🎭 ┋ ব্যাচেলার পয়েন্ট নাটক ┋ 🎭", callback_data="natok_videos")],
        [InlineKeyboardButton("🎬 ┋ বাংলা ডাবিং মুভি ┋ 🎬", callback_data="bangla_dubbed")],
        [InlineKeyboardButton("🍿 ┋ হিন্দি ড্রামা মুভি ┋ 🍿", callback_data="hindi_movies")],
        [InlineKeyboardButton("📂 এক ক্লিকে সব চ্যানেলে জয়েন করুন", url=ALL_CHANNELS_LINK)]
    ]
    await update.message.reply_text(
        "🌟 **আমাদের অফিশিয়াল মিডিয়া বটে আপনাকে স্বাগতম!** ❤️\n\nআপনার পছন্দের ক্যাটাগরি নিচে দেওয়া হলো, যেকোনো একটিতে ক্লিক করুন 👇",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if query.data == "check_join":
        if await check_subscription(user_id, context):
            await query.message.delete()
            await start_command(update, context)
        else:
            await query.answer("❌ আপনি এখনো চ্যানেলে জয়েন করেননি!", show_alert=True)
        return

    category_map = {
        "hot_videos": ("hot", "🔥 হট ভিডিও"),
        "cid_videos": ("cid", "🕵️‍♂️ সিআইডি এপিসোড"),
        "natok_videos": ("natok", "🎭 ব্যাচেলার পয়েন্ট নাটক"),
        "bangla_dubbed": ("bangla", "🎬 বাংলা ডাবিং মুভি"),
        "hindi_movies": ("hindi", "🍿 হিন্দি ড্রামা মুভি")
    }

    if query.data in category_map:
        key, name = category_map[query.data]
        videos = DATABASE.get(key, [])

        if videos:
            video_id = videos[-1] 
            await context.bot.send_video(chat_id=query.message.chat_id, video=video_id, caption=f"📥 আপনার কাঙ্ক্ষিত {name}টি দেওয়া হলো!")
        else:
            await query.message.reply_text(f"❌ এই মুহূর্তে {name}-এর কোনো ভিডিও পাওয়া যায়নি।")

async def auto_post_job(context: ContextTypes.DEFAULT_TYPE):
    chat_id = -1001234567890
    posts = [
        {"photo": "https://i.ibb.co/3W59xv8/girl.jpg", "caption": "🔥 **এক্সক্লুসিভ হট ভিডিও আপডেট!**"},
        {"photo": "https://i.ibb.co/3W59xv8/cid.jpg", "caption": "🕵️‍♂️ **CID Season 2 Bangla এপিসোড!**"}
    ]
    selected = random.choice(posts)
    keyboard = [
        [InlineKeyboardButton("📥 ভিডিও দেখতে এখানে চাপ দিন", url=f"https://t.me/YourBotUsername?start=start")],
        [InlineKeyboardButton("📂 এক ক্লিকে সব চ্যানেলে জয়েন করুন", url=ALL_CHANNELS_LINK)]
    ]
    try:
        await context.bot.send_photo(chat_id=chat_id, photo=selected["photo"], caption=selected["caption"], reply_markup=InlineKeyboardMarkup(keyboard))
    except Exception as e:
        print(f"Auto post error: {e}")

async def post_init(application):
    job_queue = application.job_queue
    job_queue.run_repeating(auto_post_job, interval=60, first=10)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).post_init(post_init).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), moderate_group))
    app.add_handler(MessageHandler(filters.VIDEO & filters.Chat(PRIVATE_CHANNEL_ID), auto_receive_from_private_channel))
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CallbackQueryHandler(button_click))
    app.run_polling(drop_pending_updates=True)
