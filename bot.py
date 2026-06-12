import logging
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

# ======= НАСТРОЙКИ =======
BOT_TOKEN = "8947877732:AAHUjh18w5vL1NBRueuEFFHS-eQQsVa72Xk"
ADMIN_ID = 5613493357
# =========================

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

orders = {}
order_counter = [0]

# ======= ПЕРЕВОДЫ =======
TEXTS = {
    "en": {
        "welcome": (
            "🎨 <b>Welcome to RetainX Studio</b>\n\n"
            "Generate stunning AI videos, images & audio\n"
            "at the <b>lowest prices on the market</b> ⚡\n\n"
            "✅ Kling 3.0 · Veo 3 · Sora 2 · Midjourney\n"
            "✅ Fast delivery · Premium quality\n\n"
            "👇 Choose what you want to create:"
        ),
        "choose_category": "👇 Choose what you want to create:",
        "select_model": "Select a model:",
        "enter_prompt": (
            "✍️ Enter your prompt in English:\n"
            "<i>(Describe what you want to generate in detail)</i>"
        ),
        "order_summary": "📋 <b>Order Summary</b>",
        "model": "🤖 Model",
        "price": "💰 Price",
        "your_prompt": "📝 Your prompt",
        "ready": "Ready to place your order?",
        "pay_btn": "💳 Pay ${price} — Confirm Order",
        "edit_prompt": "✏️ Edit Prompt",
        "main_menu": "⬅️ Main Menu",
        "back": "⬅️ Back",
        "pricing_btn": "💰 Pricing",
        "support_btn": "💬 Support",
        "place_order": "🚀 Place Order",
        "payment_instructions": (
            "✅ <b>Order #{order_id} Created!</b>\n\n"
            "🤖 Model: <b>{model}</b>\n"
            "💰 Amount: <b>${price}</b>\n\n"
            "💳 <b>Payment Instructions:</b>\n"
            "Send <b>${price}</b> USDT (TRC20) to:\n\n"
            "<code>TGZu7K7kfqtNMTqCABfByLceuA49qRvLgo</code>\n\n"
            "After payment, send your transaction ID here ⬇️"
        ),
        "payment_received": (
            "⏳ <b>Payment received!</b>\n\n"
            "We're verifying and will start generating shortly.\n"
            "Usually 5–15 minutes ⚡"
        ),
        "generating": (
            "🎬 <b>Payment confirmed! Generating now...</b>\n\n"
            "Model: <b>{model}</b>\n"
            "Prompt: <i>{prompt}</i>\n\n"
            "⏱ Est. time: 5–15 minutes"
        ),
        "delivered_caption": (
            "✨ <b>Your generation is ready!</b>\n\n"
            "🤖 Model: {model}\n"
            "📝 Prompt: <i>{prompt}</i>\n\n"
            "Thank you for using RetainX Studio! 🎨\n"
            "Order again → /start"
        ),
        "cancelled": (
            "❌ <b>Order Cancelled</b>\n\n"
            "If you made a payment, contact support.\n"
            "💬 @RetainXStudioBot"
        ),
        "pricing_title": "💰 <b>RetainX Studio — Price List</b>\n\n",
        "pricing_footer": "🔥 Up to 3x cheaper than competitors!",
        "cat_video": "🎬 Video Generation",
        "cat_image": "🖼 Image Generation",
        "cat_audio": "🎵 Audio & Voice",
    },
    "ru": {
        "welcome": (
            "🎨 <b>Добро пожаловать в RetainX Studio</b>\n\n"
            "Генерируй крутые AI видео, изображения и аудио\n"
            "по <b>самым низким ценам на рынке</b> ⚡\n\n"
            "✅ Kling 3.0 · Veo 3 · Sora 2 · Midjourney\n"
            "✅ Быстрая доставка · Премиум качество\n\n"
            "👇 Выбери что хочешь создать:"
        ),
        "choose_category": "👇 Выбери что хочешь создать:",
        "select_model": "Выбери модель:",
        "enter_prompt": (
            "✍️ Введи промт на английском:\n"
            "<i>(Опиши подробно что хочешь сгенерировать)</i>"
        ),
        "order_summary": "📋 <b>Детали заказа</b>",
        "model": "🤖 Модель",
        "price": "💰 Цена",
        "your_prompt": "📝 Твой промт",
        "ready": "Готов оформить заказ?",
        "pay_btn": "💳 Оплатить ${price} — Подтвердить",
        "edit_prompt": "✏️ Изменить промт",
        "main_menu": "⬅️ Главное меню",
        "back": "⬅️ Назад",
        "pricing_btn": "💰 Цены",
        "support_btn": "💬 Поддержка",
        "place_order": "🚀 Сделать заказ",
        "payment_instructions": (
            "✅ <b>Заказ #{order_id} создан!</b>\n\n"
            "🤖 Модель: <b>{model}</b>\n"
            "💰 Сумма: <b>${price}</b>\n\n"
            "💳 <b>Оплата:</b>\n"
            "Отправь <b>${price}</b> USDT (TRC20) на:\n\n"
            "<code>YOUR_WALLET_ADDRESS</code>\n\n"
            "После оплаты пришли ID транзакции сюда ⬇️"
        ),
        "payment_received": (
            "⏳ <b>Оплата получена!</b>\n\n"
            "Проверяем и скоро начнём генерацию.\n"
            "Обычно 5–15 минут ⚡"
        ),
        "generating": (
            "🎬 <b>Оплата подтверждена! Генерируем...</b>\n\n"
            "Модель: <b>{model}</b>\n"
            "Промт: <i>{prompt}</i>\n\n"
            "⏱ Примерно 5–15 минут"
        ),
        "delivered_caption": (
            "✨ <b>Твоя генерация готова!</b>\n\n"
            "🤖 Модель: {model}\n"
            "📝 Промт: <i>{prompt}</i>\n\n"
            "Спасибо за заказ в RetainX Studio! 🎨\n"
            "Заказать снова → /start"
        ),
        "cancelled": (
            "❌ <b>Заказ отменён</b>\n\n"
            "Если вы сделали оплату, свяжитесь с поддержкой.\n"
            "💬 @RetainXStudioBot"
        ),
        "pricing_title": "💰 <b>RetainX Studio — Прайс-лист</b>\n\n",
        "pricing_footer": "🔥 До 3х дешевле конкурентов!",
        "cat_video": "🎬 Генерация видео",
        "cat_image": "🖼 Генерация изображений",
        "cat_audio": "🎵 Аудио и озвучка",
    },
    "es": {
        "welcome": (
            "🎨 <b>Bienvenido a RetainX Studio</b>\n\n"
            "Genera videos, imágenes y audio con IA\n"
            "a los <b>precios más bajos del mercado</b> ⚡\n\n"
            "✅ Kling 3.0 · Veo 3 · Sora 2 · Midjourney\n"
            "✅ Entrega rápida · Calidad premium\n\n"
            "👇 ¿Qué quieres crear?"
        ),
        "choose_category": "👇 ¿Qué quieres crear?",
        "select_model": "Selecciona un modelo:",
        "enter_prompt": (
            "✍️ Escribe tu prompt en inglés:\n"
            "<i>(Describe en detalle lo que quieres generar)</i>"
        ),
        "order_summary": "📋 <b>Resumen del pedido</b>",
        "model": "🤖 Modelo",
        "price": "💰 Precio",
        "your_prompt": "📝 Tu prompt",
        "ready": "¿Listo para hacer tu pedido?",
        "pay_btn": "💳 Pagar ${price} — Confirmar",
        "edit_prompt": "✏️ Editar prompt",
        "main_menu": "⬅️ Menú principal",
        "back": "⬅️ Atrás",
        "pricing_btn": "💰 Precios",
        "support_btn": "💬 Soporte",
        "place_order": "🚀 Hacer pedido",
        "payment_instructions": (
            "✅ <b>¡Pedido #{order_id} creado!</b>\n\n"
            "🤖 Modelo: <b>{model}</b>\n"
            "💰 Monto: <b>${price}</b>\n\n"
            "💳 <b>Instrucciones de pago:</b>\n"
            "Envía <b>${price}</b> USDT (TRC20) a:\n\n"
            "<code>YOUR_WALLET_ADDRESS</code>\n\n"
            "Después del pago, envía tu ID de transacción aquí ⬇️"
        ),
        "payment_received": (
            "⏳ <b>¡Pago recibido!</b>\n\n"
            "Verificando y comenzaremos pronto.\n"
            "Normalmente 5–15 minutos ⚡"
        ),
        "generating": (
            "🎬 <b>¡Pago confirmado! Generando ahora...</b>\n\n"
            "Modelo: <b>{model}</b>\n"
            "Prompt: <i>{prompt}</i>\n\n"
            "⏱ Aprox. 5–15 minutos"
        ),
        "delivered_caption": (
            "✨ <b>¡Tu generación está lista!</b>\n\n"
            "🤖 Modelo: {model}\n"
            "📝 Prompt: <i>{prompt}</i>\n\n"
            "¡Gracias por usar RetainX Studio! 🎨\n"
            "Pedir de nuevo → /start"
        ),
        "cancelled": (
            "❌ <b>Pedido cancelado</b>\n\n"
            "Si realizaste un pago, contacta soporte.\n"
            "💬 @RetainXStudioBot"
        ),
        "pricing_title": "💰 <b>RetainX Studio — Lista de precios</b>\n\n",
        "pricing_footer": "🔥 ¡Hasta 3x más barato que la competencia!",
        "cat_video": "🎬 Generación de video",
        "cat_image": "🖼 Generación de imágenes",
        "cat_audio": "🎵 Audio y voz",
    },
    "de": {
        "welcome": (
            "🎨 <b>Willkommen bei RetainX Studio</b>\n\n"
            "Erstelle beeindruckende KI-Videos, Bilder & Audio\n"
            "zu den <b>niedrigsten Preisen am Markt</b> ⚡\n\n"
            "✅ Kling 3.0 · Veo 3 · Sora 2 · Midjourney\n"
            "✅ Schnelle Lieferung · Premium-Qualität\n\n"
            "👇 Was möchtest du erstellen?"
        ),
        "choose_category": "👇 Was möchtest du erstellen?",
        "select_model": "Wähle ein Modell:",
        "enter_prompt": (
            "✍️ Gib deinen Prompt auf Englisch ein:\n"
            "<i>(Beschreibe detailliert, was du generieren möchtest)</i>"
        ),
        "order_summary": "📋 <b>Bestellübersicht</b>",
        "model": "🤖 Modell",
        "price": "💰 Preis",
        "your_prompt": "📝 Dein Prompt",
        "ready": "Bereit zur Bestellung?",
        "pay_btn": "💳 ${price} bezahlen — Bestätigen",
        "edit_prompt": "✏️ Prompt bearbeiten",
        "main_menu": "⬅️ Hauptmenü",
        "back": "⬅️ Zurück",
        "pricing_btn": "💰 Preise",
        "support_btn": "💬 Support",
        "place_order": "🚀 Bestellen",
        "payment_instructions": (
            "✅ <b>Bestellung #{order_id} erstellt!</b>\n\n"
            "🤖 Modell: <b>{model}</b>\n"
            "💰 Betrag: <b>${price}</b>\n\n"
            "💳 <b>Zahlungsanweisungen:</b>\n"
            "Sende <b>${price}</b> USDT (TRC20) an:\n\n"
            "<code>YOUR_WALLET_ADDRESS</code>\n\n"
            "Nach der Zahlung sende deine Transaktions-ID hier ⬇️"
        ),
        "payment_received": (
            "⏳ <b>Zahlung erhalten!</b>\n\n"
            "Wir prüfen und beginnen bald mit der Generierung.\n"
            "Normalerweise 5–15 Minuten ⚡"
        ),
        "generating": (
            "🎬 <b>Zahlung bestätigt! Generierung läuft...</b>\n\n"
            "Modell: <b>{model}</b>\n"
            "Prompt: <i>{prompt}</i>\n\n"
            "⏱ Ca. 5–15 Minuten"
        ),
        "delivered_caption": (
            "✨ <b>Deine Generierung ist fertig!</b>\n\n"
            "🤖 Modell: {model}\n"
            "📝 Prompt: <i>{prompt}</i>\n\n"
            "Danke für RetainX Studio! 🎨\n"
            "Erneut bestellen → /start"
        ),
        "cancelled": (
            "❌ <b>Bestellung storniert</b>\n\n"
            "Bei Zahlung bitte Support kontaktieren.\n"
            "💬 @RetainXStudioBot"
        ),
        "pricing_title": "💰 <b>RetainX Studio — Preisliste</b>\n\n",
        "pricing_footer": "🔥 Bis zu 3x günstiger als die Konkurrenz!",
        "cat_video": "🎬 Videogenerierung",
        "cat_image": "🖼 Bildgenerierung",
        "cat_audio": "🎵 Audio & Stimme",
    },
    "fr": {
        "welcome": (
            "🎨 <b>Bienvenue sur RetainX Studio</b>\n\n"
            "Génère des vidéos, images et audios IA\n"
            "aux <b>prix les plus bas du marché</b> ⚡\n\n"
            "✅ Kling 3.0 · Veo 3 · Sora 2 · Midjourney\n"
            "✅ Livraison rapide · Qualité premium\n\n"
            "👇 Que veux-tu créer ?"
        ),
        "choose_category": "👇 Que veux-tu créer ?",
        "select_model": "Choisis un modèle :",
        "enter_prompt": (
            "✍️ Entre ton prompt en anglais :\n"
            "<i>(Décris en détail ce que tu veux générer)</i>"
        ),
        "order_summary": "📋 <b>Résumé de la commande</b>",
        "model": "🤖 Modèle",
        "price": "💰 Prix",
        "your_prompt": "📝 Ton prompt",
        "ready": "Prêt à passer commande ?",
        "pay_btn": "💳 Payer ${price} — Confirmer",
        "edit_prompt": "✏️ Modifier le prompt",
        "main_menu": "⬅️ Menu principal",
        "back": "⬅️ Retour",
        "pricing_btn": "💰 Tarifs",
        "support_btn": "💬 Support",
        "place_order": "🚀 Commander",
        "payment_instructions": (
            "✅ <b>Commande #{order_id} créée !</b>\n\n"
            "🤖 Modèle : <b>{model}</b>\n"
            "💰 Montant : <b>${price}</b>\n\n"
            "💳 <b>Instructions de paiement :</b>\n"
            "Envoie <b>${price}</b> USDT (TRC20) à :\n\n"
            "<code>YOUR_WALLET_ADDRESS</code>\n\n"
            "Après le paiement, envoie ton ID de transaction ici ⬇️"
        ),
        "payment_received": (
            "⏳ <b>Paiement reçu !</b>\n\n"
            "Nous vérifions et commençons bientôt.\n"
            "Généralement 5–15 minutes ⚡"
        ),
        "generating": (
            "🎬 <b>Paiement confirmé ! Génération en cours...</b>\n\n"
            "Modèle : <b>{model}</b>\n"
            "Prompt : <i>{prompt}</i>\n\n"
            "⏱ Environ 5–15 minutes"
        ),
        "delivered_caption": (
            "✨ <b>Ta génération est prête !</b>\n\n"
            "🤖 Modèle : {model}\n"
            "📝 Prompt : <i>{prompt}</i>\n\n"
            "Merci d'utiliser RetainX Studio ! 🎨\n"
            "Commander à nouveau → /start"
        ),
        "cancelled": (
            "❌ <b>Commande annulée</b>\n\n"
            "Si tu as payé, contacte le support.\n"
            "💬 @RetainXStudioBot"
        ),
        "pricing_title": "💰 <b>RetainX Studio — Tarifs</b>\n\n",
        "pricing_footer": "🔥 Jusqu'à 3x moins cher que la concurrence !",
        "cat_video": "🎬 Génération vidéo",
        "cat_image": "🖼 Génération d'images",
        "cat_audio": "🎵 Audio & Voix",
    },
    "zh": {
        "welcome": (
            "🎨 <b>欢迎来到 RetainX Studio</b>\n\n"
            "以<b>市场最低价格</b>生成精彩的AI视频、图像和音频 ⚡\n\n"
            "✅ Kling 3.0 · Veo 3 · Sora 2 · Midjourney\n"
            "✅ 快速交付 · 顶级质量\n\n"
            "👇 选择你想创建的内容："
        ),
        "choose_category": "👇 选择你想创建的内容：",
        "select_model": "选择模型：",
        "enter_prompt": (
            "✍️ 用英文输入你的提示词：\n"
            "<i>（详细描述你想要生成的内容）</i>"
        ),
        "order_summary": "📋 <b>订单摘要</b>",
        "model": "🤖 模型",
        "price": "💰 价格",
        "your_prompt": "📝 你的提示词",
        "ready": "准备好下单了吗？",
        "pay_btn": "💳 支付 ${price} — 确认订单",
        "edit_prompt": "✏️ 修改提示词",
        "main_menu": "⬅️ 主菜单",
        "back": "⬅️ 返回",
        "pricing_btn": "💰 价格表",
        "support_btn": "💬 客服支持",
        "place_order": "🚀 立即下单",
        "payment_instructions": (
            "✅ <b>订单 #{order_id} 已创建！</b>\n\n"
            "🤖 模型：<b>{model}</b>\n"
            "💰 金额：<b>${price}</b>\n\n"
            "💳 <b>付款说明：</b>\n"
            "发送 <b>${price}</b> USDT（TRC20）至：\n\n"
            "<code>YOUR_WALLET_ADDRESS</code>\n\n"
            "付款后，在此发送你的交易ID ⬇️"
        ),
        "payment_received": (
            "⏳ <b>收到付款！</b>\n\n"
            "正在验证，即将开始生成。\n"
            "通常需要5–15分钟 ⚡"
        ),
        "generating": (
            "🎬 <b>付款已确认！正在生成...</b>\n\n"
            "模型：<b>{model}</b>\n"
            "提示词：<i>{prompt}</i>\n\n"
            "⏱ 预计5–15分钟"
        ),
        "delivered_caption": (
            "✨ <b>你的生成结果已完成！</b>\n\n"
            "🤖 模型：{model}\n"
            "📝 提示词：<i>{prompt}</i>\n\n"
            "感谢使用 RetainX Studio！🎨\n"
            "再次下单 → /start"
        ),
        "cancelled": (
            "❌ <b>订单已取消</b>\n\n"
            "如已付款，请联系客服。\n"
            "💬 @RetainXStudioBot"
        ),
        "pricing_title": "💰 <b>RetainX Studio — 价格表</b>\n\n",
        "pricing_footer": "🔥 比竞争对手便宜3倍！",
        "cat_video": "🎬 视频生成",
        "cat_image": "🖼 图像生成",
        "cat_audio": "🎵 音频与配音",
    },
    "ar": {
        "welcome": (
            "🎨 <b>مرحباً بك في RetainX Studio</b>\n\n"
            "أنشئ فيديوهات وصور وصوتيات بالذكاء الاصطناعي\n"
            "بـ<b>أقل الأسعار في السوق</b> ⚡\n\n"
            "✅ Kling 3.0 · Veo 3 · Sora 2 · Midjourney\n"
            "✅ تسليم سريع · جودة ممتازة\n\n"
            "👇 اختر ما تريد إنشاءه:"
        ),
        "choose_category": "👇 اختر ما تريد إنشاءه:",
        "select_model": "اختر النموذج:",
        "enter_prompt": (
            "✍️ أدخل وصفك باللغة الإنجليزية:\n"
            "<i>(اصف بالتفصيل ما تريد توليده)</i>"
        ),
        "order_summary": "📋 <b>ملخص الطلب</b>",
        "model": "🤖 النموذج",
        "price": "💰 السعر",
        "your_prompt": "📝 وصفك",
        "ready": "هل أنت جاهز لتقديم طلبك؟",
        "pay_btn": "💳 ادفع ${price} — تأكيد الطلب",
        "edit_prompt": "✏️ تعديل الوصف",
        "main_menu": "⬅️ القائمة الرئيسية",
        "back": "⬅️ رجوع",
        "pricing_btn": "💰 الأسعار",
        "support_btn": "💬 الدعم",
        "place_order": "🚀 تقديم الطلب",
        "payment_instructions": (
            "✅ <b>تم إنشاء الطلب #{order_id}!</b>\n\n"
            "🤖 النموذج: <b>{model}</b>\n"
            "💰 المبلغ: <b>${price}</b>\n\n"
            "💳 <b>تعليمات الدفع:</b>\n"
            "أرسل <b>${price}</b> USDT (TRC20) إلى:\n\n"
            "<code>YOUR_WALLET_ADDRESS</code>\n\n"
            "بعد الدفع، أرسل معرّف المعاملة هنا ⬇️"
        ),
        "payment_received": (
            "⏳ <b>تم استلام الدفع!</b>\n\n"
            "نحن نتحقق وسنبدأ قريباً.\n"
            "عادةً 5–15 دقيقة ⚡"
        ),
        "generating": (
            "🎬 <b>تم تأكيد الدفع! جارٍ التوليد...</b>\n\n"
            "النموذج: <b>{model}</b>\n"
            "الوصف: <i>{prompt}</i>\n\n"
            "⏱ المدة المتوقعة: 5–15 دقيقة"
        ),
        "delivered_caption": (
            "✨ <b>توليدك جاهز!</b>\n\n"
            "🤖 النموذج: {model}\n"
            "📝 الوصف: <i>{prompt}</i>\n\n"
            "شكراً لاستخدام RetainX Studio! 🎨\n"
            "اطلب مرة أخرى → /start"
        ),
        "cancelled": (
            "❌ <b>تم إلغاء الطلب</b>\n\n"
            "إن كنت قد دفعت، تواصل مع الدعم.\n"
            "💬 @RetainXStudioBot"
        ),
        "pricing_title": "💰 <b>RetainX Studio — قائمة الأسعار</b>\n\n",
        "pricing_footer": "🔥 أرخص بـ3 مرات من المنافسين!",
        "cat_video": "🎬 توليد الفيديو",
        "cat_image": "🖼 توليد الصور",
        "cat_audio": "🎵 الصوت والتعليق",
    },
}

