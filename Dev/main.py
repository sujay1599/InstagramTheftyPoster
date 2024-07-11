import os
import yaml
import json
from cryptography.fernet import Fernet
from instagrapi import Client
from time import sleep
from datetime import datetime, timedelta
import moviepy.editor as mp

# Load configuration
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

# Load the encryption key and encrypted credentials
key = config['key'].encode()
cipher_suite = Fernet(key)
encrypted_username = config['instagram']['username'].encode()
encrypted_password = config['instagram']['password'].encode()

# Decrypt the credentials
INSTAGRAM_USERNAME = cipher_suite.decrypt(encrypted_username).decode()
INSTAGRAM_PASSWORD = cipher_suite.decrypt(encrypted_password).decode()

SCRAPING_ENABLED = config['scraping']['enabled']
UPLOAD_ENABLED = config['uploading']['enabled']
PERIODICALLY_DELETE_REELS_UPLOADED = config['deleting']['periodically_delete_reels_uploaded']
NUM_REELS = config['scraping']['num_reels']
USE_HASHTAGS = config['hashtags']['use_hashtags']
HASHTAGS_LIST = config['hashtags'].get('hashtags_list', '')
UPLOAD_INTERVAL_MINUTES = config['uploading']['upload_interval_minutes']
ADD_TO_STORY = config['uploading']['add_to_story']
SCRAPE_INTERVAL_MINUTES = config['scraping']['scrape_interval_minutes']
DELETE_INTERVAL_MINUTES = config['deleting'].get('delete_interval_minutes', 0)

# Initialize the Instagram client
cl = Client()

# Login to Instagram
try:
    cl.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
    print("Logged in using username and password")
except Exception as e:
    print(f"Username/password login failed: {e}")
    exit(1)

# Load or initialize the log file
log_filename = 'upload_log.txt'
last_scraped_file = 'last_scraped_timestamp.txt'

if os.path.exists(log_filename):
    with open(log_filename, 'r') as log_file:
        uploaded_reels = set(line.strip() for line in log_file)
else:
    uploaded_reels = set()

if os.path.exists(last_scraped_file):
    with open(last_scraped_file, 'r') as file:
        last_scraped_timestamp = int(file.read().strip())
else:
    last_scraped_timestamp = 0

def get_unuploaded_reels():
    downloads_dir = 'downloads'
    unuploaded_reels = []
    for filename in os.listdir(downloads_dir):
        if filename.endswith('.mp4'):
            reel_id = filename.split('_')[1].split('.')[0]
            if reel_id not in uploaded_reels:
                unuploaded_reels.append(filename)
    return unuploaded_reels

def scrape_reels(username, num_reels):
    global last_scraped_timestamp
    user_id = cl.user_id_from_username(username)
    try:
        reels = cl.user_clips(user_id, amount=num_reels)
    except json.JSONDecodeError as e:
        print(f"JSONDecodeError: {e} - Retrying in 5 seconds")
        sleep(5)
        try:
            reels = cl.user_clips(user_id, amount=num_reels)
        except json.JSONDecodeError as e:
            print(f"Failed to decode JSON again: {e}")
            return []
    except Exception as e:
        print(f"Error fetching reels: {e}")
        return []
    
    os.makedirs('downloads', exist_ok=True)  # Ensure the 'downloads' directory exists
    downloaded_reels = []
    for reel in reels:
        if reel.taken_at.timestamp() <= last_scraped_timestamp:
            print(f"Reel {reel.pk} was posted before last scrape. Skipping...")
            continue
        
        if f"{username}_{reel.pk}" in uploaded_reels:
            print(f"Reel {reel.pk} already uploaded. Skipping...")
            continue
        
        expected_media_path = os.path.join('downloads', f'{username}_{reel.pk}.mp4')
        if os.path.exists(expected_media_path):
            print(f"Reel {reel.pk} already downloaded. Skipping...")
            continue
        
        media_path = cl.clip_download(reel.pk, folder='downloads')
        if os.path.exists(expected_media_path):  # Check if the file was downloaded successfully
            description_path = os.path.join('downloads', f'{reel.pk}.txt')
            with open(description_path, 'w', encoding='utf-8') as f:
                f.write(reel.caption_text)
            print(f"Scraped and saved reel: {reel.pk}")
            downloaded_reels.append(reel)
        else:
            print(f"Failed to download reel: {reel.pk}")
    
    if downloaded_reels:
        last_scraped_timestamp = max(reel.taken_at.timestamp() for reel in downloaded_reels)
        with open(last_scraped_file, 'w') as file:
            file.write(str(int(last_scraped_timestamp)))

    return downloaded_reels

