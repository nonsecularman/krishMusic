
import re
import requests
from pyrogram import filters
from pyrogram.types import Message

from RiyaMusic import app
from config import LOGGER_ID


# Function to download and send Instagram media
async def send_instagram_media(message: Message, url: str):
    processing_msg = await message.reply_text("ᴘʀᴏᴄᴇssɪɴɢ...")
    api_url = f"https://insta-dl.hazex.workers.dev/?url={url}"

    try:
        response = requests.get(api_url)
        result = response.json()
        data = result.get("result", {})
    except Exception as e:
        error_msg = f"Eʀʀᴏʀ:\n{e}"
        try:
            await processing_msg.edit(error_msg)
        except Exception:
            await message.reply_text(error_msg)
            await app.send_message(LOGGER_ID, error_msg)
        return await app.send_message(LOGGER_ID, error_msg)

    if not result.get("error", True) and data.get("url"):
        video_url = data["url"]
        duration = data.get("duration", "Unknown")
        quality = data.get("quality", "Unknown")
        extension = data.get("extension", "Unknown")
        size = data.get("formattedSize", "Unknown")
        caption = (
            f"Dᴏᴡɴʟᴏᴀᴅᴇᴅ Bʏ : @kryshmusicbot\nPᴏᴡᴇʀᴇᴅ Bʏ : @iscamz"
        )
        await processing_msg.delete()
        await message.reply_video(video_url, caption=caption)
    else:
        try:
            await processing_msg.edit("Fᴀɪʟᴇᴅ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ ʀᴇᴇʟ")
        except Exception:
            await message.reply_text("Fᴀɪʟᴇᴅ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ ʀᴇᴇʟ")


# Command-based handlers
@app.on_message(filters.command(["ig", "instagram", "reel"]))
async def insta_command_handler(client, message: Message):
    if len(message.command) < 2:
        await message.reply_text(
            "Pʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴛʜᴇ Iɴsᴛᴀɢʀᴀᴍ ʀᴇᴇʟ URL ᴀғᴛᴇʀ ᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅ"
        )
        return
    url = message.text.split()[1]
    if not re.match(
        re.compile(r"^(https?://)?(www\.)?(instagram\.com|instagr\.am)/.*$"), url
    ):
        return await message.reply_text(
            "Tʜᴇ ᴘʀᴏᴠɪᴅᴇᴅ URL ɪs ɴᴏᴛ ᴀ ᴠᴀʟɪᴅ Iɴsᴛᴀɢʀᴀᴍ URL😅😅"
        )
    await send_instagram_media(message, url)


# Auto-detect Instagram URLs in any message
@app.on_message(filters.regex(r"(https?://(?:www\.)?(?:instagram\.com|instagr\.am)/\S+)"))
async def insta_auto_handler(client, message: Message):
    match = re.search(r"(https?://(?:www\.)?(?:instagram\.com|instagr\.am)/\S+)", message.text)
    if match:
        url = match.group(1)
        await send_instagram_media(message, url)


MODULE = "Rᴇᴇʟ"
HELP = """
ɪɴsᴛᴀɢʀᴀᴍ ʀᴇᴇʟ ᴅᴏᴡɴʟᴏᴀᴅᴇʀ:

• /ig [URL]: ᴅᴏᴡɴʟᴏᴀᴅ ɪɴsᴛᴀɢʀᴀᴍ ʀᴇᴇʟs. Pʀᴏᴠɪᴅᴇ ᴛʜᴇ ɪɴsᴛᴀɢʀᴀᴍ ʀᴇᴇʟ URL ᴀғᴛᴇʀ ᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅ.
• /instagram [URL]: ᴅᴏᴡɴʟᴏᴀᴅ ɪɴsᴛᴀɢʀᴀᴍ ʀᴇᴇʟs.
• /reel [URL]: ᴅᴏᴡɴʟᴏᴀᴅ ɪɴsᴛᴀɢʀᴀᴍ ʀᴇᴇʟs.
• Sending any Instagram link directly: ʙᴏᴛ ᴡɪʟʟ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ᴅᴏᴡɴʟᴏᴀᴅ ɪᴛ.
"""
