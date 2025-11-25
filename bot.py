import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.keyboard import InlineKeyboardBuilder
from deep_translator import GoogleTranslator

def translate_to_russian(text, source_lang):
    try:
        if source_lang == "zh":
            translator = GoogleTranslator(source='zh-CN', target='ru')
        elif source_lang == "en":
            translator = GoogleTranslator(source='en', target='ru')
        else:
            return text
        return translator.translate(text)
    except Exception as e:
        print(f"Ошибка перевода: {e}")
        return text

# === НАСТРОЙКИ ===
BOT_TOKEN = "8563519693:AAGcDz7eTcWpKxK1cISHMsa1F8H5S28TUrI"
MAIN_CHAT_ID = -1003345325031

TOPIC_IDS = {
    "global": 3,
    "russia_sng": 4,
    "china": 5
}

# === ЛОКАЛИЗАЦИЯ ===
MESSAGES = {
    "start_choose_lang": "👋 Добро пожаловать! Пожалуйста, выберите язык.\n\n"
                         "👋 Welcome! Please choose your language.\n\n"
                         "👋 欢迎！请选择语言。",
    "lang_selected": {
        "ru": "🇷🇺 Выбран русский язык.",
        "en": "🇬🇧 English selected.",
        "zh": "🇨🇳 中文已选择。"
    },
    "choose_server": {
        "ru": "🌍 Выберите сервер для демо-запроса:",
        "en": "🌍 Choose a server for the demo request:",
        "zh": "🌍 请选择演示服务器："
    },
    "ask_server_version": {
        "ru": "📦 Выберите версию сервера:",
        "en": "📦 Choose server version:",
        "zh": "📦 请选择服务器版本："
    },
    "ask_area": {  # <-- ИСПРАВЛЕНО: добавлен ключ
        "ru": "📐 Выберите размер игровой площадки:",
        "en": "📐 Choose game area size:",
        "zh": "📐 请选择游戏区域尺寸"
    },
    "ask_vr_device": {
        "ru": "👓 Выберите VR-шлем:",
        "en": "👓 Choose VR headset:",
        "zh": "👓 请选择 VR 头显："
    },
    "ask_partner_contact": {
        "ru": "📎 Хотите добавить контактные данные партнёра?",
        "en": "📎 Would you like to add partner contact details?",
        "zh": "📎 是否要添加合作伙伴联系信息？"
    },
    "partner_contact_yes": {
        "ru": "✅ Да, добавить",
        "en": "✅ Yes, add",
        "zh": "✅ 是，添加"
    },
    "partner_contact_no": {
        "ru": "❌ Нет, пропустить",
        "en": "❌ No, skip",
        "zh": "❌ 否，跳过"
    },
    "ask_partner_name": {
        "ru": "👤 Имя партнёра:",
        "en": "👤 Partner name:",
        "zh": "👤 合作伙伴姓名："
    },
    "ask_partner_phone": {
        "ru": "📱 Номер телефона партнёра:",
        "en": "📱 Partner phone number:",
        "zh": "📱 合作伙伴电话号码："
    },
    "ask_partner_email": {
        "ru": "📧 Email партнёра:",
        "en": "📧 Partner email:",
        "zh": "📧 合作伙伴电子邮件："
    },
    "ask_partner_crm": {
        "ru": "🔗 Ссылка на CRM партнёра:",
        "en": "🔗 Partner CRM link:",
        "zh": "🔗 合作伙伴CRM链接："
    },
    "ask_city": {
        "ru": "🏙️ Укажите город:",
        "en": "🏙️ Enter the city:",
        "zh": "🏙️ 请输入城市："
    },
    "ask_duration": {
        "ru": "⏳ Укажите срок действия демо игры:",
        "en": "⏳ Enter demo validity period:",
        "zh": "⏳ 请输入演示有效期："
    },
    "ask_comment": {
        "ru": "✏️ Добавить комментарий (опционально):",
        "en": "✏️ Add a comment (optional):",
        "zh": "✏️ 添加评论（可选）："
    },
    "enter_comment": {
        "ru": "Введите комментарий:",
        "en": "Enter comment:",
        "zh": "请输入评论："
    },
    "send_without_comment": {
        "ru": "✅ Отправить без комментария",
        "en": "✅ Send without comment",
        "zh": "✅ 发送，无需评论"
    },
    "success_with_link": {
        "ru": "✅ Запрос успешно оформлен и отправлен в раздел <a href='{link}'>[перейти к запросу]</a>",
        "en": "✅ Request successfully submitted and sent to section <a href='{link}'>[go to request]</a>",
        "zh": "✅ 请求已成功提交并发送至分区 <a href='{link}'>[跳转到请求]</a>"
    },
    "final_message": {
        "ru": "Прошу включить {server_type} сервер, для города {city}.\n"
              "Игровая зона с размером {area_size} метров.\n"
              "Версия сервера: {server_version}.\n"
              "Партнер использует {vr_device}.\n"
              "Срок демо показа: {duration} дня(ей).\n"
              "{partner_info}",

        "en": "Please activate the {server_type} server for {city}.\n"
              "Game area size is {area_size} meters.\n"
              "Server version: {server_version}.\n"
              "Partner uses {vr_device}.\n"
              "Demo period: {duration} day(s).\n"
              "{partner_info}",

        "zh": "请启用 {server_type} 服务器，城市 {city}。\n"
              "游戏区域尺寸为 {area_size} 米。\n"
              "服务器版本：{server_version}。\n"
              "合作方使用 {vr_device}。\n"
              "演示有效期：{duration} 天。\n"
              "{partner_info}"
    },
    "buttons": {
        "lang": {
            "ru": {"lang_ru": "🇷🇺 Русский", "lang_en": "🇬🇧 English", "lang_zh": "🇨🇳 中文"},
            "en": {"lang_ru": "🇷🇺 Russian", "lang_en": "🇬🇧 English", "lang_zh": "🇨🇳 Chinese"},
            "zh": {"lang_ru": "🇷🇺 俄语", "lang_en": "🇬🇧 英语", "lang_zh": "🇨🇳 中文"}
        },
        "server": {
            "ru": {"server_usd": "🇺🇸 Сервер USD", "server_eud": "🇪🇺 Сервер EUD", "server_rud": "🇷🇺 Сервер RUD", "server_chd": "🇨🇳 Сервер CHD"},
            "en": {"server_usd": "🇺🇸 Server USD", "server_eud": "🇪🇺 Server EUD", "server_rud": "🇷🇺 Server RUD", "server_chd": "🇨🇳 Server CHD"},
            "zh": {"server_usd": "🇺🇸 服务器 USD", "server_eud": "🇪🇺 服务器 EUD", "server_rud": "🇷🇺 服务器 RUD", "server_chd": "🇨🇳 服务器 CHD"}
        },
        "server_version": {
            "ru": {"ver_1272": "📦 1.2.7.2", "ver_1281": "🚀 1.2.8.1"},
            "en": {"ver_1272": "📦 1.2.7.2", "ver_1281": "🚀 1.2.8.1"},
            "zh": {"ver_1272": "📦 1.2.7.2", "ver_1281": "🚀 1.2.8.1"}
        },
        "vr_device": {
            "ru": {"vr_quest2": "🔵 Meta Quest 2", "vr_quest3": "🔵 Meta Quest 3/3s", "vr_pico4": "🟣 Pico 4", "vr_pico4ultra": "🟣 Pico 4 Ultra/Ultra Enterprise"},
            "en": {"vr_quest2": "🔵 Meta Quest 2", "vr_quest3": "🔵 Meta Quest 3/3s", "vr_pico4": "🟣 Pico 4", "vr_pico4ultra": "🟣 Pico 4 Ultra/Ultra Enterprise"},
            "zh": {"vr_quest2": "🔵 Meta Quest 2", "vr_quest3": "🔵 Meta Quest 3/3s", "vr_pico4": "🟣 Pico 4", "vr_pico4ultra": "🟣 Pico 4 Ultra/Ultra Enterprise"}
        },
        "duration": {
            "ru": {"dur_3": "3 дня", "dur_7": "7 дней", "dur_14": "14 дней", "dur_30": "30 дней"},
            "en": {"dur_3": "3 days", "dur_7": "7 days", "dur_14": "14 days", "dur_30": "30 days"},
            "zh": {"dur_3": "3 天", "dur_7": "7 天", "dur_14": "14 天", "dur_30": "30 天"}
        },
        "comment": {
            "ru": "✏️ Добавить комментарий",
            "en": "✏️ Add comment",
            "zh": "✏️ 添加评论"
        },
        "back": {
            "ru": "⬅️ Назад",
            "en": "⬅️ Back",
            "zh": "⬅️ 返回"
        }
    }
}

