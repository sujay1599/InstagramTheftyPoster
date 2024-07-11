
# InstagramTheftyPoster

InstagramTheftyPoster is a Python project designed to automate the process of scraping, uploading, and optionally deleting Instagram reels. The application uses encrypted credentials to log in to Instagram, scrape reels from specified profiles, upload them with new descriptions, and manage the deletion of uploaded reels based on user-defined intervals.

## Features

- **Scrape Instagram Reels**: Automatically scrape reels from specified Instagram profiles.
- **Upload Reels**: Upload the scraped reels to another Instagram account with new descriptions and optional hashtags.
- **Add to Story**: Optionally add uploaded reels to Instagram stories.
- **Periodic Deletion**: Delete uploaded reels either immediately after upload or based on a user-defined interval.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/sujay1599/InstagramTheftyPoster.git
   cd InstagramTheftyPoster
   ```

2. **Create and activate a virtual environment (optional but recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install the required packages:**

   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. **Run the `start.py` script to configure the application:**

   ```bash
   python start.py
   ```

   This script will prompt you for the following information:
   - Instagram username and password (encrypted and stored in `config.yaml`)
   - Scraping options (enable/disable, profiles to scrape, number of reels per profile, interval between scrapes)
   - Uploading options (enable/disable, interval between uploads, add to story)
   - Hashtags options (enable/disable, list of hashtags)
   - Deletion options (enable/disable periodic deletion, interval between deletions)

2. **Configuration file (`config.yaml`):**

   The configuration details provided during the `start.py` script execution will be saved in a `config.yaml` file. Here is an example of what the configuration file might look like:

   ```yaml
   instagram:
     username: <encrypted_username>
     password: <encrypted_password>
   key: <encryption_key>
   scraping:
     enabled: true
     profiles: profile1 profile2
     num_reels: 5
     scrape_interval_minutes: 60
   uploading:
     enabled: true
     upload_interval_minutes: 30
     add_to_story: true
   hashtags:
     use_hashtags: true
     hashtags_list: "#example #hashtag"
   deleting:
     periodically_delete_reels_uploaded: true
     delete_interval_minutes: 1440
   ```

## Usage

1. **Run the main script to start the automation:**

   ```bash
   python main.py
   ```

   The script will:
   - Log in to Instagram using the provided credentials.
   - Scrape reels from specified profiles at the defined interval.
   - Upload scraped reels with new descriptions and optional hashtags.
   - Add uploaded reels to stories if enabled.
   - Delete uploaded reels based on the defined deletion interval.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
```

This `README.md` provides a comprehensive guide to setting up, configuring, and running your project, as well as information on contributing and the project's license.
