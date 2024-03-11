from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from pyrogram.types import Message
from bs4 import BeautifulSoup
import requests
import asyncio
import os
import json
from flask_app import keep_alive
from book_1 import books_name_link
from data import read, write
from buttons_generator import button_generater_func
from text_for_bot import start_the_bot, the_user_helper, how_it_works,about_the_bot , skip_ads, suggestions, the_bots
from buttoms_replay import buttoms_replay, pages, how_to_skip_ads
from books import books_
from short_link import short_link_opration

# تجهيز قاعده البيانات لاضافع ال id 
db_path = 'db.json'
if os.path.exists(db_path):
    pass
else:
    write(db_path, [])
data = read(db_path)

bot_token="6766334553:AAFPsgblPVz0Esm_Ft4SRYqgNvlhuL2tVl4"
#معلومات و التعريف عن البوت
bot_pyrogram = Client(
    name='Bot',
    api_hash="db93b5d1b9cc15b7b8512a7082a99692",
    api_id=29817603,
    bot_token=bot_token
)
#مولد لنكات الصفحات
async def link_buttom_for_accounts(msg, link, app_name):
        
    k = InlineKeyboardMarkup([[InlineKeyboardButton(f"RANDOMS",url=f"{link}")]])
    await msg.reply_text(f"شاهد كل جديد على {app_name}",reply_markup=k,disable_web_page_preview=True)		


#########################################################
#########################################################

#اوامر المستخدم معرفه عدد المستخدمين
@bot_pyrogram.on_message(filters.command('users_num'))
async def on_owner_command(bot:Client, msg:Message):

    #اليوسر ايد الخاص بالمرسل
    user_id = msg.from_user.id

    if user_id == 5497992601 :
        users_count = len(data)
        await msg.reply(users_count)

# معرفه id المستخدمين اوامر المستخدم
@bot_pyrogram.on_message(filters.command('users_id'))
async def on_owner_command(bot:Client, msg:Message):

    #اليوسر ايد الخاص بالمرسل
    user_id = msg.from_user.id

    if user_id == 5497992601 :
        for i in data:
            await msg.reply(i)

#اوامر المستخدم معرفه معلومات حول مستخدم واحد فقط
@bot_pyrogram.on_message(filters.command('user'))
async def on_owner_command(bot:Client, msg:Message):

    #اليوسر ايد الخاص بالمرسل
    user_id = msg.from_user.id

    if user_id == 5497992601 :
        try:
            id = msg.text
            name = id.split(None, 1)[1]
            info = await bot.get_chat(int(name))
            await msg.reply(info)
        except:
            await msg.reply('اختر ال id الذي تود البحث عنه')

#اوامر المستخدم ارسال نص لكل مستخدمين البوت
@bot_pyrogram.on_message(filters.command('user_bc'))
async def on_owner_command(bot:Client, msg:Message):

    #اليوسر ايد الخاص بالمرسل
    user_id = msg.from_user.id

    if user_id == 5497992601 :
        try:
            id = msg.text
            text_to_send = id.split(None, 1)[1]
            for i in data:
                    await bot.send_message(i, text_to_send)
        except:
            await msg.reply("يوجد مشكله بارسال الرسائل لجميع المستخدمين او يجب ان تكتب الرساله التي تود ارسالها للمستخدمين")

# ارسال ملف يحتوي على الid الخاص بكل المستخدمين 
@bot_pyrogram.on_message(filters.command('users_file'))
async def on_owner_command(bot:Client, msg:Message):

    #اليوسر ايد الخاص بالمرسل
    user_id = msg.from_user.id

    if user_id == 5497992601 :
        await bot.send_document(user_id, 'db.json')

# help, uh, user_help اوامر المستخدم
@bot_pyrogram.on_message(filters.command(['help', 'user_help', 'uh']))
async def on_owner_command(bot:Client, msg:Message):

    #اليوسر ايد الخاص بالمرسل
    user_id = msg.from_user.id

    if user_id == 5497992601 :
        text = the_user_helper()
        await msg.reply(text)

#########################################################
#########################################################