AREA_SIZES_GLOBAL = ["4x8", "6x6", "8x8", "9x6", "10x7", "10x10", "10x12", "10x15"]
AREA_SIZES_CHD = ["4x8", "6x6", "7x15", "8x8", "8x12", "9x6", "10x7", "10x10", "10x12", "10x15"]

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# === FSM STATES ===
class Form(StatesGroup):
    language = State()
    server_type = State()
    server_version = State()
    area_size = State()  # <-- ИСПРАВЛЕНО: добавлено состояние
    vr_device = State()
    partner_contact = State()
    partner_name = State()
    partner_phone = State()
    partner_email = State()
    partner_crm = State()
    city = State()
    duration = State()
    comment = State()

# === KEYBOARD FUNCTIONS ===

def get_lang_keyboard(lang_code):
    buttons = MESSAGES["buttons"]["lang"][lang_code]
    return types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text=buttons["lang_ru"], callback_data="lang_ru")],
        [types.InlineKeyboardButton(text=buttons["lang_en"], callback_data="lang_en")],
        [types.InlineKeyboardButton(text=buttons["lang_zh"], callback_data="lang_zh")]
    ])

def get_server_keyboard(lang_code):
    buttons = MESSAGES["buttons"]["server"][lang_code]
    return types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text=buttons["server_usd"], callback_data="server_usd")],
        [types.InlineKeyboardButton(text=buttons["server_eud"], callback_data="server_eud")],
        [types.InlineKeyboardButton(text=buttons["server_rud"], callback_data="server_rud")],
        [types.InlineKeyboardButton(text=buttons["server_chd"], callback_data="server_chd")],
        [types.InlineKeyboardButton(text=MESSAGES["buttons"]["back"][lang_code], callback_data="back")]
    ])

