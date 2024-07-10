import os

# Load the log file
log_filename = 'upload_log.txt'

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