#  بدايه البوت و الامر  'start'
@bot_pyrogram.on_message(filters.command('start'))
async def start(bot:Client, msg:Message):
    #اليوسر ايد الخاص بالمرسل
    user_id = msg.from_user.id

    #حفظ id المستخدم فقط اذا ضغط ستارت start 
    if user_id not in data:
        data.append(user_id)
        write(db_path, data)
    
    # يوزر القناة بدون @
    ch = "RANDOMS_CH" 
    # المستخدم من اجل التاكد من اشتراكه في البوت  id استخراج
    # توكن البوت - ورفعه مشرف بالقناه 
    token = bot_token
    url = f"https://api.telegram.org/bot{token}/getchatmember?chat_id=@{ch}&user_id={user_id}"

    req = requests.get(url)
    
    #اذا اليوسر مشترك بالقناه
    if user_id == ch or 'member' in req.text or 'creator' in req.text or 'administartor' in req.text:


        #الرد بالازرار
        buttoms = buttoms_replay()
        replay_markup = ReplyKeyboardMarkup(buttoms, one_time_keyboard= True, resize_keyboard=True)

        text = start_the_bot()

        # ارسال الرساله الترحيبيه
        await bot.send_message(user_id, text, reply_markup=replay_markup)

    else:
        ch = "RANDOMS_CH" # يوزر القناة بدون @ 
        k = InlineKeyboardMarkup([[InlineKeyboardButton(f"RANDOMS_CH",url=f"t.me/{ch}")]])
        await msg.reply_text(f"""**عذرا عزيزي - {msg.from_user.first_name}  عليك الاشتراك في قناة**""",reply_markup=k,disable_web_page_preview=True)		

#صفحات مواقع التواصل الاجتماعي
@bot_pyrogram.on_message(filters.regex('صفحاتنا'))
async def pages_(bot:Client, msg):
    #اليوسر ايد الخاص بالمرسل
    user_id = msg.from_user.id

    #حفظ id المستخدم فقط اذا ضغط ستارت start 
    if user_id not in data:
        data.append(user_id)
        write(db_path, data)

    # يوزر القناة بدون @
    ch = "RANDOMS_CH" 
    # المستخدم من اجل التاكد من اشتراكه في البوت  id استخراج
    # توكن البوت - ورفعه مشرف بالقناه 
    token = bot_token
    url = f"https://api.telegram.org/bot{token}/getchatmember?chat_id=@{ch}&user_id={user_id}"
    req =  requests.get(url)

    #اذا اليوسر مشترك بالقناه
    if user_id == ch or 'member' in req.text or 'creator' in req.text or 'administartor' in req.text:
        #الرد بالازرار
        buttoms = pages()
        replay_markup = ReplyKeyboardMarkup(buttoms, one_time_keyboard= True, resize_keyboard=True)

        # ارسال الرساله الترحيبيه
        await bot.send_message(user_id, "تابعنا على وسائل التواصل الاجتماعي", reply_markup=replay_markup)

    else:
        ch = "RANDOMS_CH" # يوزر القناة بدون @ 
        k = InlineKeyboardMarkup([[InlineKeyboardButton(f"RANDOMS_CH",url=f"t.me/{ch}")]])
        await msg.reply_text(f"""**عذرا عزيزي - {msg.from_user.first_name}  عليك الاشتراك في قناة**""",reply_markup=k,disable_web_page_preview=True)		

#شرح كيف يعمل البوت
@bot_pyrogram.on_message(filters.regex("كيف يعمل البوت"))
async def pages_(bot:Client, msg):
    #اليوسر ايد الخاص بالمرسل
    user_id = msg.from_user.id

    #حفظ id المستخدم فقط اذا ضغط ستارت start 
    if user_id not in data:
        data.append(user_id)
        write(db_path, data)


    # يوزر القناة بدون @
    ch = "RANDOMS_CH" 
    # المستخدم من اجل التاكد من اشتراكه في البوت  id استخراج
    # توكن البوت - ورفعه مشرف بالقناه 
    token = bot_token
    url = f"https://api.telegram.org/bot{token}/getchatmember?chat_id=@{ch}&user_id={user_id}"
    req =  requests.get(url)

    #اذا اليوسر مشترك بالقناه
    if user_id == ch or 'member' in req.text or 'creator' in req.text or 'administartor' in req.text:
        # ارسال الرساله الترحيبيه
        await bot.send_message(user_id, how_it_works())

    else:
        ch = "RANDOMS_CH" # يوزر القناة بدون @ 
        k = InlineKeyboardMarkup([[InlineKeyboardButton(f"RANDOMS_CH",url=f"t.me/{ch}")]])
        await msg.reply_text(f"""**عذرا عزيزي - {msg.from_user.first_name}  عليك الاشتراك في قناة**""",reply_markup=k,disable_web_page_preview=True)		