def get_version_keyboard(lang_code):
    buttons = MESSAGES["buttons"]["server_version"][lang_code]
    return types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text=buttons["ver_1272"], callback_data="ver_1272")],
        [types.InlineKeyboardButton(text=buttons["ver_1281"], callback_data="ver_1281")],
        [types.InlineKeyboardButton(text=MESSAGES["buttons"]["back"][lang_code], callback_data="back")]
    ])

def get_area_keyboard(lang_code, server_type):
    sizes = AREA_SIZES_CHD if server_type == "CHD" else AREA_SIZES_GLOBAL
    return types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text=size, callback_data=f"area_{size}")]
        for size in sizes
    ] + [[types.InlineKeyboardButton(text=MESSAGES["buttons"]["back"][lang_code], callback_data="back")]])

def get_vr_keyboard(lang_code):
    buttons = MESSAGES["buttons"]["vr_device"][lang_code]
    return types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text=buttons["vr_quest2"], callback_data="vr_quest2")],
        [types.InlineKeyboardButton(text=buttons["vr_quest3"], callback_data="vr_quest3")],
        [types.InlineKeyboardButton(text=buttons["vr_pico4"], callback_data="vr_pico4")],
        [types.InlineKeyboardButton(text=buttons["vr_pico4ultra"], callback_data="vr_pico4ultra")],
        [types.InlineKeyboardButton(text=MESSAGES["buttons"]["back"][lang_code], callback_data="back")]
    ])

def get_partner_keyboard(lang_code):
    return types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text=MESSAGES["partner_contact_yes"][lang_code], callback_data="partner_yes")],
        [types.InlineKeyboardButton(text=MESSAGES["partner_contact_no"][lang_code], callback_data="partner_no")],
        [types.InlineKeyboardButton(text=MESSAGES["buttons"]["back"][lang_code], callback_data="back")]
    ])