def get_lang(user: types.User) -> str:
    code = (user.language_code or "en")[:2].lower()
    return code if code in TEXTS else "en"

def t(lang: str, key: str) -> str:
    return TEXTS.get(lang, TEXTS["en"]).get(key, TEXTS["en"].get(key, key))

# ======= МОДЕЛИ =======
CATEGORIES_DATA = [
    ("cat_video", [
        ("Kling 3.0", 2.99), ("Kling 2.6 Motion", 1.66), ("Kling 2.1", 1.33),
        ("Google Veo 3", 2.33), ("Google Veo 3 Fast", 1.66),
        ("Seedance 2.0", 1.99), ("Hailuo 02", 1.99),
        ("Runway Aleph", 2.33), ("Runway Gen-4", 1.33),
        ("Sora 2", 1.99), ("Sora 2 PRO", 2.33),
    ]),
    ("cat_image", [
        ("Midjourney", 1.33), ("Grok Imagine", 0.49), ("Flux Pro", 0.66),
    ]),
    ("cat_audio", [
        ("Suno Music", 0.99), ("ElevenLabs Voice", 0.99),
    ]),
]

MODELS_BY_CAT = {cat: models for cat, models in CATEGORIES_DATA}
MODEL_PRICES = {m: p for _, models in CATEGORIES_DATA for m, p in models}

