import yaml

config = {
    'instagram': {
        'username': input('Enter Instagram username: '),
        'password': input('Enter Instagram password: ')
    },
    'scraping': {
        'enabled': input('Enable scraping? (true/false): ').lower() == 'true',
        'profiles': input('Enter profiles to scrape (comma separated): '),
        'num_reels': int(input('Number of reels to scrape per profile: ')),
        'scrape_interval_minutes': int(input('Interval between scrapes (minutes): '))
    },
    'uploading': {
        'enabled': input('Enable uploading? (true/false): ').lower() == 'true',
        'upload_interval_minutes': int(input('Interval between uploads (minutes): ')),
        'add_to_story': input('Add to story? (true/false): ').lower() == 'true'
    },
    'deleting': {
        'periodically_delete_reels_uploaded': input('Enable periodic deletion of uploaded reels? (true/false): ').lower() == 'true'
    },
    'hashtags': {
        'use_hashtags': input('Use hashtags? (true/false): ').lower() == 'true'
    }
}

if config['deleting']['periodically_delete_reels_uploaded']:
    config['deleting']['delete_interval_minutes'] = int(input('Interval between deletions (minutes, 0 for immediate): '))

if config['hashtags']['use_hashtags']:
    config['hashtags']['hashtags_list'] = input('Enter hashtags (comma separated): ')

with open('config.yaml', 'w') as file:
    yaml.dump(config, file)

print('Configuration saved to config.yaml')
