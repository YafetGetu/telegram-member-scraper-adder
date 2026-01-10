from telethon import TelegramClient, errors
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.types import InputPeerUser
import csv
import asyncio
from dotenv import load_dotenv
import os

# WARNING MESSAGE
print("=" * 70)
print("IMPORTANT WARNING & TERMS OF USE:")
print("=" * 70)
print("1. EDUCATIONAL PURPOSE ONLY - This tool is for learning about APIs")
print("2. PERMISSION REQUIRED - You must have admin rights to add members")
print("3. RESPECT PRIVACY - Only add users who want to join the group")
print("4. TELEGRAM TERMS - Violating Telegram's ToS can result in account ban")
print("5. SPAMMING PROHIBITED - Adding users without consent is illegal")
print("6. RATE LIMITS - Respect Telegram's rate limits to avoid bans")
print("=" * 70)

confirm = input("\nDo you understand and accept these conditions? (yes/no): ").strip().lower()

if confirm != 'yes':
    print("\nOperation cancelled. Please read and accept the conditions.")
    exit()

# Get target group from user
print("\n" + "=" * 60)
print("ENTER TARGET GROUP INFORMATION")
print("=" * 60)
print("You MUST be an ADMIN in this group to add members")
print("Examples:")
print("- https://t.me/examplegroup")
print("- @examplegroup")
print("- t.me/examplegroup")
print("=" * 60)

target_group = input("\nEnter the group link/username: ").strip()

# Validate input
if not target_group:
    print("Error: Group link cannot be empty!")
    exit()

# Clean up input
if target_group.startswith("https://"):
    target_group = target_group[8:]  # Remove https://
if target_group.startswith("t.me/"):
    target_group = "@" + target_group[5:]  # Convert to @username format
elif not target_group.startswith("@"):
    target_group = "@" + target_group

print(f"\nTarget group set to: {target_group}")

# Check if user has admin rights
admin_check = input("\nAre you an ADMIN in this group? (yes/no): ").strip().lower()
if admin_check != 'yes':
    print("\nERROR: You must be an admin to add members to this group!")
    print("Operation cancelled.")
    exit()

load_dotenv()

api_id = int(os.getenv("TELEGRAM_API_ID"))
api_hash = os.getenv("TELEGRAM_API_HASH")

client = TelegramClient("session", api_id, api_hash)

async def main():
    await client.start()

    print(f"\n" + "=" * 60)
    print("LOADING GROUP INFORMATION")
    print("=" * 60)
    
    try:
        # Load target entity
        group = await client.get_entity(target_group)
        print(f"Target group: {group.title}")
        
        # Check if user is admin (basic check)
        try:
            my_permissions = await client.get_permissions(group, await client.get_me())
            if not my_permissions.is_admin:
                print("\nWARNING: You might not have admin privileges!")
                print("You can only add members if you're an admin.")
                
                continue_check = input("Continue anyway? (yes/no): ").strip().lower()
                if continue_check != 'yes':
                    print("Operation cancelled.")
                    return
        except:
            print("Note: Could not verify admin status automatically")
        
    except errors.ChannelInvalidError:
        print(f"Error: Cannot access group {target_group}")
        print("Possible reasons:")
        print("1. Group doesn't exist")
        print("2. You're not a member")
        print("3. The link is incorrect")
        return
    except Exception as e:
        print(f"Error loading group: {e}")
        return
    
    # List available CSV files
    csv_dir = "csv"
    if not os.path.exists(csv_dir):
        print(f"\nERROR: '{csv_dir}' directory not found!")
        print(f"Please run the scraper tool first to create CSV files.")
        return
    
    csv_files = [f for f in os.listdir(csv_dir) if f.endswith('.csv')]
    
    if not csv_files:
        print(f"\nERROR: No CSV files found in '{csv_dir}' directory!")
        print(f"Please run the scraper tool first to create CSV files.")
        return
    
    print(f"\n" + "=" * 60)
    print("AVAILABLE CSV FILES")
    print("=" * 60)
    for i, csv_file in enumerate(csv_files, 1):
        print(f"{i}. {csv_file}")
    print("=" * 60)
    
    # Let user select CSV file
    while True:
        try:
            selection = input(f"\nSelect CSV file (1-{len(csv_files)}): ").strip()
            if selection.isdigit():
                idx = int(selection) - 1
                if 0 <= idx < len(csv_files):
                    selected_csv = csv_files[idx]
                    break
            print(f"Please enter a number between 1 and {len(csv_files)}")
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            return
    
    csv_path = os.path.join(csv_dir, selected_csv)
    print(f"\nUsing CSV file: {selected_csv}")
    print(f"Adding members to: {group.title}")
    print("=" * 60)
    
    # Confirm before proceeding
    final_confirm = input("\nSTART adding members? (yes/no): ").strip().lower()
    if final_confirm != 'yes':
        print("Operation cancelled.")
        return
    
    print("\n" + "=" * 60)
    print("STARTING MEMBER ADDITION PROCESS")
    print("=" * 60)
    print("Note: 35-second delay between invites to avoid spam detection")
    print("=" * 60)
    
    success_count = 0
    fail_count = 0
    total_users = 0
    
    with open(csv_path, encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)  # skip headers
        
        rows = list(reader)
        total_users = len(rows)
        
        print(f"\nProcessing {total_users} users from CSV...")
        
        for username, user_id in rows:
            try:
                user = None
                if username:
                    try:
                        user = await client.get_entity(username)
                    except ValueError:
                        print(f"Invalid username format: {username}")
                        fail_count += 1
                        continue
                else:
                    try:
                        user = InputPeerUser(int(user_id), 0)
                    except ValueError:
                        print(f"Invalid user ID: {user_id}")
                        fail_count += 1
                        continue
                
                if user:
                    await client(InviteToChannelRequest(group, [user]))
                    print(f"Added: {username or user_id}")
                    success_count += 1
                    
                    # Delay to avoid spam detection
                    await asyncio.sleep(35)

            except errors.FloodWaitError as e:
                print(f"FloodWait: Waiting {e.seconds} seconds")
                await asyncio.sleep(e.seconds)
                
                # Retry after waiting
                try:
                    await client(InviteToChannelRequest(group, [user]))
                    print(f"Added after wait: {username or user_id}")
                    success_count += 1
                    await asyncio.sleep(35)
                except:
                    print(f"Failed after retry: {username or user_id}")
                    fail_count += 1

            except errors.UserPrivacyRestrictedError:
                print(f"Privacy restricted: {username or user_id}")
                fail_count += 1

            except errors.UserNotMutualContactError:
                print(f"Cannot add (not mutual contact): {username or user_id}")
                fail_count += 1

            except errors.UserIdInvalidError:
                print(f"Invalid ID: {username or user_id}")
                fail_count += 1

            except Exception as e:
                print(f"Failed: {username or user_id} -> {type(e).__name__}")
                fail_count += 1
    
    # Summary
    print("\n" + "=" * 60)
    print("PROCESS COMPLETE - SUMMARY")
    print("=" * 60)
    print(f"Total users processed: {total_users}")
    print(f"Successfully added: {success_count}")
    print(f"Failed to add: {fail_count}")
    print("=" * 60)
    
    # Final reminder
    print("\n" + "=" * 60)
    print("REMINDER: Use this tool responsibly!")
    print("- Respect user privacy")
    print("- Only add willing participants")
    print("- Follow Telegram's Terms of Service")
    print("=" * 60)

with client:
    client.loop.run_until_complete(main())