# ======= СОСТОЯНИЯ =======
class OrderStates(StatesGroup):
    choosing_model = State()
    entering_prompt = State()
    waiting_payment = State()

# ======= СТАРТ =======
@dp.message(CommandStart())
async def start(message: types.Message, state: FSMContext):
    await state.clear()
    lang = get_lang(message.from_user)
    await state.update_data(lang=lang)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t(lang, "cat_video"), callback_data="cat_video")],
        [InlineKeyboardButton(text=t(lang, "cat_image"), callback_data="cat_image")],
        [InlineKeyboardButton(text=t(lang, "cat_audio"), callback_data="cat_audio")],
        [InlineKeyboardButton(text=t(lang, "pricing_btn"), callback_data="pricing")],
        [InlineKeyboardButton(text=t(lang, "support_btn"), url="https://t.me/RetainXStudioBot")],
    ])
    await message.answer(t(lang, "welcome"), reply_markup=keyboard, parse_mode="HTML")

# ======= ПРАЙС =======
@dp.callback_query(F.data == "pricing")
async def show_pricing(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", get_lang(callback.from_user))
    text = t(lang, "pricing_title")
    for cat_key, models in CATEGORIES_DATA:
        text += f"<b>{t(lang, cat_key)}</b>\n"
        for model, price in models:
            text += f"  • {model} — <b>${price}</b>\n"
        text += "\n"
    text += t(lang, "pricing_footer")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t(lang, "place_order"), callback_data="back_to_menu")],
    ])
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")