#للتواصل معي بخصوص البوت
@bot_pyrogram.on_message(filters.regex('لاي اقتراحات'))
async def pages_(bot:Client, msg:Message):
    #اليوسر ايد الخاص بالمرسل
    user_id = msg.from_user.id

    #حفظ id المستخدم فقط اذا ضغط ستارت start 
    if user_id not in data:
        data.append(user_id)
        write(db_path, data)

        # يوزر القناة بدون @
    ch = "RANDOMS_CH" 
    # المستخدم من اجل التاكد من اشتراكه في البوت  id استخراج
    # توكن البوت - ورفعه مشرف بالقناه 
    token = bot_token
    url = f"https://api.telegram.org/bot{token}/getchatmember?chat_id=@{ch}&user_id={user_id}"
    req =  requests.get(url)

    #اذا اليوسر مشترك بالقناه
    if user_id == ch or 'member' in req.text or 'creator' in req.text or 'administartor' in req.text:
        # ارسال الرساله الترحيبيه

        k = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(f"TELEGRAM",url=f"https://t.me/ahmad0alhelo")
                ],
                [
                    InlineKeyboardButton(f"INSTAGRAM",url=f"https://www.instagram.com/ahmad.alhelok/?hl=ar")
                ],
                [
                    InlineKeyboardButton(f'FACEBOOK', url='https://www.facebook.com/ahmad.alhel0')
                ]
            ]
            )

        await msg.reply_text(suggestions(),reply_markup=k,disable_web_page_preview=True)		


    else:
        ch = "RANDOMS_CH" # يوزر القناة بدون @ 
        k = InlineKeyboardMarkup([[InlineKeyboardButton(f"RANDOMS_CH",url=f"t.me/{ch}")]])
        await msg.reply_text(f"""**عذرا عزيزي - {msg.from_user.first_name}  عليك الاشتراك في قناة**""",reply_markup=k,disable_web_page_preview=True)		

#بوتاتنا
@bot_pyrogram.on_message(filters.regex('بوتاتنا'))
async def pages_(bot:Client, msg:Message):
    #اليوسر ايد الخاص بالمرسل
    user_id = msg.from_user.id

    #حفظ id المستخدم فقط اذا ضغط ستارت start 
    if user_id not in data:
        data.append(user_id)
        write(db_path, data)

    # يوزر القناة بدون @
    ch = "RANDOMS_CH" 
    # المستخدم من اجل التاكد من اشتراكه في البوت  id استخراج
    # توكن البوت - ورفعه مشرف بالقناه 
    token = bot_token
    url = f"https://api.telegram.org/bot{token}/getchatmember?chat_id=@{ch}&user_id={user_id}"
    req =  requests.get(url)

    #اذا اليوسر مشترك بالقناه
    if user_id == ch or 'member' in req.text or 'creator' in req.text or 'administartor' in req.text:

        k = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(f"RANDOMS_pc",url=f"https://t.me/RANDOMS1_bot")
                ]
            ]
            )
        # ارسال الرساله 
        await bot.send_message(user_id, the_bots(), reply_markup=k, disable_web_page_preview=True)

    else:
        ch = "RANDOMS_CH" # يوزر القناة بدون @ 
        k = InlineKeyboardMarkup([[InlineKeyboardButton(f"RANDOMS_CH",url=f"t.me/{ch}")]])
        await msg.reply_text(f"""**عذرا عزيزي - {msg.from_user.first_name}  عليك الاشتراك في قناة**""",reply_markup=k,disable_web_page_preview=True)		

