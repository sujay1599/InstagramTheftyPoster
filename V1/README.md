# InstagramTheftPoster

InstagramTheftyPoster allows users to log in to Instagram, scrape profiles for reels, and download the reels to a designated download folder within the project. Additionally, the downloaded reels can be uploaded to the user's Instagram account or posted on their Instagram stories.

## Requirements

To install the required packages, run:

```
pip install -r requirements.txt
```


## Configuration

Before running the scripts, create a `config.yaml` file by running `start.py`. 

This will prompt you to enter your Instagram credentials, scraping profiles, and other configurations.

```yaml
instagram:
  username: ''
  password: ''
scraping:
  enabled: true
  profiles: ''
  num_reels: 10
  scrape_interval_minutes: 60
uploading:
  enabled: true
  delete_after_upload: true
  upload_interval_minutes: 5
  add_to_story: true
hashtags:
  use_hashtags: true
  hashtags_list: '#example #hashtag'
```

## Usage
Configure: Run start.py to create the config.yaml file.
Run: Execute main.py to start scraping and uploading reels based on the configuration.

## Commands
```
python start.py
python main.py
```

## Main Functions


## The script performs the following tasks:
## main.py
```
Login to Instagram: Uses the credentials provided in config.yaml.
Scrape Reels: Scrapes the specified number of reels from the profiles listed in the configuration.
Upload Reels: Uploads the scraped reels to your Instagram account and optionally adds them to your story.
Logging: Keeps track of uploaded reels to avoid duplicates.
start.py
Prompts the user to enter configuration details and saves them in config.yaml.
Saves scrapped items to folder called download within the project.
```

## delete.py
This script reads the upload_log.txt file to get a list of uploaded reels and deletes the corresponding .mp4, .mp4.jpg, and .txt files from the downloads folder.

## Log Files
```
upload_log.txt: Keeps track of the IDs of uploaded reels to prevent re-uploading the same content.

last_scraped_timestamp.txt: Stores the timestamp of the last scraped reel to ensure that only new reels are scraped in subsequent runs.
```
## License
This project is licensed under the MIT License.