# ======= МЕНЮ =======
@dp.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    lang = get_lang(callback.from_user)
    await state.update_data(lang=lang)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t(lang, "cat_video"), callback_data="cat_video")],
        [InlineKeyboardButton(text=t(lang, "cat_image"), callback_data="cat_image")],
        [InlineKeyboardButton(text=t(lang, "cat_audio"), callback_data="cat_audio")],
        [InlineKeyboardButton(text=t(lang, "pricing_btn"), callback_data="pricing")],
        [InlineKeyboardButton(text=t(lang, "support_btn"), url="https://t.me/RetainXStudioBot")],
    ])
    await callback.message.edit_text(t(lang, "choose_category"), reply_markup=keyboard, parse_mode="HTML")

# ======= КАТЕГОРИЯ =======
@dp.callback_query(F.data.in_({"cat_video", "cat_image", "cat_audio"}))
async def choose_category(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", get_lang(callback.from_user))
    cat_key = callback.data
    models = MODELS_BY_CAT.get(cat_key, [])
    buttons = [[InlineKeyboardButton(text=f"{m} — ${p}", callback_data=f"model_{m}")] for m, p in models]
    buttons.append([InlineKeyboardButton(text=t(lang, "back"), callback_data="back_to_menu")])
    await callback.message.edit_text(
        f"<b>{t(lang, cat_key)}</b>\n\n{t(lang, 'select_model')}",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons),
        parse_mode="HTML"
    )
    await state.set_state(OrderStates.choosing_model)