def upload_reels_with_new_descriptions(unuploaded_reels, username):
    if not unuploaded_reels:
        print("No new reels to upload.")
        return
    for reel_file in unuploaded_reels:
        reel_id = reel_file.split('_')[1].split('.')[0]
        media_path = os.path.join('downloads', reel_file)
        description_path = os.path.join('downloads', f'{reel_id}.txt')
        if not os.path.exists(media_path) or f"{username}_{reel_id}" in uploaded_reels:
            print(f"Media file {media_path} not found or already uploaded. Skipping upload for reel: {reel_id}")
            continue
        new_description = f"Taken from: @{username}\n{HASHTAGS_LIST}"
        
        # Upload to Instagram feed
        cl.clip_upload(media_path, new_description)
        print(f"Uploaded reel: {reel_id} with description: {new_description}")
        
        # Upload to Instagram story
        if ADD_TO_STORY:
            cl.video_upload_to_story(media_path, new_description)
            print(f"Added reel: {reel_id} to story")
        
        # Release video file resources using moviepy
        video = mp.VideoFileClip(media_path)
        video.reader.close()
        if video.audio:
            video.audio.reader.close_proc()
        
        # Log the upload
        with open(log_filename, 'a') as log_file:
            log_file.write(f"{username}_{reel_id}\n")
        
        # Update the set of uploaded reels
        uploaded_reels.add(f"{username}_{reel_id}")
        
        if PERIODICALLY_DELETE_REELS_UPLOADED and DELETE_INTERVAL_MINUTES == 0:
            try:
                os.remove(media_path)
                os.remove(description_path)
                print(f"Deleted reel: {reel_id} and its description file")
            except PermissionError as e:
                print(f"Failed to delete reel: {reel_id}, {e}")
        
        next_upload_time = datetime.now() + timedelta(minutes=UPLOAD_INTERVAL_MINUTES)
        print(f"Next upload at: {next_upload_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Waiting for {UPLOAD_INTERVAL_MINUTES} minutes before next upload.")
        sleep(UPLOAD_INTERVAL_MINUTES * 60)

def delete_uploaded_files():
    # Load the log file
    if os.path.exists(log_filename):
        with open(log_filename, 'r') as log_file:
            uploaded_reels = set(line.strip() for line in log_file)
    else:
        uploaded_reels = set()

    # Delete files in the downloads folder that match the log
    downloads_dir = 'downloads'

    for filename in os.listdir(downloads_dir):
        if filename.endswith('.mp4') or filename.endswith('.mp4.jpg') or filename.endswith('.txt'):
            base_filename = '_'.join(filename.split('_')[:2])  # Extract username and reel_id part
            if base_filename in uploaded_reels:
                try:
                    os.remove(os.path.join(downloads_dir, filename))
                    print(f"Deleted file: {filename}")
                except Exception as e:
                    print(f"Failed to delete {filename}: {e}")

    print("Deletion process completed.")

def main():
    global last_scraped_timestamp
    while True:
        if SCRAPING_ENABLED:
            profiles_to_scrape = config['scraping']['profiles'].split(',')
            for profile in profiles_to_scrape:
                print(f"Scraping profile: {profile}")
                reels = scrape_reels(profile, num_reels=NUM_REELS)
                print(f"Finished scraping reels for profile: {profile}")
            if UPLOAD_ENABLED:
                print("Starting upload of scraped reels.")
                for profile in profiles_to_scrape:
                    unuploaded_reels = get_unuploaded_reels()
                    upload_reels_with_new_descriptions(unuploaded_reels, profile)
        if PERIODICALLY_DELETE_REELS_UPLOADED and DELETE_INTERVAL_MINUTES > 0:
            print(f"Waiting for {DELETE_INTERVAL_MINUTES} minutes before deleting uploaded reels.")
            sleep(DELETE_INTERVAL_MINUTES * 60)
            print("Starting deletion of uploaded reels.")
            delete_uploaded_files()
        
        print(f"Waiting for {SCRAPE_INTERVAL_MINUTES} minutes before next cycle.")
        sleep(SCRAPE_INTERVAL_MINUTES * 60)

if __name__ == "__main__":
    main()