@bot_pyrogram.on_message(filters.regex('حول البوت'))
async def pages_(bot:Client, msg:Message):
    #اليوسر ايد الخاص بالمرسل
    user_id = msg.from_user.id

    #حفظ id المستخدم فقط اذا ضغط ستارت start 
    if user_id not in data:
        data.append(user_id)
        write(db_path, data)

        # يوزر القناة بدون @
    ch = "RANDOMS_CH" 
    # المستخدم من اجل التاكد من اشتراكه في البوت  id استخراج
    # توكن البوت - ورفعه مشرف بالقناه 
    token = bot_token
    url = f"https://api.telegram.org/bot{token}/getchatmember?chat_id=@{ch}&user_id={user_id}"
    req =  requests.get(url)

    #اذا اليوسر مشترك بالقناه
    if user_id == ch or 'member' in req.text or 'creator' in req.text or 'administartor' in req.text:
        # ارسال الرساله الترحيبيه

        k = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(f"TELEGRAM",url=f"https://t.me/ahmad0alhelo")
                ],
                [
                    InlineKeyboardButton(f"INSTAGRAM",url=f"https://www.instagram.com/ahmad.alhelok/?hl=ar")
                ],
                [
                    InlineKeyboardButton(f'FACEBOOK', url='https://www.facebook.com/ahmad.alhel0')
                ]
            ]
            )

        await msg.reply_text(about_the_bot(),reply_markup=k,disable_web_page_preview=True)		


    else:
        ch = "RANDOMS_CH" # يوزر القناة بدون @ 
        k = InlineKeyboardMarkup([[InlineKeyboardButton(f"RANDOMS_CH",url=f"t.me/{ch}")]])
        await msg.reply_text(f"""**عذرا عزيزي - {msg.from_user.first_name}  عليك الاشتراك في قناة**""",reply_markup=k,disable_web_page_preview=True)		

#'اشهر الكتب'
@bot_pyrogram.on_message(filters.regex('اشهر الكتب'))
async def pages_(bot:Client, msg):
    #اليوسر ايد الخاص بالمرسل
    user_id = msg.from_user.id

    #حفظ id المستخدم فقط اذا ضغط ستارت start 
    if user_id not in data:
        data.append(user_id)
        write(db_path, data)

    # يوزر القناة بدون @
    ch = "RANDOMS_CH" 
    # المستخدم من اجل التاكد من اشتراكه في البوت  id استخراج
    # توكن البوت - ورفعه مشرف بالقناه 
    token = bot_token
    url = f"https://api.telegram.org/bot{token}/getchatmember?chat_id=@{ch}&user_id={user_id}"
    req =  requests.get(url)

    #اذا اليوسر مشترك بالقناه
    if user_id == ch or 'member' in req.text or 'creator' in req.text or 'administartor' in req.text:

        q = books_()

        short_links = []
        for i in q['book_link_list']:

            d = short_link_opration(i)
            short_links.append(d)


        await button_generater_func(q['book_name_list'],"يتم العمل على هذا القسم", short_links, InlineKeyboardButton, InlineKeyboardMarkup, msg)

    else:
        ch = "RANDOMS_CH" # يوزر القناة بدون @ 
        k = InlineKeyboardMarkup([[InlineKeyboardButton(f"RANDOMS_CH",url=f"t.me/{ch}")]])
        await msg.reply_text(f"""**عذرا عزيزي - {msg.from_user.first_name}  عليك الاشتراك في قناة**""",reply_markup=k,disable_web_page_preview=True)		

#لتخطي الاعلانات
@bot_pyrogram.on_message(filters.regex('كيف تتخطى الاعلانات'))
async def pages_(bot:Client, msg):
    #اليوسر ايد الخاص بالمرسل
    user_id = msg.from_user.id

    #حفظ id المستخدم فقط اذا ضغط ستارت start 
    if user_id not in data:
        data.append(user_id)
        write(db_path, data)

    # يوزر القناة بدون @
    ch = "RANDOMS_CH" 
    # المستخدم من اجل التاكد من اشتراكه في البوت  id استخراج
    # توكن البوت - ورفعه مشرف بالقناه 
    token = bot_token
    url = f"https://api.telegram.org/bot{token}/getchatmember?chat_id=@{ch}&user_id={user_id}"
    req =  requests.get(url)

    #اذا اليوسر مشترك بالقناه
    if user_id == ch or 'member' in req.text or 'creator' in req.text or 'administartor' in req.text:
        #الرد بالازرار
        buttoms = how_to_skip_ads()
        replay_markup = ReplyKeyboardMarkup(buttoms, one_time_keyboard= True, resize_keyboard=True)

        #الرساله
        message = skip_ads()

        # ارسال الرساله 
        await bot.send_message(user_id, message, reply_markup=replay_markup)

    else:
        ch = "RANDOMS_CH" # يوزر القناة بدون @ 
        k = InlineKeyboardMarkup([[InlineKeyboardButton(f"RANDOMS_CH",url=f"t.me/{ch}")]])
        await msg.reply_text(f"""**عذرا عزيزي - {msg.from_user.first_name}  عليك الاشتراك في قناة**""",reply_markup=k,disable_web_page_preview=True)		

