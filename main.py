from defs import getUrl, getcards, phone
from pyrogram import Client, filters
from pyrogram.types import Message
import asyncio
import os, sys
import re
import requests
from datetime import datetime
import pytz
from config import API_ID, API_HASH, SESSION, SEND_ID


app = Client(
     name='NormalScrap',
     api_id=API_ID,
     api_hash=API_HASH,
     session_string=str(SESSION),
     in_memory=True,
)

ccs = []

with open('cards.txt', 'r') as r:
    temp_cards = r.read().splitlines()

for x in temp_cards:
    car = getcards(x)
    if car:
        ccs.append(car[0])
    else:
        continue


@app.on_message(filters.text)
async def my_event_handler(client: Client, message: Message):
    ist_timezone = pytz.timezone('Asia/Kolkata')
    current_time = datetime.now(tz=ist_timezone).strftime("%a %b %d %H:%M:%S %Y")

    if message.reply_markup:
        urls = getUrl(text)
        if not urls:
            return
        text = requests.get(urls[0]).text
    else:
        text = message.text
    ...

    cards = getcards(text)   
    if not cards:
        return
    cc, mes, ano, cvv = cards
    if cc in ccs:
        return
    ccs.append(cc)
    extra = cc[0:0 + 12]
    bin = requests.get(f'https://bins.antipublic.cc/bins/{cc[:6]}')
    if not bin:
        return
    bin_json = bin.json()
    fullinfo = f"{cc}|{mes}|{ano}|{cvv}"
    print(f'{cc}|{mes}|{ano}|{cvv} - ALPHA XOP [a+]')
    with open('cards.txt', 'a') as w:
        w.write(fullinfo + '\n')

    await app.send_message(
        chat_id=SEND_ID,
        text=f"""
══════════════════════
                тσχιᴄ ѕᴄяαρρєя    
══════════════════════

**• ᴄᴀʀᴅ ⥁**
  ⤷ `{cc}|{mes}|{ano}|{cvv}` 
**━━━━━━━━━━━━━━━━━━━**
**• ʙɪɴ ➻** `{cc[:6]}` | {bin_json['country_flag']}

**• ɪɴғᴏ ➻**  `{bin_json['type']}` 
**• ᴛʏᴘᴇ ➻** `{bin_json['brand']}`
**• ʙᴀɴᴋ ➻** `{bin_json['bank']}`
**• ᴄᴏᴜɴᴛʀʏ ➻** `{bin_json['country_name']}` | {bin_json['country_flag']} 

**• ᴇxᴛʀᴀ ➻**
  ⤷ `{extra}xxxx|{mes}|{ano}|{cvv}` 
**━━━━━━━━━━━━━━━━━━━**
**Time:** `{current_time}` (IST)
""",)



@app.on_message(filters.outgoing & filters.regex(r'\.lives'))
async def my_event_handler(client: Client, message: Message):
    await message.reply_document(document='cards.txt')
    await asyncio.sleep(30)


app.run()