# ======= МОДЕЛЬ =======
@dp.callback_query(F.data.startswith("model_"))
async def choose_model(callback: types.CallbackQuery, state: FSMContext):
    model_name = callback.data.replace("model_", "")
    price = MODEL_PRICES.get(model_name)
    data = await state.get_data()
    lang = data.get("lang", get_lang(callback.from_user))
    await state.update_data(model=model_name, price=price)
    await callback.message.edit_text(
        f"✅ <b>{model_name}</b> — ${price}\n\n{t(lang, 'enter_prompt')}",
        parse_mode="HTML"
    )
    await state.set_state(OrderStates.entering_prompt)

# ======= ПРОМТ =======
@dp.message(OrderStates.entering_prompt)
async def receive_prompt(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", get_lang(message.from_user))
    model = data.get("model")
    price = data.get("price")
    prompt = message.text
    await state.update_data(prompt=prompt)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t(lang, "pay_btn").replace("${price}", str(price)), callback_data="confirm_order")],
        [InlineKeyboardButton(text=t(lang, "edit_prompt"), callback_data=f"model_{model}")],
        [InlineKeyboardButton(text=t(lang, "main_menu"), callback_data="back_to_menu")],
    ])
    await message.answer(
        f"{t(lang, 'order_summary')}\n\n"
        f"{t(lang, 'model')}: <b>{model}</b>\n"
        f"{t(lang, 'price')}: <b>${price}</b>\n\n"
        f"{t(lang, 'your_prompt')}:\n<i>{prompt}</i>\n\n"
        f"{t(lang, 'ready')}",
        reply_markup=keyboard,
        parse_mode="HTML"
    )

