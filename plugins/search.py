import asyncio
from info import *
from utils import *
from time import time 
from client import User
from pyrogram import Client, filters 
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton 

@Client.on_message(filters.text & filters.group & filters.incoming & ~filters.command(["verify", "connect", "id"]))
async def search(bot, message):
    f_sub = await force_sub(bot, message)
    if f_sub==False:
       return     
    channels = (await get_group(message.chat.id))["channels"]
    if bool(channels)==False:
       return     
    if message.text.startswith("/"):
       return    
    query   = message.text 
    head    = "<b> (User) 👀 𝐎𝐧𝐥𝐢𝐧𝐞 𝐒𝐭𝐫𝐞𝐚𝐦𝐢𝐧𝐠 𝐋𝐢𝐧𝐤 👀</b>\n\n"
    results = ""
    try:
       for channel in channels:
           async for msg in User.search_messages(chat_id=channel, query=query):
               name = (msg.text or msg.caption).split("\n")[0]
               if name in results:
                  continue 
               results += f"<b>🎭 {name}\n👉 {msg.link}</b>\n\n"                                                      
       if bool(results)==False:
          movies = await search_imdb(query)
          buttons = []
          for movie in movies: 
              buttons.append([InlineKeyboardButton(movie['title'], callback_data=f"recheck_{movie['id']}")])
          msg = await message.reply_text(𝐒𝐨𝐫𝐫𝐲 𝐍𝐨 𝐓𝐞𝐫𝐚𝐛𝐨𝐱 𝐋𝐢𝐧𝐤 𝐅𝐨𝐮𝐧𝐝 \n\n𝐆𝐞𝐭 𝐝𝐢𝐫𝐞𝐜𝐭 𝐟𝐢𝐥𝐞 📁\n\n𝐀𝐬𝐤 𝐚𝐠𝐚𝐢𝐧 𝐭𝐡𝐢𝐬 𝐦𝐨𝐯𝐢𝐞 𝐢𝐧 𝐭𝐡𝐢𝐬 👇 𝐠𝐫𝐨𝐮𝐩 𝐮 𝐠𝐞𝐭 𝐅𝐢𝐥𝐞 📁/n here :- https://telegram.me/+wQpK7mlEc_JkNjVl )
       else:
          msg = await message.reply_text(text=head+results, disable_web_page_preview=True)
       _time = (int(time()) + (15*60))
       await save_dlt_message(msg, _time)
    except:
       pass
       


@Client.on_callback_query(filters.regex(r"^recheck"))
async def recheck(bot, update):
    clicked = update.from_user.id
    try:      
       typed = update.message.reply_to_message.from_user.id
    except:
       return await update.message.delete(2)       
    if clicked != typed:
       return await update.answer("That's not for you! 👀", show_alert=True)

    m=await update.message.edit("Searching..💥")
    id      = update.data.split("_")[-1]
    query   = await search_imdb(id)
    channels = (await get_group(update.message.chat.id))["channels"]
    head    = "<u>I Have Searched Movie With Wrong Spelling But Take care next time 👇\n\nPowered By </u> <b><I>@CyniteBackup</I></b>\n\n"
    results = ""
    try:
       for channel in channels:
           async for msg in User.search_messages(chat_id=channel, query=query):
               name = (msg.text or msg.caption).split("\n")[0]
               if name in results:
                  continue 
               results += f"<b><I>🎭 {name}</I></b>\n\n👉 {msg.link}</I></b>\n\n"
       if bool(results)==False:          
          return await update.message.edit( "👀 𝐒𝐨𝐫𝐫𝐲 𝐍𝐨 𝐓𝐞𝐫𝐚𝐛𝐨𝐱 𝐋𝐢𝐧𝐤 𝐅𝐨𝐮𝐧𝐝 😔\n\n𝐆𝐞𝐭 𝐝𝐢𝐫𝐞𝐜𝐭 𝐟𝐢𝐥𝐞 📁\n\n𝐀𝐬𝐤 𝐚𝐠𝐚𝐢𝐧 𝐭𝐡𝐢𝐬 𝐦𝐨𝐯𝐢𝐞 𝐢𝐧 𝐭𝐡𝐢𝐬 👇 𝐠𝐫𝐨𝐮𝐩 𝐮 𝐠𝐞𝐭 𝐅𝐢𝐥𝐞 📁/n📤 here :- https://telegram.me/+wQpK7mlEc_JkNjVl)", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(" Ask here 📤 To Get File", url=f"https://t.me/+wQpK7mlEc_JkNjVl")]]))
       await update.message.edit(text=head+results, disable_web_page_preview=True)
    except Exception as e:
       await update.message.edit(f"❌ Error: `{e}`")
       await update.message.delete(20)
                                   

@Client.on_callback_query(filters.regex(r"^request"))
async def request(bot, update):
    clicked = update.from_user.id
    try:      
       typed = update.message.reply_to_message.from_user.id
    except:
       return await update.message.delete()       
    if clicked != typed:
       return await update.answer("That's not for you! 👀", show_alert=True)

    admin = (await get_group(update.message.chat.id))["user_id"]
    id    = update.data.split("_")[1]
    name  = await search_imdb(id)
    url   = "https://www.imdb.com/title/tt"+id
    text  = f"#RequestFromYourGroup\n\nName: {name}\nIMDb: {url}"
    await bot.send_message(chat_id=admin, text=text, disable_web_page_preview=True)
    await update.answer("✅ Request Sent To Admin", show_alert=True)
    await update.message.delete(60)
