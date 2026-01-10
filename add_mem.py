from telethon import TelegramClient, errors
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.types import InputPeerUser
import csv
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()

api_id = int(os.getenv("TELEGRAM_API_ID"))
api_hash = os.getenv("TELEGRAM_API_HASH")

# Public group OR private link (must be joined!)
target_group = "https://t.me/highschools_confessions"

client = TelegramClient("session", api_id, api_hash)


async def main():
    await client.start()

    # Load target entity
    group = await client.get_entity(target_group)
    print(f"Target group loaded: {group.title}")

    # CSV path (relative, GitHub-safe)
    csv_path = os.path.join("csv", "abrshi3118.csv")

    with open(csv_path, encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)  # skip headers

        for username, user_id in reader:
            try:
                user = None
                if username:
                    user = await client.get_entity(username)
                else:
                    user = InputPeerUser(int(user_id), 0)

                await client(InviteToChannelRequest(group, [user]))
                print(f"Added: {username or user_id}")

                await asyncio.sleep(35)

            except errors.FloodWaitError as e:
                print(f"FloodWait: wait {e.seconds} seconds")
                await asyncio.sleep(e.seconds)

            except errors.UserPrivacyRestrictedError:
                print(f"Privacy restricted: {username or user_id}")

            except errors.UserNotMutualContactError:
                print(f"Cannot add (not mutual contact): {username or user_id}")

            except errors.UserIdInvalidError:
                print(f"Invalid ID: {username or user_id}")

            except Exception as e:
                print(f"Failed: {username or user_id} -> {e}")


with client:
    client.loop.run_until_complete(main())
