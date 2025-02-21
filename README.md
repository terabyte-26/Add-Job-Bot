# Job Posting Bot

This is a Telegram bot for job posting. The bot allows users to add job postings, which are then verified by admins before being posted to a public channel.

## Features

- Start command to check group membership
- Add job command to submit job details
- Admin approval process for job postings
- Interactive buttons for user inputs

## Prerequisites

- Python 3.8+
- Telegram Bot API credentials

## Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/wmerl/Add-Job-Bot/
    cd Add-Job-Bot
    ```

2. **Create a virtual environment**:

    ```bash
    python -m venv .venv
    ```

3. **Activate the virtual environment**:

    - **Windows**:
      ```bash
      .\.venv\Scripts\activate
      ```
    - **macOS/Linux**:
      ```bash
      source .venv/bin/activate
      ```

4. **Install the dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

5. **Create a `.env` file** in the root directory and add your Telegram Bot API credentials:

    ```env
    API_ID=your_api_id
    API_HASH=your_api_hash
    BOT_TOKEN=your_bot_token
    ```

## Running the Bot

1. **Run the bot**:

    ```bash
    python run.py
    ```

2. The bot should now be live and listening for commands.

## Project Structure

```
.
├── bot/
│ ├── init.py
│ ├── callbacks.py
├── consts.py
├── requirements.txt
├── run.py
├── Procfile
└── .env
```



## Bot Commands

- **/start**: Checks if the user is a member of the group and sends appropriate messages.
- **/add_job**: Initiates the process of adding a new job posting.

## Admin Commands

- **verify**: Approves the job posting.
- **reject**: Rejects the job posting.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