#ارسال مقطع اختصار الروابط windos
@bot_pyrogram.on_message(filters.regex('تخطي الاعلانات windows'))
async def skip_ad_windos(bot:Client, msg:Message):
    #اليوسر ايد الخاص بالمرسل
    user_id = msg.from_user.id

    # يوزر القناة بدون @
    ch = "RANDOMS_CH" 
    # المستخدم من اجل التاكد من اشتراكه في البوت  id استخراج
    # توكن البوت - ورفعه مشرف بالقناه 
    token = bot_token
    url = f"https://api.telegram.org/bot{token}/getchatmember?chat_id=@{ch}&user_id={user_id}"
    req =  requests.get(url)

    #اذا اليوسر مشترك بالقناه
    if user_id == ch or 'member' in req.text or 'creator' in req.text or 'administartor' in req.text:
        
        try:
            #رابط الفيديو
            vidio_dir = "https://res.cloudinary.com/dfcge5cyk/video/upload/v1710154370/randoms/RANDOMS_book/gexr0nuapahdirv9qvhm.mp4"
            #ارسال الفيديو
            await bot.send_video(user_id, vidio_dir)
        except:
            text  = 'يوجد مشكله بارسال الفيديو'
            await bot.send_message(user_id, text)
    else:
        ch = "RANDOMS_CH" # يوزر القناة بدون @ 
        k = InlineKeyboardMarkup([[InlineKeyboardButton(f"RANDOMS_CH",url=f"t.me/{ch}")]])
        await msg.reply_text(f"""**عذرا عزيزي - {msg.from_user.first_name}  عليك الاشتراك في قناة**""",reply_markup=k,disable_web_page_preview=True)		


#ارسال مقطع اختصار الروابط ios
@bot_pyrogram.on_message(filters.regex('تخطي الاعلانات لاجهزه ios'))
async def skip_ad_windos(bot:Client, msg:Message):
    #اليوسر ايد الخاص بالمرسل
    user_id = msg.from_user.id

    # يوزر القناة بدون @
    ch = "RANDOMS_CH" 
    # المستخدم من اجل التاكد من اشتراكه في البوت  id استخراج
    # توكن البوت - ورفعه مشرف بالقناه 
    token = bot_token
    url = f"https://api.telegram.org/bot{token}/getchatmember?chat_id=@{ch}&user_id={user_id}"
    req =  requests.get(url)

    #اذا اليوسر مشترك بالقناه
    if user_id == ch or 'member' in req.text or 'creator' in req.text or 'administartor' in req.text:

        try:
            #رابط الفيديو
            vidio_dir = "https://res.cloudinary.com/dfcge5cyk/video/upload/v1710166943/randoms/RANDOMS_book/y9tfwawsgpzefdifgkzz.mp4"
            #ارسال الفيديو
            await bot.send_video(user_id, vidio_dir)
        except:
            text  = 'يوجد مشكله بارسال الفيديو'
            await bot.send_message(user_id, text)

    else:
        ch = "RANDOMS_CH" # يوزر القناة بدون @ 
        k = InlineKeyboardMarkup([[InlineKeyboardButton(f"RANDOMS_CH",url=f"t.me/{ch}")]])
        await msg.reply_text(f"""**عذرا عزيزي - {msg.from_user.first_name}  عليك الاشتراك في قناة**""",reply_markup=k,disable_web_page_preview=True)		

