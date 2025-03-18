# Discord Profile Picture Fetcher

A Python-based bot to fetch and process Discord profile pictures from discord channels using webhooks.
---

## Features

- Fetches profile pictures from discord channels
- Downloads images in configurable sizes (128, 256, 512, etc.).
- Sends images to specified Discord webhooks.
- Supports multiple channels with unique webhooks.
- Debug mode for detailed logging.

---

## Requirements

- Python 3.8 or higher
- Discord token
- Required Python libraries (see [Dependencies](#dependencies))

---

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/2034/Discord-PFP-Fetcher.git
    cd Discord-PFP-Fetcher
    ```

2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Add your Discord bot token**:
    - Create a `token.txt` file in the project directory.
    - Add your bot token inside the file:
      ```
      YOUR_DISCORD_BOT_TOKEN
      ```

4. **Configure channels and webhooks**:
    - Edit the `profileChannels` dictionary in `main.py` with your channel IDs and webhook URLs.

---

## Configuration

### profileChannels
Map channel IDs to their respective names and webhook URLs:
```python
profileChannels = {
     123456789012345678: ["channel_name", "https://discord.com/api/webhooks/your_webhook_url"],
     987654321098765432: ["another_channel", "https://discord.com/api/webhooks/another_webhook_url"]
}
```

### Image Size
Set the size of downloaded images by modifying the `imageSize` variable:
```python
imageSize = 512  # Options: 128, 256, 512, 1024, 2048, 4096
```

### Debug Mode
Enable or disable debug mode by setting the `debug` variable:
```python
debug = True  # Set to False to disable debug output
```

---

## Dependencies

The following Python libraries are required:
- discord.py-self: For interacting with the Discord API.
- requests: For making HTTP requests.
- asyncio: For asynchronous operations.
- colorama: For colored terminal output.

Install them using:
```bash
pip install -r requirements.txt
```

---

## Error Handling

- If a webhook is invalid, the bot will log an error and skip processing for that channel.
- If an image download fails, the bot will log the failure and continue processing other messages.
- If the bot encounters a critical error, it will log the error and exit.