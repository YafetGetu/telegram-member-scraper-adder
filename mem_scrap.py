from telethon import TelegramClient
import csv
import os
from dotenv import load_dotenv

# WARNING MESSAGE
print("=" * 60)
print("IMPORTANT WARNING:")
print("=" * 60)
print("1. This tool is for EDUCATIONAL PURPOSES ONLY.")
print("2. You must have PERMISSION to scrape members from any group.")
print("3. RESPECT user privacy and Telegram's Terms of Service.")
print("4. Make sure to TURN OFF 2-Step Verification in your")
print("   Telegram account settings before using this tool.")
print("=" * 60)

confirm = input("Do you understand and accept these conditions? (yes/no): ")

if confirm.lower() != 'yes':
    print("Operation cancelled. Please read and accept the conditions.")
    exit()

# Get group username from user
print("\n" + "=" * 60)
group_username = input("Enter the group username (e.g., @groupof2011 or groupof2011): ").strip()

# Ensure the username starts with @
if not group_username.startswith('@'):
    group_username = '@' + group_username

print(f"Target group: {group_username}")
print("=" * 60)

# Check if user has turned off 2-step verification
check_2fa = input("\nHave you turned OFF 2-Step Verification? (yes/no): ")

if check_2fa.lower() != 'yes':
    print("\n" + "=" * 60)
    print("PLEASE TURN OFF 2-STEP VERIFICATION FIRST!")
    print("Go to: Telegram Settings > Privacy and Security > 2-Step Verification")
    print("Then click 'Disable' or 'Turn Off'")
    print("=" * 60)
    print("\nRun this script again after disabling 2-Step Verification.")
    exit()

load_dotenv()

api_id = int(os.getenv("TELEGRAM_API_ID"))
api_hash = os.getenv("TELEGRAM_API_HASH")

client = TelegramClient("anonym", api_id, api_hash)

async def main():
    await client.start()

    print(f"\nScraping members from {group_username}...")
    print("This may take a while depending on group size...")
    
    try:
        members = await client.get_participants(group_username)
        
        if not members:
            print("No members found or you don't have access to this group.")
            return
            
        print(f"Found {len(members)} members.")
        
        # Create csv directory if it doesn't exist
        os.makedirs("csv", exist_ok=True)
        
        # Get filename from user
        filename = input("\nEnter the CSV filename (without .csv): ").strip()
        if not filename.endswith('.csv'):
            filename += '.csv'
        
        csv_path = os.path.join("csv", filename)
        
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["username", "id"])
            for user in members:
                username = user.username if user.username else ""
                writer.writerow([username, user.id])
        
        print(f"\n" + "=" * 60)
        print(f"SUCCESS: {len(members)} members saved to csv/{filename}")
        print("=" * 60)
        
    except Exception as e:
        print(f"\nERROR: {e}")
        print("Possible reasons:")
        print("1. You're not a member of the group")
        print("2. The group doesn't exist")
        print("3. You don't have permission to view members")
        print("4. Telegram API restrictions")

with client:
    client.loop.run_until_complete(main())

# Final warning
print("\n" + "=" * 60)
print("REMEMBER: Use this data responsibly and ethically.")
print("Respect user privacy and Telegram's Terms of Service.")
print("=" * 60)