def get_duration_keyboard(lang_code):
    buttons = MESSAGES["buttons"]["duration"][lang_code]
    return types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text=buttons["dur_3"], callback_data="dur_3")],
        [types.InlineKeyboardButton(text=buttons["dur_7"], callback_data="dur_7")],
        [types.InlineKeyboardButton(text=buttons["dur_14"], callback_data="dur_14")],
        [types.InlineKeyboardButton(text=buttons["dur_30"], callback_data="dur_30")],
        [types.InlineKeyboardButton(text=MESSAGES["buttons"]["back"][lang_code], callback_data="back")]
    ])

def get_comment_keyboard(lang_code):
    send_without_comment_text = MESSAGES["send_without_comment"][lang_code]
    buttons = MESSAGES["buttons"]["comment"]
    return types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text=buttons[lang_code], callback_data="add_comment")],
        [types.InlineKeyboardButton(text=MESSAGES["buttons"]["back"][lang_code], callback_data="back")],
        [types.InlineKeyboardButton(text=send_without_comment_text, callback_data="send_without_comment")]
    ])

# === HANDLERS ===

@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    if message.chat.type != "private":
        bot_info = await bot.get_me()
        builder = InlineKeyboardBuilder()
        msg_text = (
            "🤖 Заполнение формы доступно только в личном чате с ботом.\n\n"
            "🤖 Form submission is only available in a private chat with the bot.\n\n"
            "🤖 表单填写仅限与机器人私聊。"
        )
        builder.button(text="Contact the bot", url=f"https://t.me/{bot_info.username}")
        await message.answer(msg_text, reply_markup=builder.as_markup(), disable_web_page_preview=True)
        return

    keyboard = get_lang_keyboard("ru")
    await message.answer(MESSAGES["start_choose_lang"], reply_markup=keyboard)
    await state.set_state(Form.language)

@dp.callback_query(lambda c: c.data.startswith("lang_"))
async def process_language(callback: types.CallbackQuery, state: FSMContext):
    lang_code = {"lang_ru": "ru", "lang_en": "en", "lang_zh": "zh"}.get(callback.data)
    if not lang_code:
        await callback.answer("Ошибка выбора языка", show_alert=True)
        return
    await state.update_data(language=lang_code)
    await callback.message.edit_text(MESSAGES["lang_selected"][lang_code], reply_markup=get_server_keyboard(lang_code))
    await state.set_state(Form.server_type)
    await callback.answer()

