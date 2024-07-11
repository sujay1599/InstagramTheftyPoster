import yaml
from cryptography.fernet import Fernet
import getpass

# Generate a key and instantiate a Fernet instance
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Get credentials from the user
username = input('Enter Instagram username: ').encode()
password = getpass.getpass('Enter Instagram password: ').encode()  # Use getpass to hide input

# Encrypt the credentials
encrypted_username = cipher_suite.encrypt(username).decode()
encrypted_password = cipher_suite.encrypt(password).decode()

# Store the encrypted credentials and the encryption key in the config
config = {
    'instagram': {
        'username': encrypted_username,
        'password': encrypted_password
    },
    'key': key.decode(),  # Store the encryption key in the config
    'scraping': {
        'enabled': input('Enable scraping? (true/false): ').lower() == 'true',
        'profiles': input('Enter profiles to scrape (space separated): '),
        'num_reels': int(input('Number of reels to scrape per profile: ')),
        'scrape_interval_minutes': int(input('Interval between scrapes (minutes): '))
    },
    'uploading': {
        'enabled': input('Enable uploading? (true/false): ').lower() == 'true',
        'upload_interval_minutes': int(input('Interval between uploads (minutes): ')),
        'add_to_story': input('Add to story? (true/false): ').lower() == 'true'
    },
    'hashtags': {
        'use_hashtags': input('Use hashtags? (true/false): ').lower() == 'true'
    }
}

if config['hashtags']['use_hashtags']:
    config['hashtags']['hashtags_list'] = input('Enter hashtags (space separated): ')

config['deleting'] = {
    'periodically_delete_reels_uploaded': input('Enable periodic deletion of uploaded reels? (true/false): ').lower() == 'true'
}

if config['deleting']['periodically_delete_reels_uploaded']:
    config['deleting']['delete_interval_minutes'] = int(input('Interval between deletions (minutes, 0 for immediate): '))

# Save the config to a file
with open('config.yaml', 'w') as file:
    yaml.dump(config, file)

print('Configuration saved to config.yaml')