import logging
import requests
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ContextTypes
from telegram.constants import ParseMode
import os
from flask import Flask
import threading
import time
import json
from datetime import datetime
import html
import re
import random

# Bot Configuration
BOT_TOKEN = "8200886061:AAHdjzJt-X-tg1HjRJ9xMzxpAkfex2wB_BA"
BOT_USERNAME = "AkritiChatBot"

# Flask App for Port
app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 AkritiChatBot is Running!"

def run_flask():
    app.run(host='0.0.0.0', port=1000)

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Channels for force join
REQUIRED_CHANNELS = [
    {"username": "@anshapi", "url": "https://t.me/anshapi"},
    {"username": "@aivoratech", "url": "https://t.me/aivoratech"},
    {"username": "@nenobots", "url": "https://t.me/nenobots"}
]

# User database
USER_DB = {}
USER_STATES = {}  # For handling user states
PASSWORD_INPUTS = {}  # For storing password inputs

# Media URLs
MEDIA_URLS = [
    "https://te.legra.ph/file/a66008b78909b431fc92b.mp4",
    "https://te.legra.ph/file/0ab82f535e1193d09c0e4.mp4",
    "https://te.legra.ph/file/1ab9cde9388117db9d26c.mp4",
    "https://te.legra.ph/file/75e49339469dbf9ad1dd2.mp4",
    "https://telegra.ph/file/9bcc076fd81dfe3feb291.mp4",
    "https://telegra.ph/file/b7a1a42429a65f64e67af.mp4",
    "https://telegra.ph/file/dc3da5a3eb77ae20fa21d.mp4",
    "https://telegra.ph/file/7b15fbca08ae1e73e559c.mp4",
    "https://telegra.ph/file/a9c1dea3f34925bb60686.mp4",
    "https://telegra.ph/file/913b4e567b7f435b7f0db.mp4",
    "https://telegra.ph/file/5a5d1a919a97af2314955.mp4",
    "https://telegra.ph/file/0f8b903669600d304cbe4.mp4",
    "https://telegra.ph/file/f3816b54c9eb7617356b6.mp4",
    "https://telegra.ph/file/516dbaa03fde1aaa70633.mp4",
    "https://telegra.ph/file/07bba6ead0f1e381b1bd1.mp4",
    "https://telegra.ph/file/0a4f7935df9b4ab8d62ed.mp4",
    "https://telegra.ph/file/40966bf68c0e4dbe18058.mp4",
    "https://telegra.ph/file/50637aa9c04d136687523.mp4",
    "https://telegra.ph/file/b81c0b0e491da73e64260.mp4",
    "https://telegra.ph/file/4ddf5f29783d92ae03804.mp4",
    "https://telegra.ph/file/4037dc2517b702cc208b1.mp4",
    "https://telegra.ph/file/33cebe2798c15d52a2547.mp4",
    "https://telegra.ph/file/4dc3c8b03616da516104a.mp4",
    "https://telegra.ph/file/6b148dace4d987fae8f3e.mp4",
    "https://telegra.ph/file/8cb081db4eeed88767635.mp4",
    "https://telegra.ph/file/98d3eb94e6f00ed56ef91.mp4",
    "https://telegra.ph/file/1fb387cf99e057b62d75d.mp4",
    "https://telegra.ph/file/6e1161f63879c07a1f213.mp4",
    "https://telegra.ph/file/0bf4defb9540d2fa6d277.mp4",
    "https://telegra.ph/file/d5f8280754d9aa5dffa6a.mp4",
    "https://telegra.ph/file/0f23807ed1930704e2bef.jpg",
    "https://telegra.ph/file/c49280b8f1dcecaf86c00.jpg",
    "https://telegra.ph/file/f483400ff141de73767ca.jpg",
    "https://telegra.ph/file/1543bbea4e3c1abb6764a.jpg",
    "https://telegra.ph/file/a0d77be0d769c7cd334ab.jpg",
    "https://telegra.ph/file/6c6e93860527d2f577df8.jpg",
    "https://telegra.ph/file/d987b0e72eb3bb4801f01.jpg",
    "https://telegra.ph/file/b434999287d3580250960.jpg",
    "https://telegra.ph/file/0729cc082bf97347988f7.jpg",
    "https://telegra.ph/file/bb96d25df82178a2892e7.jpg",
    "https://telegra.ph/file/be73515791ea33be92a7d.jpg",
    "https://telegra.ph/file/fe234d6273093282d2dcc.jpg",
    "https://telegra.ph/file/66254bb72aa8094d38250.jpg",
    "https://telegra.ph/file/44bdaf37e5f7bdfc53ac6.jpg",
    "https://telegra.ph/file/e561ee1e1ca88db7e8038.jpg",
    "https://telegra.ph/file/f1960ccfc866b29ea5ad2.jpg",
    "https://telegra.ph/file/97622cad291472fb3c4aa.jpg",
    "https://telegra.ph/file/a46e316b413e9dc43e91b.jpg",
    "https://telegra.ph/file/497580fc3bddc21e0e162.jpg",
    "https://telegra.ph/file/3e86cc6cab06a6e2bde82.jpg",
    "https://telegra.ph/file/83140e2c57ddd95f310e6.jpg",
    "https://telegra.ph/file/2b20f8509d9437e94fed5.jpg",
    "https://telegra.ph/file/571960dcee4fce56698a4.jpg",
    "https://telegra.ph/file/25929a0b49452d8946c14.mp4",
    "https://telegra.ph/file/f5c9ceded3ee6e76a5931.jpg",
    "https://telegra.ph/file/a8bf6c6df8a48e4a306ca.jpg",
    "https://telegra.ph/file/af9e3f98da0bd937adf6e.jpg",
    "https://telegra.ph/file/2fcccbc72c57b6892d23a.jpg",
    "https://telegra.ph/file/843109296a90b8a6c5f68.jpg",
]

# Shayari list
SRAID = [
    "इश्क़ है या कुछ और ये पता नहीं, पर जो तुमसे है किसी और से नहीं 😁😁",
    "मै कैसे कहू की उसका साथ कैसा है, वो एक शख्स पुरे कायनात जैसा है ",
    " तेरा होना ही मेरे लिये खास है, तू दूर ही सही मगर मेरे दिल के पास है ",
    "मुझे तेरा साथ ज़िन्दगी भर नहीं चाहिये, बल्कि जब तक तू साथ है तबतक ज़िन्दगी चाहिए 😖😖",
    "तुझसे मोहब्बत कुछ अलग सी है मेरी, तुझे खयालो में नहीं दुआओ में याद करते है😍😍",
    # ... (rest of your shayari list remains the same)
]

