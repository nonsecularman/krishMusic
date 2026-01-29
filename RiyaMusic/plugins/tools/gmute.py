from pyrogram import Client, filters
from pyrogram.types import Message

from config import OWNER_ID

# ✅ SUDO LIST (Manual Add)
SUDO_USERS = [OWNER_ID]

# GMUTED USERS STORE
GMUTED_USERS = set()


# ✅ Permission Check
def is_owner_or_sudo(user_id: int):
    return user_id in SUDO_USERS


# ✅ /gmute Command
@Client.on_message(filters.command("gmute") & filters.group)
async def gmute_user(client, message: Message):

    if not is_owner_or_sudo(message.from_user.id):
        return await message.reply_text(
            "❌ Only OWNER & SUDO can use /gmute!"
        )

    if not message.reply_to_message:
        return await message.reply_text(
            "⚠️ Reply to a user message then type:\n/gmute"
        )

    user_id = message.reply_to_message.from_user.id
    GMUTED_USERS.add(user_id)

    await message.reply_text(
        f"✅ GMUTED!\nअब `{user_id}` के सारे msg delete होंगे."
    )


# ✅ /ungmute Command
@Client.on_message(filters.command("ungmute") & filters.group)
async def ungmute_user(client, message: Message):

    if not is_owner_or_sudo(message.from_user.id):
        return await message.reply_text(
            "❌ Only OWNER & SUDO can use /ungmute!"
        )

    if not message.reply_to_message:
        return await message.reply_text(
            "⚠️ Reply to a user message then type:\n/ungmute"
        )

    user_id = message.reply_to_message.from_user.id

    if user_id not in GMUTED_USERS:
        return await message.reply_text("⚠️ User is not GMUTED!")

    GMUTED_USERS.remove(user_id)

    await message.reply_text(
        f"✅ UNGMUTED!\nअब `{user_id}` के msg delete नहीं होंगे."
    )


# ✅ Auto Delete GMUTED Messages
@Client.on_message(filters.group)
async def delete_gmuted_messages(client, message: Message):

    if message.from_user and message.from_user.id in GMUTED_USERS:
        try:
            await message.delete()
        except:
            pass