# ======= ПОДТВЕРЖДЕНИЕ =======
@dp.callback_query(F.data == "confirm_order")
async def confirm_order(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", get_lang(callback.from_user))
    model = data.get("model")
    price = data.get("price")
    prompt = data.get("prompt")
    user = callback.from_user
    order_counter[0] += 1
    order_id = order_counter[0]
    orders[order_id] = {
        "user_id": user.id, "username": user.username or user.first_name,
        "model": model, "price": price, "prompt": prompt,
        "status": "pending_payment", "lang": lang
    }
    admin_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Confirm Payment & Start", callback_data=f"paid_{order_id}")],
        [InlineKeyboardButton(text="❌ Cancel Order", callback_data=f"cancel_{order_id}")],
    ])
    await bot.send_message(
        ADMIN_ID,
        f"🔔 <b>NEW ORDER #{order_id}</b>\n\n"
        f"👤 @{user.username or 'no username'} (ID: {user.id})\n"
        f"🌐 Lang: {lang}\n"
        f"🤖 Model: <b>{model}</b>\n"
        f"💰 Price: <b>${price}</b>\n\n"
        f"📝 Prompt:\n<code>{prompt}</code>",
        reply_markup=admin_keyboard, parse_mode="HTML"
    )
    await callback.message.edit_text(
        t(lang, "payment_instructions").format(order_id=order_id, model=model, price=price),
        parse_mode="HTML"
    )
    await state.set_state(OrderStates.waiting_payment)
    await state.update_data(order_id=order_id)

