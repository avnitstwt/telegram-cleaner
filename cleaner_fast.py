import asyncio
from telethon import TelegramClient

# 🔑 YOUR DETAILS
api_id = 1780047
api_hash = "35981a05b4634fc98359fb023a1c824f"
channel = -1002437817236

DAILY_DELETE_LIMIT = 10

client = TelegramClient("session", api_id, api_hash)

seen_files = {}
deleted_count = 0

async def main():
    global deleted_count

    async for msg in client.iter_messages(channel):
        if deleted_count >= DAILY_DELETE_LIMIT:
            print("✅ Daily delete limit reached")
            break

        if msg.document:
            try:
                file_name = msg.document.attributes[0].file_name
                file_size = msg.document.size

                # 🔑 Unique key (no download)
                key = (file_name, file_size)

                if key in seen_files:
                    print(f"🗑 Deleting duplicate: {file_name}")

                    await msg.delete()
                    deleted_count += 1

                    # Log message in channel
                    await client.send_message(
                        channel,
                        f"⚡ [Cleaner]\nDeleted duplicate:\n📄 {file_name}"
                    )

                else:
                    seen_files[key] = msg.id

            except Exception as e:
                print(f"Error: {e}")

    print(f"✅ Total deleted today: {deleted_count}")

async def start():
    await client.start()
    await main()

asyncio.run(start())