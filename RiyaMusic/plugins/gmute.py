from pyrogram import filters
from pyrogram.types import Message

from RiyaMusic import app
from config import OWNER_ID

GMUTED_USERS = set()


@app.on_message(filters.command("gmute") & filters.group)
async def gmute_user(_, message: Message):

    if message.from_user.id != OWNER_ID:
        return await message.reply_text("❌ Only OWNER!")

    if not message.reply_to_message:
        return await message.reply_text("⚠️ Reply to user!")

    user_id = message.reply_to_message.from_user.id
    GMUTED_USERS.add(user_id)

    await message.reply_text("✅ User GMUTED!")


@app.on_message(filters.command("ungmute") & filters.group)
async def ungmute_user(_, message: Message):

    if message.from_user.id != OWNER_ID:
        return await message.reply_text("❌ Only OWNER!")

    if not message.reply_to_message:
        return await message.reply_text("⚠️ Reply to user!")

    user_id = message.reply_to_message.from_user.id

    GMUTED_USERS.discard(user_id)
    await message.reply_text("✅ User UNMUTED!")


@app.on_message(filters.group & ~filters.command(["gmute", "ungmute"]))
async def delete_gmuted(_, message: Message):

    if message.from_user and message.from_user.id in GMUTED_USERS:
        try:
            await message.delete()
        except:
            pass