@dp.callback_query(lambda c: c.data.startswith("server_"))
async def process_server_type(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang_code = data.get("language", "en")
    server_map = {
        "server_usd": ("USD", TOPIC_IDS["global"]),
        "server_eud": ("EUD", TOPIC_IDS["global"]),
        "server_rud": ("RUD", TOPIC_IDS["russia_sng"]),
        "server_chd": ("CHD", TOPIC_IDS["china"]),
    }
    server_info = server_map.get(callback.data)
    if not server_info:
        await callback.answer("Ошибка выбора сервера", show_alert=True)
        return
    server_type, topic_id = server_info
    await state.update_data(server_type=server_type, topic_id=topic_id)
    await callback.message.edit_text(MESSAGES["ask_server_version"][lang_code], reply_markup=get_version_keyboard(lang_code))
    await state.set_state(Form.server_version)
    await callback.answer()

@dp.callback_query(lambda c: c.data.startswith("ver_"))
async def process_server_version(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang_code = data.get("language", "en")
    version = {"ver_1272": "1.2.7.2", "ver_1281": "1.2.8.1"}.get(callback.data)
    if not version:
        await callback.answer("Ошибка выбора версии", show_alert=True)
        return
    await state.update_data(server_version=version)
    server_type = data.get("server_type")
    await callback.message.edit_text(MESSAGES["ask_area"][lang_code], reply_markup=get_area_keyboard(lang_code, server_type))
    await state.set_state(Form.area_size)
    await callback.answer()

@dp.callback_query(lambda c: c.data.startswith("area_"))
async def process_area_size(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang_code = data.get("language", "en")
    area_size = callback.data.replace("area_", "")
    await state.update_data(area_size=area_size)
    await callback.message.edit_text(MESSAGES["ask_vr_device"][lang_code], reply_markup=get_vr_keyboard(lang_code))
    await state.set_state(Form.vr_device)
    await callback.answer()

@dp.callback_query(lambda c: c.data.startswith("vr_"))
async def process_vr_device(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang_code = data.get("language", "en")
    vr_map = {
        "vr_quest2": "Meta Quest 2",
        "vr_quest3": "Meta Quest 3/3s",
        "vr_pico4": "Pico 4",
        "vr_pico4ultra": "Pico 4 Ultra/Ultra Enterprise"
    }
    vr_device = vr_map.get(callback.data)
    if not vr_device:
        await callback.answer("Ошибка выбора VR", show_alert=True)
        return
    await state.update_data(vr_device=vr_device)
    await callback.message.edit_text(MESSAGES["ask_partner_contact"][lang_code], reply_markup=get_partner_keyboard(lang_code))
    await state.set_state(Form.partner_contact)
    await callback.answer()

@dp.callback_query(lambda c: c.data == "partner_yes")
async def partner_yes(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang_code = data.get("language", "en")
    await callback.message.edit_text(MESSAGES["ask_partner_name"][lang_code], reply_markup=types.InlineKeyboardMarkup(
        inline_keyboard=[[types.InlineKeyboardButton(text=MESSAGES["buttons"]["back"][lang_code], callback_data="back")]]
    ))
    await state.set_state(Form.partner_name)
    await callback.answer()

@dp.callback_query(lambda c: c.data == "partner_no")
async def partner_no(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(partner_name=None, partner_phone=None, partner_email=None, partner_crm=None)
    data = await state.get_data()
    lang_code = data.get("language", "en")
    await callback.message.edit_text(MESSAGES["ask_city"][lang_code], reply_markup=types.InlineKeyboardMarkup(
        inline_keyboard=[[types.InlineKeyboardButton(text=MESSAGES["buttons"]["back"][lang_code], callback_data="back")]]
    ))
    await state.set_state(Form.city)
    await callback.answer()

@dp.message(Form.partner_name)
async def process_partner_name(message: types.Message, state: FSMContext):
    await state.update_data(partner_name=message.text if message.text.strip() else None)
    data = await state.get_data()
    lang_code = data.get("language", "en")
    await message.answer(MESSAGES["ask_partner_phone"][lang_code], reply_markup=types.InlineKeyboardMarkup(
        inline_keyboard=[[types.InlineKeyboardButton(text=MESSAGES["buttons"]["back"][lang_code], callback_data="back")]]
    ))
    await state.set_state(Form.partner_phone)

@dp.message(Form.partner_phone)
async def process_partner_phone(message: types.Message, state: FSMContext):
    await state.update_data(partner_phone=message.text if message.text.strip() else None)
    data = await state.get_data()
    lang_code = data.get("language", "en")
    await message.answer(MESSAGES["ask_partner_email"][lang_code], reply_markup=types.InlineKeyboardMarkup(
        inline_keyboard=[[types.InlineKeyboardButton(text=MESSAGES["buttons"]["back"][lang_code], callback_data="back")]]
    ))
    await state.set_state(Form.partner_email)

@dp.message(Form.partner_email)
async def process_partner_email(message: types.Message, state: FSMContext):
    await state.update_data(partner_email=message.text if message.text.strip() else None)
    data = await state.get_data()
    lang_code = data.get("language", "en")
    await message.answer(MESSAGES["ask_partner_crm"][lang_code], reply_markup=types.InlineKeyboardMarkup(
        inline_keyboard=[[types.InlineKeyboardButton(text=MESSAGES["buttons"]["back"][lang_code], callback_data="back")]]
    ))
    await state.set_state(Form.partner_crm)

@dp.message(Form.partner_crm)
async def process_partner_crm(message: types.Message, state: FSMContext):
    await state.update_data(partner_crm=message.text if message.text.strip() else None)
    data = await state.get_data()
    lang_code = data.get("language", "en")
    await message.answer(MESSAGES["ask_city"][lang_code], reply_markup=types.InlineKeyboardMarkup(
        inline_keyboard=[[types.InlineKeyboardButton(text=MESSAGES["buttons"]["back"][lang_code], callback_data="back")]]
    ))
    await state.set_state(Form.city)

@dp.message(Form.city)
async def process_city(message: types.Message, state: FSMContext):
    await state.update_data(city=message.text)
    data = await state.get_data()
    lang_code = data.get("language", "en")
    await message.answer(MESSAGES["ask_duration"][lang_code], reply_markup=get_duration_keyboard(lang_code))
    await state.set_state(Form.duration)

@dp.callback_query(lambda c: c.data.startswith("dur_"))
async def process_duration(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang_code = data.get("language", "en")
    duration = {"dur_3": "3", "dur_7": "7", "dur_14": "14", "dur_30": "30"}.get(callback.data)
    if not duration:
        await callback.answer("Ошибка выбора срока", show_alert=True)
        return
    await state.update_data(duration=duration)
    await callback.message.edit_text(MESSAGES["ask_comment"][lang_code], reply_markup=get_comment_keyboard(lang_code))
    await state.set_state(Form.comment)
    await callback.answer()

@dp.callback_query(lambda c: c.data == "add_comment")
async def ask_comment(callback: types.CallbackQuery, state: FSMContext):
    lang_code = (await state.get_data()).get("language", "en")
    await callback.message.edit_text(MESSAGES["enter_comment"][lang_code])
    await state.set_state(Form.comment)
    await callback.answer()

@dp.callback_query(lambda c: c.data == "send_without_comment")
async def send_without_comment(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(comment=None)
    await finalize_request(callback, state)

@dp.message(Form.comment)
async def process_comment(message: types.Message, state: FSMContext):
    await state.update_data(comment=message.text)
    await finalize_request(message, state)

async def finalize_request(event, state: FSMContext):
    data = await state.get_data()
    lang_code = data.get("language", "en")

    user = event.from_user if hasattr(event, 'from_user') else event.message.from_user
    user_id = user.id
    username = user.username
    first_name = user.first_name
    last_name = user.last_name

    server_type = data.get("server_type")
    server_version = data.get("server_version")
    vr_device = data.get("vr_device")
    area_size = data.get("area_size")
    city = data.get("city")
    duration = data.get("duration")
    topic_id = data.get("topic_id")
    comment = data.get("comment")
    partner_name = data.get("partner_name")
    partner_phone = data.get("partner_phone")
    partner_email = data.get("partner_email")
    partner_crm = data.get("partner_crm")

    final_lang = "ru" if lang_code in ["zh", "en"] else lang_code

    fields_to_translate = {
        "city": city,
        "area_size": area_size,
        "partner_name": partner_name,
        "partner_phone": partner_phone,
        "partner_email": partner_email,
        "partner_crm": partner_crm
    }
    translated_fields = {}
    if lang_code in ["zh", "en"] and final_lang == "ru":
        for key, value in fields_to_translate.items():
            if value:
                translated_fields[key] = translate_to_russian(value, lang_code)
            else:
                translated_fields[key] = value
    else:
        translated_fields = fields_to_translate

    partner_lines = []
    if translated_fields["partner_name"]:
        partner_lines.append(f"Контакт (Имя): {translated_fields['partner_name']}")
    if translated_fields["partner_phone"]:
        partner_lines.append(f"Номер телефона: {translated_fields['partner_phone']}")
    if translated_fields["partner_email"]:
        partner_lines.append(f"Email: {translated_fields['partner_email']}")
    if translated_fields["partner_crm"]:
        partner_lines.append(f"Ссылка на CRM: {translated_fields['partner_crm']}")
    
    partner_info = "\n".join(partner_lines) + "\n" if partner_lines else ""

    final_msg = MESSAGES["final_message"][final_lang].format(
        server_type=server_type,
        city=translated_fields["city"],
        area_size=translated_fields["area_size"],
        server_version=server_version,
        vr_device=vr_device,
        duration=duration,
        partner_info=partner_info
    )

    if comment:
        if lang_code in ["zh", "en"] and final_lang == "ru":
            translated_comment = translate_to_russian(comment, lang_code)
            final_msg += f"\n\n💬 Комментарий: {translated_comment}"
        else:
            final_msg += f"\n\n💬 Комментарий: {comment}"

    user_info = f"\n\n👤 Запрос отправлен пользователем: {first_name}"
    if last_name:
        user_info += f" {last_name}"
    if username:
        user_info += f" (@{username})"
    user_info += f" (ID: {user_id})"
    if lang_code == "zh":
        user_info += " (на китайском языке)"
    elif lang_code == "en":
        user_info += " (на английском языке)"

    final_msg += user_info

    sent_message = await bot.send_message(chat_id=MAIN_CHAT_ID, text=final_msg, message_thread_id=topic_id)
    msg_id = sent_message.message_id
    chat_id_short = str(MAIN_CHAT_ID).replace("-100", "")
    link = f"https://t.me/c/{chat_id_short}/{msg_id}?thread={topic_id}"

    if hasattr(event, 'message') and hasattr(event, 'data'):
        await event.message.edit_text(MESSAGES["success_with_link"][lang_code].format(link=link), parse_mode="HTML")
    else:
        await event.answer(MESSAGES["success_with_link"][lang_code].format(link=link), parse_mode="HTML")

    await state.clear()

@dp.callback_query(lambda c: c.data == "back")
async def process_back(callback: types.CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    data = await state.get_data()
    lang_code = data.get("language", "ru")
    server_type = data.get("server_type")

    if current_state == Form.area_size:  # <-- ИСПРАВЛЕНО: состояние существует
        await callback.message.edit_text(MESSAGES["ask_server_version"][lang_code], reply_markup=get_version_keyboard(lang_code))
        await state.set_state(Form.server_version)
    elif current_state == Form.vr_device:
        await callback.message.edit_text(MESSAGES["ask_area"][lang_code], reply_markup=get_area_keyboard(lang_code, server_type))
        await state.set_state(Form.area_size)
    elif current_state == Form.partner_contact:
        await callback.message.edit_text(MESSAGES["ask_vr_device"][lang_code], reply_markup=get_vr_keyboard(lang_code))
        await state.set_state(Form.vr_device)
    elif current_state == Form.partner_name:
        await callback.message.edit_text(MESSAGES["ask_partner_contact"][lang_code], reply_markup=get_partner_keyboard(lang_code))
        await state.set_state(Form.partner_contact)
    elif current_state == Form.partner_phone:
        await callback.message.edit_text(MESSAGES["ask_partner_name"][lang_code], reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[[types.InlineKeyboardButton(text=MESSAGES["buttons"]["back"][lang_code], callback_data="back")]]
        ))
        await state.set_state(Form.partner_name)
    elif current_state == Form.partner_email:
        await callback.message.edit_text(MESSAGES["ask_partner_phone"][lang_code], reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[[types.InlineKeyboardButton(text=MESSAGES["buttons"]["back"][lang_code], callback_data="back")]]
        ))
        await state.set_state(Form.partner_phone)
    elif current_state == Form.partner_crm:
        await callback.message.edit_text(MESSAGES["ask_partner_email"][lang_code], reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[[types.InlineKeyboardButton(text=MESSAGES["buttons"]["back"][lang_code], callback_data="back")]]
        ))
        await state.set_state(Form.partner_email)
    elif current_state == Form.city:
        if data.get("partner_name") is not None:
            await callback.message.edit_text(MESSAGES["ask_partner_crm"][lang_code], reply_markup=types.InlineKeyboardMarkup(
                inline_keyboard=[[types.InlineKeyboardButton(text=MESSAGES["buttons"]["back"][lang_code], callback_data="back")]]
            ))
            await state.set_state(Form.partner_crm)
        else:
            await callback.message.edit_text(MESSAGES["ask_partner_contact"][lang_code], reply_markup=get_partner_keyboard(lang_code))
            await state.set_state(Form.partner_contact)
    elif current_state == Form.duration:
        await callback.message.edit_text(MESSAGES["ask_city"][lang_code], reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[[types.InlineKeyboardButton(text=MESSAGES["buttons"]["back"][lang_code], callback_data="back")]]
        ))
        await state.set_state(Form.city)
    elif current_state == Form.comment:
        await callback.message.edit_text(MESSAGES["ask_duration"][lang_code], reply_markup=get_duration_keyboard(lang_code))
        await state.set_state(Form.duration)
    elif current_state == Form.server_version:
        await callback.message.edit_text(MESSAGES["choose_server"][lang_code], reply_markup=get_server_keyboard(lang_code))
        await state.set_state(Form.server_type)
    elif current_state == Form.server_type:
        await callback.message.edit_text(MESSAGES["start_choose_lang"], reply_markup=get_lang_keyboard(lang_code))
        await state.set_state(Form.language)

    await callback.answer()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())