#ارسال مقطع اختصار الروابط android
@bot_pyrogram.on_message(filters.regex('تخطي الاعلانات لاجهزه android'))
async def skip_ad_windos(bot:Client, msg:Message):
    #اليوسر ايد الخاص بالمرسل
    user_id = msg.from_user.id

    # يوزر القناة بدون @
    ch = "RANDOMS_CH" 
    # المستخدم من اجل التاكد من اشتراكه في البوت  id استخراج
    # توكن البوت - ورفعه مشرف بالقناه 
    token = bot_token
    url = f"https://api.telegram.org/bot{token}/getchatmember?chat_id=@{ch}&user_id={user_id}"
    req =  requests.get(url)

    #اذا اليوسر مشترك بالقناه
    if user_id == ch or 'member' in req.text or 'creator' in req.text or 'administartor' in req.text:

        try:
            #رابط الفيديو
            vidio_dir = "https://res.cloudinary.com/dfcge5cyk/video/upload/v1710157151/randoms/RANDOMS_book/pvrop1nhfhozeuhe4iak.mp4"
            #ارسال الفيديو
            await bot.send_video(user_id, vidio_dir)
        except:
            text  = 'يوجد مشكله بارسال الفيديو'
            await bot.send_message(user_id, text)

    else:
        ch = "RANDOMS_CH" # يوزر القناة بدون @ 
        k = InlineKeyboardMarkup([[InlineKeyboardButton(f"RANDOMS_CH",url=f"t.me/{ch}")]])
        await msg.reply_text(f"""**عذرا عزيزي - {msg.from_user.first_name}  عليك الاشتراك في قناة**""",reply_markup=k,disable_web_page_preview=True)		

# ==================================
#الصفحات

@bot_pyrogram.on_message(filters.regex("YOUTUBE"))
async def pages_(bot:Client, msg):
    #اليوسر ايد الخاص بالمرسل
    user_id = msg.from_user.id


    # يوزر القناة بدون @
    ch = "RANDOMS_CH" 
    # المستخدم من اجل التاكد من اشتراكه في البوت  id استخراج
    # توكن البوت - ورفعه مشرف بالقناه 
    token = bot_token
    url = f"https://api.telegram.org/bot{token}/getchatmember?chat_id=@{ch}&user_id={user_id}"
    req =  requests.get(url)

    #اذا اليوسر مشترك بالقناه
    if user_id == ch or 'member' in req.text or 'creator' in req.text or 'administartor' in req.text:
        # ارسال الرساله الترحيبيه
        link = 'https://www.youtube.com/channel/UCFtDm5Bdq2KZdWCkmHPiBYw'
        app_name = 'YOUTUBE'
        await link_buttom_for_accounts(msg, link, app_name)

    else:
        ch = "RANDOMS_CH" # يوزر القناة بدون @ 
        k = InlineKeyboardMarkup([[InlineKeyboardButton(f"RANDOMS_CH",url=f"t.me/{ch}")]])
        await msg.reply_text(f"""**عذرا عزيزي - {msg.from_user.first_name}  عليك الاشتراك في قناة**""",reply_markup=k,disable_web_page_preview=True)		

@bot_pyrogram.on_message(filters.regex("FACEBOOK"))
async def pages_(bot:Client, msg):
    #اليوسر ايد الخاص بالمرسل
    user_id = msg.from_user.id


    # يوزر القناة بدون @
    ch = "RANDOMS_CH" 
    # المستخدم من اجل التاكد من اشتراكه في البوت  id استخراج
    # توكن البوت - ورفعه مشرف بالقناه 
    token = bot_token
    url = f"https://api.telegram.org/bot{token}/getchatmember?chat_id=@{ch}&user_id={user_id}"
    req =  requests.get(url)

    #اذا اليوسر مشترك بالقناه
    if user_id == ch or 'member' in req.text or 'creator' in req.text or 'administartor' in req.text:
        # ارسال الرساله الترحيبيه
        link = 'https://www.facebook.com/profile.php?id=61556736453822'
        app_name = 'FACEBOOK'
        await link_buttom_for_accounts(msg, link, app_name)

    else:
        ch = "RANDOMS_CH" # يوزر القناة بدون @ 
        k = InlineKeyboardMarkup([[InlineKeyboardButton(f"RANDOMS_CH",url=f"t.me/{ch}")]])
        await msg.reply_text(f"""**عذرا عزيزي - {msg.from_user.first_name}  عليك الاشتراك في قناة**""",reply_markup=k,disable_web_page_preview=True)		