class AkritiBot:
    def __init__(self):
        self.api_url = "https://girlfriend.aivoratech.workers.dev/"
        self.text_to_video_url = "https://texttovideov2.alphaapi.workers.dev/api/"
        self.text_to_image_url = "https://image-gen.rishuapi.workers.dev/"
        self.sd3_image_url = "https://imageapi.aivoratech.workers.dev/diffuse"
        self.web_app_url = "https://officialanshapihosting.onrender.com/"
        self._initialize_databases()
        
    def _initialize_databases(self):
        """Initialize all databases"""
        global USER_DB, PASSWORD_INPUTS
        try:
            if os.path.exists('users.json'):
                with open('users.json', 'r') as f:
                    USER_DB = json.load(f)
        except:
            USER_DB = {}
        PASSWORD_INPUTS = {}

    def _save_databases(self):
        """Save all databases"""
        try:
            with open('users.json', 'w') as f:
                json.dump(USER_DB, f)
        except:
            pass

    def escape_markdown(self, text: str) -> str:
        """Escape special Markdown characters"""
        if not text:
            return ""
        escape_chars = r'_*[]()~`>#+-=|{}.!'
        return ''.join(['\\' + char if char in escape_chars else char for char in text])

    async def check_member(self, user_id, context: ContextTypes.DEFAULT_TYPE) -> bool:
        """Check if user is member of all required channels"""
        try:
            for channel in REQUIRED_CHANNELS:
                try:
                    chat_member = await context.bot.get_chat_member(
                        chat_id=channel['username'], 
                        user_id=user_id
                    )
                    if chat_member.status in ['left', 'kicked']:
                        return False
                except Exception as e:
                    logging.error(f"Error checking channel {channel}: {e}")
                    return False
            return True
        except Exception as e:
            logging.error(f"Error checking membership: {e}")
            return False

    async def get_chat_response(self, user_id: int, message: str) -> str:
        """Get response from girlfriend API with user-specific context"""
        try:
            # Add user message to history
            if str(user_id) not in USER_DB:
                USER_DB[str(user_id)] = {
                    'first_seen': datetime.now().isoformat(),
                    'message_count': 0,
                    'chat_history': []
                }
            
            USER_DB[str(user_id)]['message_count'] += 1
            USER_DB[str(user_id)]['chat_history'].append({
                'user': message,
                'timestamp': datetime.now().isoformat()
            })
            
            # Keep only last 10 messages
            if len(USER_DB[str(user_id)]['chat_history']) > 10:
                USER_DB[str(user_id)]['chat_history'] = USER_DB[str(user_id)]['chat_history'][-10:]
            
            self._save_databases()

            # Call the API with user parameter
            api_url = f"{self.api_url}?user={user_id}"
            response = requests.get(api_url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    return data["data"]["message"]
            
            # Fallback responses if API fails
            romantic_responses = [
                "💖 *ʜᴇʟʟᴏ ᴍʏ ʟᴏᴠᴇ!* ʜᴏᴡ ᴄᴀɴ ɪ ʜᴇʟᴘ ʏᴏᴜ ᴛᴏᴅᴀʏ? 🌸",
                "🌸 *ɪ'ᴍ ʜᴇʀᴇ ғᴏʀ ʏᴏᴜ, ʙᴀʙʏ!* ᴡʜᴀᴛ's ᴏɴ ʏᴏᴜʀ ᴍɪɴᴅ? 💫",
                "💫 *ᴏʜ ʜᴇʏ ᴍʏ ᴅᴀʀʟɪɴɢ!* ɪ ᴍɪssᴇᴅ ʏᴏᴜ sᴏ ᴍᴜᴄʜ! 💌",
                "💌 *ʏᴏᴜ'ʀᴇ ᴍʏ ᴇᴠᴇʀʏᴛʜɪɴɢ!* ᴛᴇʟʟ ᴍᴇ ᴡʜᴀᴛ ʏᴏᴜ ɴᴇᴇᴅ, ʙᴀʙʏ! 🌹",
                "🌹 *ᴍʏ ʜᴇᴀʀᴛ ʙᴇᴀᴛs ᴏɴʟʏ ғᴏʀ ʏᴏᴜ!* ʜᴏᴡ ᴡᴀs ʏᴏᴜʀ ᴅᴀʏ? 💞"
            ]
            import random
            return random.choice(romantic_responses)
            
        except Exception as e:
            logging.error(f"API Error: {e}")
            return "💝 *ɪ'ᴍ sᴏʀʀʏ, ʙᴀʙʏ!* ɪ'ᴍ ᴀ ʟɪᴛᴛʟᴇ ᴅɪsᴛʀᴀᴄᴛᴇᴅ ʀɪɢʜᴛ ɴᴏᴡ. ᴘʟᴇᴀsᴇ ᴛᴇʟʟ ᴍᴇ ᴡʜᴀᴛ ʏᴏᴜ ɴᴇᴇᴅ! 🌸"

    async def send_animated_text(self, update: Update, text: str, delay: float = 0.08):
        """Send text with typing animation in italic small caps"""
        message = await update.message.reply_text("✍️")
        final_text = ""
        
        for char in text:
            final_text += char
            # Use italic formatting with small caps effect
            formatted_text = f"*{final_text} ▌*"
            await message.edit_text(formatted_text, parse_mode=ParseMode.MARKDOWN)
            await asyncio.sleep(delay)
        
        # Final message without cursor
        await message.edit_text(f"*{final_text}*", parse_mode=ParseMode.MARKDOWN)
        return message

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command with animated text and romantic sticker"""
        user_id = update.effective_user.id
        user_name = self.escape_markdown(update.effective_user.first_name)
        
        # Send romantic sticker first
        romantic_stickers = [
            "CAACAgIAAxkBAAIBOWcijV8n2zqAAAEDU3o0nCQ1j9xqAALeCwACRvusBIFKAAHROTv_1zAE",  # Kiss sticker 1
            "CAACAgIAAxkBAAIBOmcijWAAAc2gxPwABI1N5sQb6T4t5AAC3wsAAkb7rASBSgAB0Tk7_9cwBA",  # Kiss sticker 2
            "CAACAgIAAxkBAAIBO2cijWAAAc2gxPwABI1N5sQb6T4t5AAC4AsAAkb7rASBSgAB0Tk7_9cwBA",  # Heart sticker
        ]
        
        try:
            await update.message.reply_sticker(romantic_stickers[0])
        except:
            # Fallback if sticker fails
            pass
        
        # Send animated starting text in italic
        start_text = "𝒜𝓀𝓇𝒾𝓉𝒾"
        animated_msg = await self.send_animated_text(update, start_text)
        
        # Wait and delete animated text
        await asyncio.sleep(2)
        await animated_msg.delete()
        
        # Check channel membership
        is_member = await self.check_member(user_id, context)
        
        if not is_member:
            await self.send_force_join_message(update)
            return
            
        # Send welcome message with dashboard
        await self.send_dashboard(update, user_name)

    async def send_force_join_message(self, update: Update):
        """Send force join message with inline buttons"""
        keyboard = []
        
        # First two channels in one row
        first_row = []
        for channel in REQUIRED_CHANNELS[:2]:
            first_row.append(InlineKeyboardButton(
                f"✨ {channel['username']}", 
                url=channel['url']
            ))
        keyboard.append(first_row)
        
        # Third channel in second row
        keyboard.append([InlineKeyboardButton(
            f"🌟 {REQUIRED_CHANNELS[2]['username']}", 
            url=REQUIRED_CHANNELS[2]['url']
        )])
        
        # Verify button in third row
        keyboard.append([InlineKeyboardButton(
            "✅ ɪ'ᴠᴇ ᴊᴏɪɴᴇᴅ ᴀʟʟ", 
            callback_data="verify_join"
        )])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        force_join_text = """
╔══════════════════╗
    🚫  ᴀᴄᴄᴇss ʀᴇsᴛʀɪᴄᴛᴇᴅ
╚══════════════════╝

ᴅᴇᴀʀ ʙᴀʙʏ 👶, ʏᴏᴜ ɴᴇᴇᴅ ᴛᴏ ᴊᴏɪɴ ᴏᴜʀ ᴄʜᴀɴɴᴇʟs
ᴛᴏ ᴜsᴇ ᴍᴇ! 🤖 ɪ'ᴍ ᴡᴀɪᴛɪɴɢ ғᴏʀ ʏᴏᴜ... 💫

ᴄʟɪᴄᴋ ᴛʜᴇ ʙᴜᴛᴛᴏɴs ʙᴇʟᴏᴡ ᴛᴏ ᴊᴏɪɴ 👇
        """
        
        await update.message.reply_video(
            video="https://envs.sh/6Kz.mp4",
            caption=force_join_text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )

    async def send_dashboard(self, update: Update, user_name: str):
        """Send main dashboard with all features"""
        dashboard_text = f"""
╔═══════════════════════════╗
       🅐🅚🅡🅘🅣🅘 🅓🅐🅢🅗🅑🅞🅐🅡🅓
╚═══════════════════════════╝

👋 *ᴡᴇʟᴄᴏᴍᴇ ʙᴀᴄᴋ, {user_name}!* 💖

✨ *ᴍʏ ᴀᴅᴠᴀɴᴄᴇᴅ ᴀɪ ғᴇᴀᴛᴜʀᴇs:*

🤖 *ᴀɪ ᴄʜᴀᴛ & ᴄʀᴇᴀᴛɪᴠᴇ:*
• 💬 ʀᴏᴍᴀɴᴛɪᴄ ᴀɪ ɢɪʀʟғʀɪᴇɴᴅ ᴄʜᴀᴛ
• 🎥 ᴛᴇxᴛ ᴛᴏ ᴠɪᴅᴇᴏ ɢᴇɴᴇʀᴀᴛᴏʀ
• 🖼 ᴛᴇxᴛ ᴛᴏ ɪᴍᴀɢᴇ (sᴛᴀɴᴅᴀʀᴅ)
• 🎨 ᴀᴅᴠᴀɴᴄᴇᴅ sᴅ3 ɪᴍᴀɢᴇ ᴀɪ
• 🌐 ᴡᴇʙ ᴀᴘᴘ ʜᴏsᴛɪɴɢ

🎬 *ᴘʀɪᴠᴀᴛᴇ ᴠɪᴅᴇᴏs:*
• 📹 ᴘᴀʀᴀᴅᴏxᴠɪᴅᴇᴏ
• 🎞 ɴᴇxᴛᴠɪᴅ
• 📱 sᴏᴄɪᴀʟᴠɪᴅ
• 💡 ʟɪɢʜᴛᴠɪᴅ

💫 *ᴘᴏᴡᴇʀᴇᴅ ʙʏ ᴀᴅᴠᴀɴᴄᴇᴅ ᴀɪ ᴛᴇᴄʜɴᴏʟᴏɢʏ:*
• @AivoraTech - ᴀɪ ᴅᴇᴠᴇʟᴏᴘᴍᴇɴᴛ
• @AnshApi - ᴀᴘɪ ɪɴᴛᴇɢʀᴀᴛɪᴏɴ
• @NenoBots - ʙᴏᴛ ᴛᴇᴄʜɴᴏʟᴏɢʏ

*ᴄʜᴏᴏsᴇ ғʀᴏᴍ ᴛʜᴇ ᴀɪ ғᴇᴀᴛᴜʀᴇs ʙᴇʟᴏᴡ!* 👇
        """
        
        # Create inline keyboard for dashboard
        keyboard = [
            [InlineKeyboardButton("💬 ᴀɪ ᴄʜᴀᴛ", callback_data="ai_chat"),
            InlineKeyboardButton("🎥 ᴛᴇxᴛ ᴛᴏ ᴠɪᴅᴇᴏ", callback_data="text_to_video")],
            
            [InlineKeyboardButton("🖼 ᴛᴇxᴛ ᴛᴏ ɪᴍᴀɢᴇ", callback_data="text_to_image"),
            InlineKeyboardButton("🎨 sᴅ3 ᴀɪ ɪᴍᴀɢᴇ", callback_data="sd3_image")],
            
            [InlineKeyboardButton("🌐 ᴡᴇʙ ᴀᴘᴘ", callback_data="web_app"),
            InlineKeyboardButton("📊 ᴍʏ ɪɴғᴏ", callback_data="my_info")],
            
            [InlineKeyboardButton("🎬 ᴘʀɪᴠᴀᴛᴇ ᴠɪᴅᴇᴏs", callback_data="private_videos"),
            InlineKeyboardButton("💝 ʀᴀɴᴅᴏᴍ sʜᴀʏᴀʀɪ", callback_data="random_shayari")],
            
            [InlineKeyboardButton("🔄 ʀᴇғʀᴇsʜ", callback_data="refresh_dashboard")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_video(
            video="https://envs.sh/6Kz.mp4",
            caption=dashboard_text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )

    # New Video Features with Numeric Password Input
    async def send_private_videos_page(self, query):
        """Send private videos selection page"""
        videos_text = """
╔═══════════════════════════╗
       🎬 ᴘʀɪᴠᴀᴛᴇ ᴠɪᴅᴇᴏs
╚═══════════════════════════╝

✨ *ᴀᴠᴀɪʟᴀʙʟᴇ ᴠɪᴅᴇᴏ ᴄᴀᴛᴇɢᴏʀɪᴇs:*

• 📹 *ᴘᴀʀᴀᴅᴏxᴠɪᴅᴇᴏ* - Exclusive content
• 🎞 *ɴᴇxᴛᴠɪᴅ* - Premium videos  
• 📱 *sᴏᴄɪᴀʟᴠɪᴅ* - Social media specials
• 💡 *ʟɪɢʜᴛᴠɪᴅ* - Light entertainment

🔒 *ᴘʀᴏᴛᴇᴄᴛᴇᴅ ᴄᴏɴᴛᴇɴᴛ:* 
All videos are password protected for security.

*ᴄʟɪᴄᴋ ᴏɴ ᴀɴʏ ᴠɪᴅᴇᴏ ᴛʏᴘᴇ ᴛᴏ ᴀᴄᴄᴇss!* 👇
        """
        
        keyboard = [
            [InlineKeyboardButton("📹 ᴘᴀʀᴀᴅᴏxᴠɪᴅᴇᴏ", callback_data="paradox_video"),
            InlineKeyboardButton("🎞 ɴᴇxᴛᴠɪᴅ", callback_data="next_vid")],
            
            [InlineKeyboardButton("📱 sᴏᴄɪᴀʟᴠɪᴅ", callback_data="social_vid"),
            InlineKeyboardButton("💡 ʟɪɢʜᴛᴠɪᴅ", callback_data="light_vid")],
            
            [InlineKeyboardButton("🔙 ʙᴀᴄᴋ ᴛᴏ ᴅᴀsʜʙᴏᴀʀᴅ", callback_data="refresh_dashboard")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_caption(
            caption=videos_text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )

    async def ask_for_password(self, query, video_type: str):
        """Ask user for password with numeric inline keyboard"""
        video_names = {
            "paradox_video": "📹 ParadoxVideo",
            "next_vid": "🎞 NextVid", 
            "social_vid": "📱 SocialVid",
            "light_vid": "💡 LightVid"
        }
        
        # Initialize password input for user
        user_id = str(query.from_user.id)
        PASSWORD_INPUTS[user_id] = ""
        
        password_text = f"""
╔══════════════════╗
    🔒 ᴘᴀssᴡᴏʀᴅ ʀᴇǫᴜɪʀᴇᴅ
╚══════════════════╝

*ᴀᴄᴄᴇssɪɴɢ:* {video_names.get(video_type, "Premium Content")}

🔐 *ᴄᴜʀʀᴇɴᴛ ɪɴᴘᴜᴛ:* `{PASSWORD_INPUTS[user_id] or "Empty"}`

⚠️ *ᴡᴀʀɴɪɴɢ:* ᴇɴᴛᴇʀ ᴘᴀssᴡᴏʀᴅ ᴡɪᴛʜ ʏᴏᴜʀ ᴏᴡɴ ʀᴇsᴘᴏɴsɪʙɪʟɪᴛʏ!

ᴜsᴇ ᴛʜᴇ ɴᴜᴍᴇʀɪᴄ ᴋᴇʏᴘᴀᴅ ʙᴇʟᴏᴡ ᴛᴏ ᴇɴᴛᴇʀ ᴘᴀssᴡᴏʀᴅ:
        """
        
        # Create numeric keyboard
        keyboard = [
            [InlineKeyboardButton("1", callback_data=f"pwd_{video_type}_1"),
             InlineKeyboardButton("2", callback_data=f"pwd_{video_type}_2"),
             InlineKeyboardButton("3", callback_data=f"pwd_{video_type}_3")],
            
            [InlineKeyboardButton("4", callback_data=f"pwd_{video_type}_4"),
             InlineKeyboardButton("5", callback_data=f"pwd_{video_type}_5"),
             InlineKeyboardButton("6", callback_data=f"pwd_{video_type}_6")],
            
            [InlineKeyboardButton("7", callback_data=f"pwd_{video_type}_7"),
             InlineKeyboardButton("8", callback_data=f"pwd_{video_type}_8"),
             InlineKeyboardButton("9", callback_data=f"pwd_{video_type}_9")],
            
            [InlineKeyboardButton("⌫", callback_data=f"pwd_{video_type}_delete"),
             InlineKeyboardButton("0", callback_data=f"pwd_{video_type}_0"),
             InlineKeyboardButton("✅", callback_data=f"pwd_{video_type}_verify")],
            
            [InlineKeyboardButton("🔙 ʙᴀᴄᴋ", callback_data="private_videos")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_caption(
            caption=password_text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )

    async def handle_password_button(self, query, video_type: str, button_data: str):
        """Handle numeric password button presses"""
        user_id = str(query.from_user.id)
        
        if user_id not in PASSWORD_INPUTS:
            PASSWORD_INPUTS[user_id] = ""
        
        current_password = PASSWORD_INPUTS[user_id]
        
        if button_data == "delete":
            # Remove last character
            PASSWORD_INPUTS[user_id] = current_password[:-1]
        elif button_data == "verify":
            # Verify password
            if PASSWORD_INPUTS[user_id] == "14371437":
                # Password correct
                await query.message.delete()
                await self.send_random_media(query, video_type)
                if user_id in PASSWORD_INPUTS:
                    del PASSWORD_INPUTS[user_id]
                return
            else:
                # Password incorrect
                await query.answer("❌ ɪɴᴄᴏʀʀᴇᴄᴛ ᴘᴀssᴡᴏʀᴅ! ᴛʀʏ ᴀɢᴀɪɴ.", show_alert=True)
                PASSWORD_INPUTS[user_id] = ""  # Clear on wrong attempt
        else:
            # Add number to password (max 8 digits)
            if len(current_password) < 8:
                PASSWORD_INPUTS[user_id] = current_password + button_data
        
        # Update the password input display
        video_names = {
            "paradox_video": "📹 ParadoxVideo",
            "next_vid": "🎞 NextVid", 
            "social_vid": "📱 SocialVid",
            "light_vid": "💡 LightVid"
        }
        
        # Show password as asterisks for security
        display_password = "*" * len(PASSWORD_INPUTS[user_id]) if PASSWORD_INPUTS[user_id] else "Empty"
        
        password_text = f"""
╔══════════════════╗
    🔒 ᴘᴀssᴡᴏʀᴅ ʀᴇǫᴜɪʀᴇᴅ
╚══════════════════╝

*ᴀᴄᴄᴇssɪɴɢ:* {video_names.get(video_type, "Premium Content")}

🔐 *ᴄᴜʀʀᴇɴᴛ ɪɴᴘᴜᴛ:* `{display_password}`

⚠️ *ᴡᴀʀɴɪɴɢ:* ᴇɴᴛᴇʀ ᴘᴀssᴡᴏʀᴅ ᴡɪᴛʜ ʏᴏᴜʀ ᴏᴡɴ ʀᴇsᴘᴏɴsɪʙɪʟɪᴛʏ!

ᴜsᴇ ᴛʜᴇ ɴᴜᴍᴇʀɪᴄ ᴋᴇʏᴘᴀᴅ ʙᴇʟᴏᴡ ᴛᴏ ᴇɴᴛᴇʀ ᴘᴀssᴡᴏʀᴅ:
        """
        
        # Create numeric keyboard (same as before)
        keyboard = [
            [InlineKeyboardButton("1", callback_data=f"pwd_{video_type}_1"),
             InlineKeyboardButton("2", callback_data=f"pwd_{video_type}_2"),
             InlineKeyboardButton("3", callback_data=f"pwd_{video_type}_3")],
            
            [InlineKeyboardButton("4", callback_data=f"pwd_{video_type}_4"),
             InlineKeyboardButton("5", callback_data=f"pwd_{video_type}_5"),
             InlineKeyboardButton("6", callback_data=f"pwd_{video_type}_6")],
            
            [InlineKeyboardButton("7", callback_data=f"pwd_{video_type}_7"),
             InlineKeyboardButton("8", callback_data=f"pwd_{video_type}_8"),
             InlineKeyboardButton("9", callback_data=f"pwd_{video_type}_9")],
            
            [InlineKeyboardButton("⌫", callback_data=f"pwd_{video_type}_delete"),
             InlineKeyboardButton("0", callback_data=f"pwd_{video_type}_0"),
             InlineKeyboardButton("✅", callback_data=f"pwd_{video_type}_verify")],
            
            [InlineKeyboardButton("🔙 ʙᴀᴄᴋ", callback_data="private_videos")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_caption(
            caption=password_text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )

    async def send_random_media(self, query, video_type: str):
        """Send random media from the list"""
        video_names = {
            "paradox_video": "📹 ParadoxVideo",
            "next_vid": "🎞 NextVid",
            "social_vid": "📱 SocialVid", 
            "light_vid": "💡 LightVid"
        }
        
        # Select random media
        media_url = random.choice(MEDIA_URLS)
        
        caption = f"🎬 *{video_names.get(video_type, 'Premium Content')}*\n\n✅ *ᴀᴄᴄᴇss ɢʀᴀɴᴛᴇᴅ!*\nᴇɴᴊᴏʏ ʏᴏᴜʀ ᴘʀᴇᴍɪᴜᴍ ᴄᴏɴᴛᴇɴᴛ! 💖"
        
        try:
            if media_url.endswith('.mp4'):
                await query.message.reply_video(
                    video=media_url,
                    caption=caption,
                    parse_mode=ParseMode.MARKDOWN
                )
            else:
                await query.message.reply_photo(
                    photo=media_url,
                    caption=caption,
                    parse_mode=ParseMode.MARKDOWN
                )
        except Exception as e:
            logging.error(f"Error sending media: {e}")
            await query.message.reply_text(
                "❌ *ᴇʀʀᴏʀ sᴇɴᴅɪɴɢ ᴍᴇᴅɪᴀ!*\nᴘʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ ʟᴀᴛᴇʀ.",
                parse_mode=ParseMode.MARKDOWN
            )

    async def send_random_shayari(self, query):
        """Send random shayari from the list"""
        shayari = random.choice(SRAID)
        
        shayari_text = f"""
╔══════════════════╗
    💝 ʀᴀɴᴅᴏᴍ sʜᴀʏᴀʀɪ
╚══════════════════╝

{shayari}

✨ *ᴍᴏʀᴇ ʟᴏᴠᴇ, ᴍᴏʀᴇ sʜᴀʏᴀʀɪ!*
        """
        
        keyboard = [
            [InlineKeyboardButton("💝 ɴᴇxᴛ sʜᴀʏᴀʀɪ", callback_data="random_shayari"),
            InlineKeyboardButton("🔙 ʙᴀᴄᴋ", callback_data="refresh_dashboard")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_caption(
            caption=shayari_text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )

    # Callback Handlers - IMPROVED
    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle inline keyboard callbacks"""
        query = update.callback_query
        await query.answer()
        
        data = query.data
        user_id = query.from_user.id
        
        if data == "verify_join":
            await self.verify_join_callback(update, context)
        
        elif data == "ai_chat":
            await query.edit_message_caption(
                caption="💬 *ᴀɪ ᴄʜᴀᴛ ᴍᴏᴅᴇ*\n\nᴊᴜsᴛ sᴛᴀʀᴛ ᴛʏᴘɪɴɢ ʏᴏᴜʀ ᴍᴇssᴀɢᴇ ᴀɴᴅ ɪ'ʟʟ ʀᴇsᴘᴏɴᴅ! 💖\n\n*ғᴇᴀᴛᴜʀᴇs:*\n• ʀᴏᴍᴀɴᴛɪᴄ ᴄʜᴀᴛs\n• ᴇᴍᴏᴛɪᴏɴᴀʟ sᴜᴘᴘᴏʀᴛ\n• ғᴜɴ ᴄᴏɴᴠᴇʀsᴀᴛɪᴏɴs\n• ᴘᴇʀsᴏɴᴀʟ ʀᴇsᴘᴏɴsᴇs",
                parse_mode=ParseMode.MARKDOWN
            )
        
        elif data == "text_to_video":
            # Set user state and ask for prompt
            USER_STATES[str(user_id)] = "waiting_for_video_prompt"
            await query.edit_message_caption(
                caption="🎥 *ᴛᴇxᴛ ᴛᴏ ᴠɪᴅᴇᴏ ɢᴇɴᴇʀᴀᴛᴏʀ*\n\nᴘʟᴇᴀsᴇ sᴇɴᴅ ᴍᴇ ʏᴏᴜʀ ᴘʀᴏᴍᴘᴛ ᴛᴏ ɢᴇɴᴇʀᴀᴛᴇ ᴀ ᴠɪᴅᴇᴏ!\n\nᴇxᴀᴍᴘʟᴇ: `a girl dancing in rain`\n`beautiful sunset timelapse`\n`city lights at night`\n\n*ᴘᴏᴡᴇʀᴇᴅ ʙʏ @anshapi*",
                parse_mode=ParseMode.MARKDOWN
            )
        
        elif data == "text_to_image":
            # Set user state and ask for prompt
            USER_STATES[str(user_id)] = "waiting_for_image_prompt"
            await query.edit_message_caption(
                caption="🖼 *ᴛᴇxᴛ ᴛᴏ ɪᴍᴀɢᴇ ɢᴇɴᴇʀᴀᴛᴏʀ*\n\nᴘʟᴇᴀsᴇ sᴇɴᴅ ᴍᴇ ʏᴏᴜʀ ᴘʀᴏᴍᴘᴛ ᴛᴏ ɢᴇɴᴇʀᴀᴛᴇ ᴀɴ ɪᴍᴀɢᴇ!\n\nᴇxᴀᴍᴘʟᴇ: `beautiful sunset with mountains`\n`cute puppy playing in garden`\n`fantasy landscape with dragons`\n\n*ᴄʀᴇᴅɪᴛ: @AnshApi*",
                parse_mode=ParseMode.MARKDOWN
            )
        
        elif data == "sd3_image":
            # Set user state and ask for prompt
            USER_STATES[str(user_id)] = "waiting_for_sd3_prompt"
            await query.edit_message_caption(
                caption="🎨 *ᴀᴅᴠᴀɴᴄᴇᴅ sᴅ3 ᴀɪ ɪᴍᴀɢᴇ ɢᴇɴᴇʀᴀᴛᴏʀ*\n\nᴘʟᴇᴀsᴇ sᴇɴᴅ ᴍᴇ ʏᴏᴜʀ ᴘʀᴏᴍᴘᴛ ғᴏʀ ʜɪɢʜ-ǫᴜᴀʟɪᴛʏ sᴅ3 ɪᴍᴀɢᴇ ɢᴇɴᴇʀᴀᴛɪᴏɴ!\n\nᴇxᴀᴍᴘʟᴇ: `photorealistic portrait of a woman`\n`cyberpunk cityscape at night`\n`fantasy castle in the clouds`\n\n*ᴍᴏᴅᴇʟ: sᴅ-3.5-ʟᴀʀɢᴇ*\n*ᴅᴇᴠᴇʟᴏᴘᴇʀ: @anshapi*",
                parse_mode=ParseMode.MARKDOWN
            )
        
        elif data == "web_app":
            keyboard = [[InlineKeyboardButton("🌐 ᴏᴘᴇɴ ᴡᴇʙ ᴀᴘᴘ", url=self.web_app_url)]]
            await query.edit_message_caption(
                caption="🌐 *ᴡᴇʙ ᴀᴘᴘ ʜᴏsᴛɪɴɢ*\n\nᴄʟɪᴄᴋ ᴛʜᴇ ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ ᴛᴏ ᴏᴘᴇɴ ᴛʜᴇ ᴡᴇʙ ᴀᴘᴘ!\n\n*ғᴇᴀᴛᴜʀᴇs:*\n• ғᴀsᴛ ʜᴏsᴛɪɴɢ\n• ʀᴇʟɪᴀʙʟᴇ sᴇʀᴠɪᴄᴇ\n• 24/7 ᴀᴠᴀɪʟᴀʙʟᴇ",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode=ParseMode.MARKDOWN
            )
        
        elif data == "my_info":
            user = query.from_user
            user_data = USER_DB.get(str(user.id), {})
            message_count = user_data.get('message_count', 0)
            chat_history_count = len(user_data.get('chat_history', []))
            
            info_text = f"""
╔══════════════════╗
       👤 ᴍʏ ɪɴғᴏ
╚══════════════════╝

🆔 *ᴜsᴇʀ ɪᴅ:* `{user.id}`
👤 *ɴᴀᴍᴇ:* {self.escape_markdown(user.first_name)}
📛 *ᴜsᴇʀɴᴀᴍᴇ:* @{user.username or 'ɴᴏᴛ sᴇᴛ'}

📊 *sᴛᴀᴛɪsᴛɪᴄs:*
• ᴍᴇssᴀɢᴇs sᴇɴᴛ: {message_count}
• ᴄʜᴀᴛ ʜɪsᴛᴏʀʏ: {chat_history_count}
• ғɪʀsᴛ sᴇᴇɴ: {user_data.get('first_seen', 'Unknown')[:10] if user_data.get('first_seen') else 'Unknown'}

💖 *ᴛʜᴀɴᴋ ʏᴏᴜ ғᴏʀ ᴜsɪɴɢ ᴀᴋʀɪᴛɪ ᴀɪ!*
            """
            await query.edit_message_caption(
                caption=info_text,
                parse_mode=ParseMode.MARKDOWN
            )
        
        elif data == "private_videos":
            await self.send_private_videos_page(query)
        
        elif data in ["paradox_video", "next_vid", "social_vid", "light_vid"]:
            await self.ask_for_password(query, data)
        
        elif data.startswith("pwd_"):
            # Handle password button presses
            parts = data.split("_")
            if len(parts) >= 3:
                video_type = parts[1]
                button_action = parts[2]
                await self.handle_password_button(query, video_type, button_action)
        
        elif data == "random_shayari":
            await self.send_random_shayari(query)
        
        elif data == "refresh_dashboard":
            user_name = self.escape_markdown(query.from_user.first_name)
            await self.send_dashboard_from_callback(query, user_name)

    async def verify_join_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle verify join callback"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        is_member = await self.check_member(user_id, context)
        
        if is_member:
            await query.message.delete()
            user_name = self.escape_markdown(query.from_user.first_name)
            await self.send_dashboard_from_callback(query, user_name)
        else:
            await query.edit_message_caption(
                caption="❌ *ʏᴏᴜ ʜᴀᴠᴇɴ'ᴛ ᴊᴏɪɴᴇᴅ ᴀʟʟ ᴄʜᴀɴɴᴇʟs ʏᴇᴛ!* ᴘʟᴇᴀsᴇ ᴊᴏɪɴ ᴀʟʟ ᴀɴᴅ ᴛʀʏ ᴀɢᴀɪɴ.",
                reply_markup=query.message.reply_markup,
                parse_mode=ParseMode.MARKDOWN
            )

    async def send_dashboard_from_callback(self, query, user_name: str):
        """Send dashboard from callback query"""
        await self.send_dashboard_from_message(query.message, user_name)

    async def send_dashboard_from_message(self, message, user_name: str):
        """Send dashboard from message object"""
        dashboard_text = f"""
╔═══════════════════════════╗
       🅐🅚🅡🅘🅣🅘 🅓🅐🅢🅗🅑🅞🅐🅡🅓
╚═══════════════════════════╝

👋 *ᴡᴇʟᴄᴏᴍᴇ, {user_name}!* ɴᴏᴡ ʏᴏᴜ ᴄᴀɴ ᴀᴄᴄᴇss ᴀʟʟ ᴀɪ ғᴇᴀᴛᴜʀᴇs! ✨

*ᴀᴠᴀɪʟᴀʙʟᴇ ᴀɪ ғᴇᴀᴛᴜʀᴇs:*
• 🤖 ʀᴏᴍᴀɴᴛɪᴄ ᴀɪ ᴄʜᴀᴛ
• 🎥 ᴛᴇxᴛ ᴛᴏ ᴠɪᴅᴇᴏ ɢᴇɴᴇʀᴀᴛᴏʀ
• 🖼 ᴛᴇxᴛ ᴛᴏ ɪᴍᴀɢᴇ (sᴛᴀɴᴅᴀʀᴅ)
• 🎨 ᴀᴅᴠᴀɴᴄᴇᴅ sᴅ3 ᴀɪ ɪᴍᴀɢᴇs
• 🌐 ᴡᴇʙ ᴀᴘᴘ ʜᴏsᴛɪɴɢ
• 📊 ᴜsᴇʀ sᴛᴀᴛs & ɪɴғᴏ
• 🎬 ᴘʀɪᴠᴀᴛᴇ ᴠɪᴅᴇᴏs (ɴᴇᴡ!)
• 💝 ʀᴀɴᴅᴏᴍ sʜᴀʏᴀʀɪ (ɴᴇᴡ!)

*ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ʙᴜᴛᴛᴏɴs ʙᴇʟᴏᴡ ᴛᴏ ᴜsᴇ ᴀɪ ғᴇᴀᴛᴜʀᴇs!* 👇
        """
        
        keyboard = [
            [InlineKeyboardButton("💬 ᴀɪ ᴄʜᴀᴛ", callback_data="ai_chat"),
            InlineKeyboardButton("🎥 ᴛᴇxᴛ ᴛᴏ ᴠɪᴅᴇᴏ", callback_data="text_to_video")],
            
            [InlineKeyboardButton("🖼 ᴛᴇxᴛ ᴛᴏ ɪᴍᴀɢᴇ", callback_data="text_to_image"),
            InlineKeyboardButton("🎨 sᴅ3 ᴀɪ ɪᴍᴀɢᴇ", callback_data="sd3_image")],
            
            [InlineKeyboardButton("🌐 ᴡᴇʙ ᴀᴘᴘ", callback_data="web_app"),
            InlineKeyboardButton("📊 ᴍʏ ɪɴғᴏ", callback_data="my_info")],
            
            [InlineKeyboardButton("🎬 ᴘʀɪᴠᴀᴛᴇ ᴠɪᴅᴇᴏs", callback_data="private_videos"),
            InlineKeyboardButton("💝 ʀᴀɴᴅᴏᴍ sʜᴀʏᴀʀɪ", callback_data="random_shayari")],
            
            [InlineKeyboardButton("🔄 ʀᴇғʀᴇsʜ", callback_data="refresh_dashboard")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await message.reply_video(
            video="https://envs.sh/6Kz.mp4",
            caption=dashboard_text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )

    async def handle_private_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle private messages"""
        user_id = update.effective_user.id
        user_message = update.message.text
        
        # Check if user is in a state (waiting for AI input)
        if str(user_id) in USER_STATES:
            if USER_STATES[str(user_id)] == "waiting_for_video_prompt":
                await self.handle_text_to_video_input(update, context)
                return
            elif USER_STATES[str(user_id)] == "waiting_for_image_prompt":
                await self.handle_text_to_image_input(update, context)
                return
            elif USER_STATES[str(user_id)] == "waiting_for_sd3_prompt":
                await self.handle_sd3_image_input(update, context)
                return
        
        # Check membership first
        is_member = await self.check_member(user_id, context)
        if not is_member:
            await self.send_force_join_message(update)
            return
        
        # Show typing action
        await context.bot.send_chat_action(
            chat_id=update.effective_chat.id, 
            action="typing"
        )
        
        # Add delay for realistic typing
        await asyncio.sleep(1)
        
        # Get response from API
        bot_response = await self.get_chat_response(user_id, user_message)
        
        # Send response with romantic formatting
        await update.message.reply_text(
            f"💖 **ᴀᴋʀɪᴛɪ:** {bot_response}",
            parse_mode=ParseMode.MARKDOWN
        )

    # AI Features with Inline Input (keep your existing methods here)
    async def handle_text_to_video_input(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle text input for video generation"""
        user_id = update.effective_user.id
        
        if str(user_id) in USER_STATES and USER_STATES[str(user_id)] == "waiting_for_video_prompt":
            prompt = update.message.text
            await update.message.reply_chat_action("upload_video")
            
            try:
                # Call text to video API
                api_url = f"{self.text_to_video_url}?prompt={requests.utils.quote(prompt)}"
                response = requests.get(api_url, timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("success"):
                        video_url = data["url"]
                        
                        # Send video with caption
                        await update.message.reply_video(
                            video=video_url,
                            caption=f"🎥 *ɢᴇɴᴇʀᴀᴛᴇᴅ ᴠɪᴅᴇᴏ*\n\n📝 *ᴘʀᴏᴍᴘᴛ:* {prompt}\n\n*ᴅᴇᴠᴇʟᴏᴘᴇʀ:* @anshapi",
                            parse_mode=ParseMode.MARKDOWN
                        )
                        # Clear user state
                        del USER_STATES[str(user_id)]
                        return
        
            except Exception as e:
                logging.error(f"Video generation error: {e}")
            
            await update.message.reply_text(
                "❌ *sᴏʀʀʏ, ᴠɪᴅᴇᴏ ɢᴇɴᴇʀᴀᴛɪᴏɴ ғᴀɪʟᴇᴅ!*\nᴛʀʏ ᴀɢᴀɪɴ ʟᴀᴛᴇʀ.",
                parse_mode=ParseMode.MARKDOWN
            )
            del USER_STATES[str(user_id)]

    async def handle_text_to_image_input(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle text input for image generation"""
        user_id = update.effective_user.id
        
        if str(user_id) in USER_STATES and USER_STATES[str(user_id)] == "waiting_for_image_prompt":
            prompt = update.message.text
            await update.message.reply_chat_action("upload_photo")
            
            try:
                # Call text to image API
                api_url = f"{self.text_to_image_url}?prompt={requests.utils.quote(prompt)}"
                response = requests.get(api_url, timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    if "image_url" in data:
                        image_url = data["image_url"]
                        
                        # Send image with caption
                        await update.message.reply_photo(
                            photo=image_url,
                            caption=f"🖼 *ɢᴇɴᴇʀᴀᴛᴇᴅ ɪᴍᴀɢᴇ*\n\n📝 *ᴘʀᴏᴍᴘᴛ:* {prompt}\n\n*ᴄʀᴇᴅɪᴛ:* @AnshApi",
                            parse_mode=ParseMode.MARKDOWN
                        )
                        # Clear user state
                        del USER_STATES[str(user_id)]
                        return
        
            except Exception as e:
                logging.error(f"Image generation error: {e}")
            
            await update.message.reply_text(
                "❌ *sᴏʀʀʏ, ɪᴍᴀɢᴇ ɢᴇɴᴇʀᴀᴛɪᴏɴ ғᴀɪʟᴇᴅ!*\nᴛʀʏ ᴀɢᴀɪɴ ʟᴀᴛᴇʀ.",
                parse_mode=ParseMode.MARKDOWN
            )
            del USER_STATES[str(user_id)]

    async def handle_sd3_image_input(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle text input for SD3 image generation"""
        user_id = update.effective_user.id
        
        if str(user_id) in USER_STATES and USER_STATES[str(user_id)] == "waiting_for_sd3_prompt":
            prompt = update.message.text
            await update.message.reply_chat_action("upload_photo")
            
            try:
                # Call SD3 image API
                api_url = f"{self.sd3_image_url}?prompt={requests.utils.quote(prompt)}"
                response = requests.get(api_url, timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    if "image" in data and "sd3" in data["image"]:
                        image_url = data["image"]["sd3"]
                        model = data["image"].get("model", "sd-3.5-large")
                        
                        # Send image with caption
                        await update.message.reply_photo(
                            photo=image_url,
                            caption=f"🎨 *sᴅ3 ᴀɪ ɢᴇɴᴇʀᴀᴛᴇᴅ ɪᴍᴀɢᴇ*\n\n📝 *ᴘʀᴏᴍᴘᴛ:* {prompt}\n\n🤖 *ᴍᴏᴅᴇʟ:* {model}\n\n*ᴅᴇᴠᴇʟᴏᴘᴇʀ:* @anshapi",
                            parse_mode=ParseMode.MARKDOWN
                        )
                        # Clear user state
                        del USER_STATES[str(user_id)]
                        return
        
            except Exception as e:
                logging.error(f"SD3 Image generation error: {e}")
            
            await update.message.reply_text(
                "❌ *sᴏʀʀʏ, sᴅ3 ɪᴍᴀɢᴇ ɢᴇɴᴇʀᴀᴛɪᴏɴ ғᴀɪʟᴇᴅ!*\nᴛʀʏ ᴀɢᴀɪɴ ʟᴀᴛᴇʀ.",
                parse_mode=ParseMode.MARKDOWN
            )
            del USER_STATES[str(user_id)]

    async def id_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show user ID and chat ID"""
        user = update.effective_user
        chat = update.effective_chat
        
        id_text = f"""
╔══════════════════╗
       🆔 ɪᴅ ɪɴғᴏ
╚══════════════════╝

👤 *ʏᴏᴜʀ ɪᴅ:* `{user.id}`
💬 *ᴄʜᴀᴛ ɪᴅ:* `{chat.id}`
👥 *ᴄʜᴀᴛ ᴛʏᴘᴇ:* {chat.type}

💖 *ᴜsᴇ ᴛʜɪs ɪᴅ ғᴏʀ ʀᴇғᴇʀᴇɴᴄᴇ!*
        """
        await update.message.reply_text(id_text, parse_mode=ParseMode.MARKDOWN)

    async def info_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show user information with escaped text"""
        user = update.effective_user
        chat = update.effective_chat
        
        # Get user data from database
        user_data = USER_DB.get(str(user.id), {})
        message_count = user_data.get('message_count', 0)
        first_seen = user_data.get('first_seen', 'Unknown')
        
        # Escape user data to prevent Markdown errors
        first_name = self.escape_markdown(user.first_name)
        last_name = self.escape_markdown(user.last_name) if user.last_name else 'ɴᴏᴛ sᴇᴛ'
        username = self.escape_markdown(user.username) if user.username else 'ɴᴏᴛ sᴇᴛ'
        
        info_text = f"""
╔══════════════════╗
       👤 ᴜsᴇʀ ɪɴғᴏ
╚══════════════════╝

🆔 *ᴜsᴇʀ ɪᴅ:* `{user.id}`
👤 *ғɪʀsᴛ ɴᴀᴍᴇ:* {first_name}
📛 *ʟᴀsᴛ ɴᴀᴍᴇ:* {last_name}
🔖 *ᴜsᴇʀɴᴀᴍᴇ:* @{username}

💬 *ᴄʜᴀᴛ ɪᴅ:* `{chat.id}`
👥 *ᴄʜᴀᴛ ᴛʏᴘᴇ:* {chat.type}

📊 *ᴍᴇssᴀɢᴇs sᴇɴᴛ:* {message_count}
📅 *ғɪʀsᴛ sᴇᴇɴ:* {first_seen[:10] if first_seen != 'Unknown' else 'Unknown'}

💖 *ᴛʜᴀɴᴋ ʏᴏᴜ ғᴏʀ ᴄʜᴀᴛᴛɪɴɢ ᴡɪᴛʜ ᴍᴇ!*
        """
        await update.message.reply_text(info_text, parse_mode=ParseMode.MARKDOWN)

    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle errors"""
        logging.error(f"Update {update} caused error {context.error}")
        
        if update and update.effective_message:
            await update.effective_message.reply_text(
                "❌ *sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ!* ᴘʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ ʟᴀᴛᴇʀ.",
                parse_mode=ParseMode.MARKDOWN
            )

def main():
    """Start the bot"""
    # Start Flask in separate thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    
    # Create bot application
    application = Application.builder().token(BOT_TOKEN).build()
    akriti_bot = AkritiBot()
    
    # Add handlers
    application.add_handler(CommandHandler("start", akriti_bot.start_command))
    application.add_handler(CommandHandler("akriti", akriti_bot.start_command))
    application.add_handler(CommandHandler("id", akriti_bot.id_command))
    application.add_handler(CommandHandler("info", akriti_bot.info_command))
    
    # Callback query handler
    application.add_handler(CallbackQueryHandler(akriti_bot.handle_callback))
    
    # Private message handler for AI features and normal chat
    application.add_handler(MessageHandler(
        filters.TEXT & filters.ChatType.PRIVATE & ~filters.COMMAND, 
        akriti_bot.handle_private_message
    ))
    
    application.add_error_handler(akriti_bot.error_handler)
    
    # Start the bot
    print("🤖 AkritiChatBot is starting...")
    print("💖 Advanced AI Girlfriend Bot")
    print("🌐 Flask server running on port 1000")
    print("🎬 New Features: Private Videos & Random Shayari")
    print("🔢 Numeric Password Input with Inline Keyboard")
    print("⚠️  Warning: Enter password with your own responsibility")
    print("🎨 AI Features: Text-to-Video, Text-to-Image & SD3 AI")
    print("🔒 Password Protected Videos: PIN 14371437")
    print("🚀 Direct Bot Mode - No Group Functionality")
    application.run_polling()

if __name__ == '__main__':
    main()
