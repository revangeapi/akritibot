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
    "तू हज़ार बार भी रूठे तो मना लूँगा तुझे",
    "मगर देख मोहब्बत में शामिल कोई दूसरा ना हो😁😁",
    "किस्मत यह मेरा इम्तेहान ले रही है😒😒",
    "तड़प कर यह मुझे दर्द दे रही है😌😌",
    "दिल से कभी भी मैंने उसे दूर नहीं किया😉😉",
    "फिर क्यों बेवफाई का वह इलज़ाम दे रही है😎😎",
    "मरे तो लाखों होंगे तुझ पर😚😚",
    "मैं तो तेरे साथ जीना चाहता हूँ😫😫",
    "वापस लौट आया है हवाओं का रुख मोड़ने वाला😣😣",
    "दिल में फिर उतर रहा है दिल तोड़ने वाला🥺🥺",
    "अपनों के बीच बेगाने हो गए हैं🥰🥰",
    "प्यार के लम्हे अनजाने हो गए हैं😘😘",
    "जहाँ पर फूल खिलते थे कभी😍😍",
    "आज वहां पर वीरान हो गए हैं🥰🥰",
    "जो शख्स तेरे तसव्वुर से हे महक जाये😁😁",
    "सोचो तुम्हारे दीदार में उसका क्या होगा😒😒",
    "मोहब्बत का एहसास तो हम दोनों को हुआ था",
    "फर्क सिर्फ इतना था की उसने किया था और मुझे हुआ था",
    "सांसों की डोर छूटती जा रही है",
    "किस्मत भी हमे दर्द देती जा रही है",
    "मौत की तरफ हैं कदम हमारे",
    "मोहब्बत भी हम से छूटती जा रही है",
    "समझता ही नहीं वो मेरे अलफ़ाज़ की गहराई",
    "मैंने हर लफ्ज़ कह दिया जिसे मोहब्बत कहते है",
    "समंदर न सही पर एक नदी तो होनी चाहिए",
    "तेरे शहर में ज़िन्दगी कही तो होनी चाहिए",
    "नज़रों से देखो तोह आबाद हम हैं",
    "दिल से देखो तोह बर्बाद हम हैं",
    "जीवन का हर लम्हा दर्द से भर गया",
    "फिर कैसे कह दें आज़ाद हम हैं",
    "मुझे नहीं मालूम वो पहली बार कब अच्छा लगा",
    "मगर उसके बाद कभी बुरा भी नहीं",
    "सच्ची मोहब्बत कभी खत्म नहीं होती",
    "वक़्त के साथ खामोश हो जाती है",
    "ज़िन्दगी के सफ़र में आपका सहारा चाहिए",
    "आपके चरणों का बस आसरा चाहिए",
    "हर मुश्किलों का हँसते हुए सामना करेंगे",
    "बस ठाकुर जी आपका एक इशारा चाहिए",
    "जिस दिल में बसा था नाम तेरा हमने वो तोड़ दिया",
    "न होने दिया तुझे बदनाम बस तेरे नाम लेना छोड़ दिया",
    "प्यार वो नहीं जो हासिल करने के लिए कुछ भी करव दे",
    "प्यार वो है जो उसकी खुशी के लिए अपने अरमान चोर दे",
    "आशिक के नाम से सभी जानते हैं😍😍",
    "इतना बदनाम हो गए हम मयखाने में🥰🥰",
    "जब भी तेरी याद आती है बेदर्द मुझे😍😍",
    "तोह पीते हैं हम दर्द पैमाने में🥰🥰",
    "हम इश्क़ के वो मुकाम पर खड़े है😁😁",
    "जहाँ दिल किसी और को चाहे तो गुन्हा लगता है😒😒",
    "सच्चे प्यार वालों को हमेशा लोग गलत ही समझते है👀👀",
    "जबकि टाइम पास वालो से लोग खुश रहते है आज कल🙈🙈",
    "गिलास पर गिलास बहुत टूट रहे हैं😋😋",
    "खुसी के प्याले दर्द से भर रहे हैं🤨🤨",
    "मशालों की तरह दिल जल रहे हैं🤭🤭",
    "जैसे ज़िन्दगी में बदकिस्मती से मिल रहे हैं😌😌",
    "सिर्फ वक़्त गुजरना हो तो किसी और को अपना बना लेना🤫🤫",
    "हम दोस्ती भी करते है तो प्यार की तरह😊😊",
    "जरूरी नहीं इश्क़ में बनहूँ के सहारे ही मिले😏😏",
    "किसी को जी भर के महसूस करना भी मोहब्बत है😚😚",
    "नशे में भी तेरा नाम लब पर आता है😘😘",
    "चलते हुए मेरे पाँव लड़खड़ाते हैं😍😍",
    "दर्द सा दिल में उठता है मेरे😘😘",
    "हसीं चेहरे पर भी दाग नजर आता है😍😍",
    "हमने भी एक ऐसे शख्स को चाहा😝😝",
    "जिसको भुला न सके और वो किस्मत मैं भी नहीं😜😜",
    "सच्चा प्यार किसी भूत की तरह होता है🥰🥰",
    "बातें तो सब करते है देखा किसी ने नहीं😚😚",
    "मत पूछ ये की मैं तुझे भुला नहीं सकता😝😝",
    "तेरी यादों के पन्ने को मैं जला नहीं सकता😜😜",
    "संघर्ष यह है कि खुद को मारना होगा🥰🥰",
    "और अपने सुकून की खातिर तुझे रुला नहीं सकता😚😚",
    "दुनिया को आग लगाने की ज़रूरत नहीं😎😎",
    "Naale Duniya Sari Ghumawa🙈🙈",
    "तो मेरे साथ चसल आग खुद लग जाएगी💙💙",
    "तरस गये है हम तेरे मुंह से कुछ सुनने को हम🙊🙊",
    "प्यार की बात न सही कोई शिकायत ही कर दे  🙈🙈",
    "तुम नहीं हो पास मगर तन्हाँ रात वही है ❤️❤️",
    "वही है चाहत यादों की बरसात वही है🙈🙈",
    "हर खुशी भी दूर है मेरे आशियाने से ❤️❤️",
    "खामोश लम्हों में दर्द-ए-हालात वही है💫💫",
    "करने लगे जब शिकवा उससे उसकी बेवफाई का😁😁",
    "रख कर होंट को होंट से खामोश कर दिया😆😆",
    "राह में मिले थे हम, राहें नसीब बन गईं😙😙",
    "ना तू अपने घर गया, ना हम अपने घर गये😉😉",
    "तुम्हें नींद नहीं आती तो कोई और वजह होगी😅😅",
    "अब हर ऐब के लिए कसूरवार इश्क तो नहीं😘😘",
    "अना कहती है इल्तेजा क्या करनी😆😆",
    "वो मोहब्बत ही क्या जो मिन्नतों से मिले💕💕",
    "न जाहिर हुई तुमसे और न ही बयान हुई हमसे💓💓",
    "बस सुलझी हुई आँखो में उलझी रही मोहब्बत🥺🥺",
    "गुफ्तगू बंद न हो बात से बात चले🥵🥵",
    "नजरों में रहो कैद दिल से दिल मिले😁😁",
    "है इश्क़ की मंज़िल में हाल कि जैसे😘😘",
    "लुट जाए कहीं राह में सामान किसी का🥰",
    "मुकम्मल ना सही अधूरा ही रहने दो😂😂",
    "ये इश्क़ है कोई मक़सद तो नहीं है🤩🤩",
    "वजह नफरतों की तलाशी जाती है😘😘",
    "मोहब्बत तो बिन वजह ही हो जाती है 😍😍",
    "सिर्फ मरी हुई मछली को ही पानी का बहाव चलाती है 😙😙",
    "जिस मछली में जान होती है वो अपना रास्ता खुद तय करती है",
    "कामयाब लोगों के चेहरों पर दो चीजें होती है 😘😘",
    "एक साइलेंस और दूसरा स्माइल🤔🤔",
    "मेरी चाहत देखनी है तो मेरे दिल पर अपना दिल रखकर देखe😌😌",
    "तेरी धड़कन ना भड्जाये तो मेरी मोहब्बत ठुकरा देना🤫🤫",
    "गलतफहमी की गुंजाईश नहीं सच्ची मोहब्बत में🤪🤪",
    "जहाँ किरदार हल्का हो कहानी डूब जाती है☺️☺️",
    "होने दो मुख़ातिब मुझे आज इन होंटो से अब्बास🤗🤗",
    "बात न तो ये समझ रहे है पर गुफ़्तगू जारी है😶😶",
    "उदासियाँ इश्क़ की पहचान है🤗🤗",
    "मुस्कुरा दिए तो इश्क़ बुरा मान जायेगा😗😗",
    "कुछ इस अदा से हाल सुनाना हमारे दिल😘😘",
    "वो खुद ही कह दे किदी भूल जाना बुरी बात है🥲",
    "माना की उससे बिछड़कर हम उमर भर रोते रहे🤔🤔",
    "पर मेरे मार जाने के बाद उमर भर रोएगा वो😅😅",
    "दिल में तुम्हारी अपनी कभी चोर जायेंगे😁😁",
    "आँखों में इंतज़ार की लकीर छोड़ जायेंगे🙈🙈",
    "किसी मासूम लम्हे मैं किसी मासूम चेहरे से🙉🙉",
    "मोहब्बत की नहीं जाती मोहब्बत हो जाती है😌😌",
    "करीब आओ तो शायद हम समझ लोगे😌😌",
    "ये दूरिया तो केवल फसले बढ़ती है🤫🤫",
    "तेरे इश्क़ में इस तरह मैं नीलाम हो जाओ🤔🤔",
    "आखरी हो मेरी बोली और मैं तेरे नाम हो जाऊ😌😌",
    "आप जब तक रहेंगे आंखों में नजारा बनकर😁😁",
    "रोज आएंगे मेरी दुनिया में उजाला बनकर👅👅",
    "उसे जब से बेवफाई की है मैं प्यार की राह में चल ना सका😅😅",
    "उसे तो किसी और का हाथ थाम लियाबस फिर कभी सम्भल नहीं सका👅👅",
    "एक ही ख़्वाब देखा है कई बार मैंने🤬🤬",
    "तेरी शादी में उलझी है चाहिए मेरे घर की😈😈",
    "तुम्हे मेरी मोहब्बत की कसम सच बताना😎😎",
    "गले में डाल कर बाहें किससे सीखाया है😍😍",
    "नहीं पता की वो कभी मेरी थी भी या नहीं😋😋",
    "मुझे ये पता है बस की माई तो था उमर बस उसी का रहा😌😌",
    "तुमने देखा कभी चाँद से पानी गिरते हुएe😏😏",
    "मैंने देखा ये मंज़र तू में चेहरा धोते हुए😉😉",
    "ठुकरा दे कोई चाहत को तू हस के सह लेना😊😊",
    "प्यार की तबियत में ज़बर जस्ती नहीं होती😉😉",
    "तेरा पता नहीं पर मेरा दिल कभी तैयार नहीं होगा😌😌",
    "मुझे तेरे अलावा कभी किसी और से प्यार नहीं होगा😍😍",
    "दिल में आहट सी हुई रूह में दस्तक गूँजी🤫🤫",
    "किस की खुशबू ये मुझे मेरे सिरहाने आई😁😁",
    "उम्र भर लिखते रहे फिर भी वारक सदा रहा😏😏",
    "जाने किया लफ्ज़ थे जो हम लिख नहीं पाये😌😌",
    "लगा के फूल हाथों से उसने कहा चुपके से😶😶",
    "अगर यहाँ कोई नहीं होता तो फूल की जगह तुम होते😆😆",
    "जान जब प्यारी थी मरने का शौक था🥵🥵",
    "अब मरने का शौक है तो कातिल नहीं मिल रहा🤫🤫",
    "सिर्फ याद बनकर न रह जाये प्यार मेरा🥲🥲",
    "कभी कभी कुछ वक़्त के लिए आया करो😎😎",
    "मुझ को समझाया ना करो अब तो हो चुकी हूँ मुझ मैं😌😌",
    "मोहब्बत मशवरा होती तो तुम से पूछ लेता😁😁",
    "उन्हों ने कहा बहुत बोलते हो अब क्या बरस जाओगे😂😂",
    "हमने कहा जिस दिन चुप हो गया तुम तरस जाओ गए😶😶",
    "कुछ ऐसे हस्दे ज़िन्दगी मैं होते है🤔🤔",
    "के इंसान तो बच जाता है मगर ज़िंदा नहीं रहता😂💓",
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
        global USER_DB
        try:
            if os.path.exists('users.json'):
                with open('users.json', 'r') as f:
                    USER_DB = json.load(f)
        except:
            USER_DB = {}

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

    # AI Features with Inline Input
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

    # New Video Features
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
        """Ask user for password for video access"""
        video_names = {
            "paradox_video": "📹 ParadoxVideo",
            "next_vid": "🎞 NextVid", 
            "social_vid": "📱 SocialVid",
            "light_vid": "💡 LightVid"
        }
        
        password_text = f"""
╔══════════════════╗
    🔒 ᴘᴀssᴡᴏʀᴅ ʀᴇǫᴜɪʀᴇᴅ
╚══════════════════╝

*ᴀᴄᴄᴇssɪɴɢ:* {video_names.get(video_type, "Premium Content")}

🔐 *ᴘʟᴇᴀsᴇ ᴇɴᴛᴇʀ ᴛʜᴇ ᴘᴀssᴡᴏʀᴅ:*
ᴛʏᴘᴇ ᴛʜᴇ 𝟾-ᴅɪɢɪᴛ ᴘɪɴ ᴛᴏ ᴠᴇʀɪғʏ ʏᴏᴜʀ ᴀᴄᴄᴇss.

💡 *ᴛɪᴘ:* The password is 14371437
        """
        
        # Set user state for password verification
        USER_STATES[str(query.from_user.id)] = f"waiting_{video_type}_password"
        
        await query.edit_message_caption(
            caption=password_text,
            parse_mode=ParseMode.MARKDOWN
        )

    async def handle_password_input(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle password input for video access"""
        user_id = update.effective_user.id
        user_message = update.message.text.strip()
        
        # Check if user is waiting for any video password
        video_types = ["paradox_video", "next_vid", "social_vid", "light_vid"]
        current_state = None
        video_type = None
        
        for vtype in video_types:
            state_key = f"waiting_{vtype}_password"
            if str(user_id) in USER_STATES and USER_STATES[str(user_id)] == state_key:
                current_state = state_key
                video_type = vtype
                break
        
        if current_state and video_type:
            if user_message == "14371437":
                # Password correct - send random media
                await self.send_random_media(update, video_type)
                del USER_STATES[str(user_id)]
            else:
                # Password incorrect
                await update.message.reply_text(
                    "❌ *ɪɴᴄᴏʀʀᴇᴄᴛ ᴘᴀssᴡᴏʀᴅ!*\n\nᴘʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ ᴏʀ ɢᴏ ʙᴀᴄᴋ ᴛᴏ ᴛʜᴇ ᴍᴇɴᴜ.",
                    parse_mode=ParseMode.MARKDOWN
                )

    async def send_random_media(self, update: Update, video_type: str):
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
                await update.message.reply_video(
                    video=media_url,
                    caption=caption,
                    parse_mode=ParseMode.MARKDOWN
                )
            else:
                await update.message.reply_photo(
                    photo=media_url,
                    caption=caption,
                    parse_mode=ParseMode.MARKDOWN
                )
        except Exception as e:
            logging.error(f"Error sending media: {e}")
            await update.message.reply_text(
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
        
        # Check if user is in a state (waiting for AI input or password)
        if str(user_id) in USER_STATES:
            # Check for video generation states
            if USER_STATES[str(user_id)] == "waiting_for_video_prompt":
                await self.handle_text_to_video_input(update, context)
                return
            elif USER_STATES[str(user_id)] == "waiting_for_image_prompt":
                await self.handle_text_to_image_input(update, context)
                return
            elif USER_STATES[str(user_id)] == "waiting_for_sd3_prompt":
                await self.handle_sd3_image_input(update, context)
                return
            
            # Check for password states
            video_types = ["paradox_video", "next_vid", "social_vid", "light_vid"]
            for vtype in video_types:
                if USER_STATES[str(user_id)] == f"waiting_{vtype}_password":
                    await self.handle_password_input(update, context)
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
    
    # Private message handler for AI features, password input and normal chat
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
    print("🎨 AI Features: Text-to-Video, Text-to-Image & SD3 AI")
    print("🔒 Password Protected Videos: PIN 14371437")
    print("🚀 Direct Bot Mode - No Group Functionality")
    application.run_polling()

if __name__ == '__main__':
    main()