# ======= TX HASH =======
@dp.message(OrderStates.waiting_payment)
async def receive_payment_proof(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "en")
    order_id = data.get("order_id")
    order = orders.get(order_id)
    if not order:
        return
    orders[order_id]["tx_proof"] = message.text
    orders[order_id]["status"] = "payment_sent"
    admin_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Confirm Payment", callback_data=f"paid_{order_id}")],
        [InlineKeyboardButton(text="❌ Reject", callback_data=f"cancel_{order_id}")],
    ])
    await bot.send_message(
        ADMIN_ID,
        f"💸 <b>Payment Proof — Order #{order_id}</b>\n\n"
        f"👤 @{order['username']} | 🌐 {lang}\n"
        f"🤖 {order['model']} — ${order['price']}\n"
        f"📝 <code>{order['prompt']}</code>\n\n"
        f"🧾 TX: <code>{message.text}</code>",
        reply_markup=admin_keyboard, parse_mode="HTML"
    )
    await message.answer(t(lang, "payment_received"), parse_mode="HTML")

# ======= АДМИН: ПОДТВЕРДИТЬ =======
@dp.callback_query(F.data.startswith("paid_"))
async def admin_confirm_paid(callback: types.CallbackQuery):
    order_id = int(callback.data.replace("paid_", ""))
    order = orders.get(order_id)
    if not order:
        await callback.answer("Not found")
        return
    orders[order_id]["status"] = "generating"
    lang = order.get("lang", "en")
    await bot.send_message(
        order["user_id"],
        t(lang, "generating").format(model=order["model"], prompt=order["prompt"]),
        parse_mode="HTML"
    )
    await callback.message.edit_text(
        f"✅ Order #{order_id} confirmed!\n"
        f"🤖 {order['model']}\n📝 {order['prompt']}\n\n"
        f"Generate in Artlist then type:\n/send_{order_id}\nand attach the file."
    )
    await callback.answer("Confirmed!")