@bot_pyrogram.on_message(filters.regex("INSTAGRAM"))
async def pages_(bot:Client, msg):
    #اليوسر ايد الخاص بالمرسل
    user_id = msg.from_user.id


    # يوزر القناة بدون @
    ch = "RANDOMS_CH" 
    # المستخدم من اجل التاكد من اشتراكه في البوت  id استخراج
    # توكن البوت - ورفعه مشرف بالقناه 
    token = bot_token
    url = f"https://api.telegram.org/bot{token}/getchatmember?chat_id=@{ch}&user_id={user_id}"
    req =  requests.get(url)

    #اذا اليوسر مشترك بالقناه
    if user_id == ch or 'member' in req.text or 'creator' in req.text or 'administartor' in req.text:
        # ارسال الرساله الترحيبيه
        link = 'https://www.instagram.com/_a_randoms_/'
        app_name = 'INSTAGRAM'
        await link_buttom_for_accounts(msg, link, app_name)

    else:
        ch = "RANDOMS_CH" # يوزر القناة بدون @ 
        k = InlineKeyboardMarkup([[InlineKeyboardButton(f"RANDOMS_CH",url=f"t.me/{ch}")]])
        await msg.reply_text(f"""**عذرا عزيزي - {msg.from_user.first_name}  عليك الاشتراك في قناة**""",reply_markup=k,disable_web_page_preview=True)		

@bot_pyrogram.on_message(filters.regex("TIK TOK"))
async def pages_(bot:Client, msg):
    #اليوسر ايد الخاص بالمرسل
    user_id = msg.from_user.id


    # يوزر القناة بدون @
    ch = "RANDOMS_CH" 
    # المستخدم من اجل التاكد من اشتراكه في البوت  id استخراج
    # توكن البوت - ورفعه مشرف بالقناه 
    token = bot_token
    url = f"https://api.telegram.org/bot{token}/getchatmember?chat_id=@{ch}&user_id={user_id}"
    req =  requests.get(url)

    #اذا اليوسر مشترك بالقناه
    if user_id == ch or 'member' in req.text or 'creator' in req.text or 'administartor' in req.text:
        # ارسال الرساله الترحيبيه
        link = 'https://www.tiktok.com/@_randoms_a_'
        app_name = 'TIK TOK'
        await link_buttom_for_accounts(msg, link, app_name)

    else:
        ch = "RANDOMS_CH" # يوزر القناة بدون @ 
        k = InlineKeyboardMarkup([[InlineKeyboardButton(f"RANDOMS_CH",url=f"t.me/{ch}")]])
        await msg.reply_text(f"""**عذرا عزيزي - {msg.from_user.first_name}  عليك الاشتراك في قناة**""",reply_markup=k,disable_web_page_preview=True)		

@bot_pyrogram.on_message(filters.regex("TELEGRAM"))
async def pages_(bot:Client, msg):
    #اليوسر ايد الخاص بالمرسل
    user_id = msg.from_user.id


    # يوزر القناة بدون @
    ch = "RANDOMS_CH" 
    # المستخدم من اجل التاكد من اشتراكه في البوت  id استخراج
    # توكن البوت - ورفعه مشرف بالقناه 
    token = bot_token
    url = f"https://api.telegram.org/bot{token}/getchatmember?chat_id=@{ch}&user_id={user_id}"
    req =  requests.get(url)

    #اذا اليوسر مشترك بالقناه
    if user_id == ch or 'member' in req.text or 'creator' in req.text or 'administartor' in req.text:
        # ارسال الرساله الترحيبيه
        link = 't.me/RANDOMS_CH'
        app_name = 'TELEGRAM'
        await link_buttom_for_accounts(msg, link, app_name)

    else:
        ch = "RANDOMS_CH" # يوزر القناة بدون @ 
        k = InlineKeyboardMarkup([[InlineKeyboardButton(f"RANDOMS_CH",url=f"t.me/{ch}")]])
        await msg.reply_text(f"""**عذرا عزيزي - {msg.from_user.first_name}  عليك الاشتراك في قناة**""",reply_markup=k,disable_web_page_preview=True)		

@bot_pyrogram.on_message(filters.regex("BIGO LIVE"))
async def pages_(bot:Client, msg):
    #اليوسر ايد الخاص بالمرسل
    user_id = msg.from_user.id


    # يوزر القناة بدون @
    ch = "RANDOMS_CH" 
    # المستخدم من اجل التاكد من اشتراكه في البوت  id استخراج
    # توكن البوت - ورفعه مشرف بالقناه 
    token = bot_token
    url = f"https://api.telegram.org/bot{token}/getchatmember?chat_id=@{ch}&user_id={user_id}"
    req =  requests.get(url)

    #اذا اليوسر مشترك بالقناه
    if user_id == ch or 'member' in req.text or 'creator' in req.text or 'administartor' in req.text:
        # ارسال الرساله الترحيبيه
        link = 'https://www.bigo.tv/user/985447292'
        app_name = 'BIGO LIVE'
        await link_buttom_for_accounts(msg, link, app_name)

    else:
        ch = "RANDOMS_CH" # يوزر القناة بدون @ 
        k = InlineKeyboardMarkup([[InlineKeyboardButton(f"RANDOMS_CH",url=f"t.me/{ch}")]])
        await msg.reply_text(f"""**عذرا عزيزي - {msg.from_user.first_name}  عليك الاشتراك في قناة**""",reply_markup=k,disable_web_page_preview=True)		

