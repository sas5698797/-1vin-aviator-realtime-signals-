import asyncio
import websockets
import os
import datetime
from telegram import Bot

# GitHub Secrets se variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
WS_TOKEN = os.getenv("WS_TOKEN")

# WebSocket URL
WS_URL = f"wss://cf.1win.direct/v4/socket.io/?Authorization={WS_TOKEN}&Language=en&xorigin=1waqhg.life&EIO=4&transport=websocket"

bot = Bot(token=BOT_TOKEN)

async def listen():
    try:
        async with websockets.connect(WS_URL, extra_headers={
            "Origin": "https://1waqhg.life",
            "User-Agent": "Mozilla/5.0"
        }) as websocket:
            print(f"[{datetime.datetime.now()}] ✅ Connected to WebSocket")

            # Initial handshake
            await websocket.send("40")
            await asyncio.sleep(1)

            start_time = datetime.datetime.now()

            while True:
                if (datetime.datetime.now() - start_time).total_seconds() > 600:  # ⏱️ 10 minute
                    print("🛑 Bot stopped after 10 minutes")
                    break

                msg = await websocket.recv()

                if "crash" in msg:
                    print(f"[{datetime.datetime.now()}] ✈️ Crash Signal: {msg}")
                    await bot.send_message(chat_id=CHAT_ID, text=f"✈️ Aviator Crash Signal: {msg}")

                await asyncio.sleep(0.1)

    except Exception as e:
        print(f"[{datetime.datetime.now()}] ❌ Error: {e}")

asyncio.run(listen())