# ======= АДМИН: ОТМЕНИТЬ =======
@dp.callback_query(F.data.startswith("cancel_"))
async def admin_cancel(callback: types.CallbackQuery):
    order_id = int(callback.data.replace("cancel_", ""))
    order = orders.get(order_id)
    if not order:
        await callback.answer("Not found")
        return
    orders[order_id]["status"] = "cancelled"
    lang = order.get("lang", "en")
    await bot.send_message(order["user_id"], t(lang, "cancelled"), parse_mode="HTML")
    await callback.message.edit_text(f"❌ Order #{order_id} cancelled.")
    await callback.answer("Cancelled")

# ======= АДМИН: ОТПРАВИТЬ ФАЙЛ =======
@dp.message(F.text.regexp(r"^/send_\d+$"))
async def admin_send_cmd(message: types.Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID:
        return
    order_id = int(message.text.replace("/send_", ""))
    await state.update_data(sending_order_id=order_id)
    await state.set_state("sending_result")
    await message.answer(f"📤 Attach file for Order #{order_id}")

@dp.message(F.from_user.id == ADMIN_ID)
async def admin_deliver(message: types.Message, state: FSMContext):
    if await state.get_state() != "sending_result":
        return
    if not (message.video or message.document or message.photo):
        return
    data = await state.get_data()
    order_id = data.get("sending_order_id")
    order = orders.get(order_id)
    if not order:
        await message.answer("Order not found")
        return
    lang = order.get("lang", "en")
    caption = t(lang, "delivered_caption").format(model=order["model"], prompt=order["prompt"])
    if message.video:
        await bot.send_video(order["user_id"], message.video.file_id, caption=caption, parse_mode="HTML")
    elif message.document:
        await bot.send_document(order["user_id"], message.document.file_id, caption=caption, parse_mode="HTML")
    elif message.photo:
        await bot.send_photo(order["user_id"], message.photo[-1].file_id, caption=caption, parse_mode="HTML")
    orders[order_id]["status"] = "delivered"
    await message.answer(f"✅ Delivered! Order #{order_id} complete.")
    await state.clear()

async def main():
    print("RetainX Studio Bot started! 🚀")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