# ====================================
#للعوده للصفحه الرئيسيه للبوت
@bot_pyrogram.on_message(filters.regex('<<عوده'))
async def pages_(bot:Client, msg):
    #اليوسر ايد الخاص بالمرسل
    user_id = msg.from_user.id

    #حفظ id المستخدم فقط اذا ضغط ستارت start 
    if user_id not in data:
        data.append(user_id)
        write(db_path, data)

        # يوزر القناة بدون @
    ch = "RANDOMS_CH" 
    # المستخدم من اجل التاكد من اشتراكه في البوت  id استخراج
    # توكن البوت - ورفعه مشرف بالقناه 
    token = bot_token
    url = f"https://api.telegram.org/bot{token}/getchatmember?chat_id=@{ch}&user_id={user_id}"
    req =  requests.get(url)

    #اذا اليوسر مشترك بالقناه
    if user_id == ch or 'member' in req.text or 'creator' in req.text or 'administartor' in req.text:
        #الرد بالازرار
        buttoms = buttoms_replay()
        replay_markup = ReplyKeyboardMarkup(buttoms, one_time_keyboard= True, resize_keyboard=True)

        # ارسال الرساله الترحيبيه
        await bot.send_message(user_id, 'عدنا', reply_markup=replay_markup)

    else:
        ch = "RANDOMS_CH" # يوزر القناة بدون @ 
        k = InlineKeyboardMarkup([[InlineKeyboardButton(f"RANDOMS_CH",url=f"t.me/{ch}")]])
        await msg.reply_text(f"""**عذرا عزيزي - {msg.from_user.first_name}  عليك الاشتراك في قناة**""",reply_markup=k,disable_web_page_preview=True)		


@bot_pyrogram.on_message(filters.command('b'))
async def book(bot:Client, msg:Message):

    user_id = msg.from_user.id

    name_row = msg.text

    #حفظ id المستخدم فقط اذا ضغط ستارت start 
    if user_id not in data:
        data.append(user_id)
        write(db_path, data)

    # يوزر القناة بدون @
    ch = "RANDOMS_CH" 
    # المستخدم من اجل التاكد من اشتراكه في البوت  id استخراج
    # توكن البوت - ورفعه مشرف بالقناه 
    token = bot_token
    url = f"https://api.telegram.org/bot{token}/getchatmember?chat_id=@{ch}&user_id={user_id}"

    req = requests.get(url)
    
    #اذا اليوسر مشترك بالقناه
    if user_id == ch or 'member' in req.text or 'creator' in req.text or 'administartor' in req.text:

        try:
            a = name_row.split(None, 1)[1]
            d = a.split()
            f = '+'.join(d)

            msg_from_bot = await bot.send_message(user_id, "...تتم المعالجه")

            try:
                q = books_name_link(f)

                short_links = []
                for i in q['books_links_']:

                    d = short_link_opration(i)
                    short_links.append(d)

                await msg_from_bot.delete()
                await button_generater_func(q['books_name_list'],None , short_links, InlineKeyboardButton, InlineKeyboardMarkup, msg)
            except:
                await msg_from_bot.delete()
                await bot.send_message ( user_id, 'الكتاب غير موجود' )
        except:
            await bot.send_message(user_id, 'اكتب اسم الكتاب')

    else:
        ch = "RANDOMS_CH" # يوزر القناة بدون @ 
        k = InlineKeyboardMarkup([[InlineKeyboardButton(f"RANDOMS_CH",url=f"t.me/{ch}")]])
        await msg.reply_text(f"""**عذرا عزيزي - {msg.from_user.first_name}  عليك الاشتراك في قناة**""",reply_markup=k,disable_web_page_preview=True)		



if __name__ == '__main__':
    keep_alive()
    bot_pyrogram.run()

else:
    print('the bot is not work :(')
