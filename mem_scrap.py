from telethon import TelegramClient
import csv
import os
from dotenv import load_dotenv
import logging
from datetime import datetime
from tqdm import tqdm  # Import tqdm for progress bar

# Setup logging
def setup_logging():
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"scraper_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

# Initialize logger
logger = setup_logging()

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
        # Get all members with progress bar
        logger.info(f"Starting scrape for {group_username}")
        
        print("\n" + "=" * 60)
        print("FETCHING MEMBERS...")
        print("=" * 60 + "\n")
        
        # Initialize progress bar
        progress_bar = tqdm(
            desc="Scraping Members",
            unit=" members",
            bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]"
        )
        
        # Get members with progress tracking
        members = []
        async for user in client.iter_participants(group_username):
            members.append(user)
            progress_bar.update(1)
        
        progress_bar.close()
        
        if not members:
            print("\nNo members found or you don't have access to this group.")
            logger.warning(f"No members found for {group_username}")
            return
            
        print(f"\nFound {len(members)} members.")
        logger.info(f"Found {len(members)} members in {group_username}")
        
        # Create csv directory if it doesn't exist
        os.makedirs("csv", exist_ok=True)
        
        # Get filename from user
        filename = input("\nEnter the CSV filename (without .csv): ").strip()
        if not filename.endswith('.csv'):
            filename += '.csv'
        
        csv_path = os.path.join("csv", filename)
        
        print("\n" + "=" * 60)
        print("SAVING DATA TO CSV...")
        print("=" * 60 + "\n")
        
        # Save to CSV with progress bar
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["username", "id"])
            
            # Add progress bar for writing
            with tqdm(total=len(members), desc="Saving to CSV", unit=" rows") as save_bar:
                for user in members:
                    username = user.username if user.username else ""
                    writer.writerow([username, user.id])
                    save_bar.update(1)
        
        print(f"\n" + "=" * 60)
        print(f"SUCCESS: {len(members)} members saved to csv/{filename}")
        print("=" * 60)
        logger.info(f"Data saved to {csv_path}")
        
    except Exception as e:
        print(f"\n ERROR: {e}")
        logger.error(f"Error occurred: {e}", exc_info=True)
        print("\nPossible reasons:")
        print("1. You're not a member of the group")
        print("2. The group doesn't exist")
        print("3. You don't have permission to view members")
        print("4. Telegram API restrictions")

# Main execution
try:
    with client:
        client.loop.run_until_complete(main())
        
    # Final warning
    print("\n" + "=" * 60)
    print("REMEMBER: Use this data responsibly and ethically.")
    print("Respect user privacy and Telegram's Terms of Service.")
    print("=" * 60)
    
except KeyboardInterrupt:
    print("\n\n Process interrupted by user.")
    logger.warning("Process interrupted by user")
except Exception as e:
    logger.error(f"Fatal error: {e}", exc_info=True)
    print(f"\n Fatal error occurred. Check logs for details.")