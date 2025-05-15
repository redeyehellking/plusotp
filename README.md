# OTP Shop Bot

OTP Shop Bot is a Telegram bot that allows users to purchase One-Time Password (OTP) accounts. It supports both fresh and old accounts, providing a seamless experience for users to browse, select, and buy OTP accounts.

## Features

- Browse and purchase fresh OTP accounts
- Browse and purchase old OTP accounts by year
- User balance management
- Automatic OTP retrieval upon purchase
- Navigation through available accounts
- Confirmation system for purchases
- Support for Two-Factor Authentication (2FA) accounts

# Deploy 
<div align="left">
  <a href="https://t.me/StackHost">
     <img src="https://graph.org/file/7e91d83f67d20f158cfdc.jpg" alt="Deploy On StackHost" width="150" />
  </a>
</div>


## Setup

1. Clone the repository:
   ```
   git clone https://github.com/your-username/otp-shop-bot.git
   cd otp-shop-bot
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your configuration:
   - Create a `config.py` file with your `API_ID` and `API_HASH` from the Telegram API
   - Set up your database connection in the `OTP/database/database.py` file

4. Run the bot:
   ```
   python bot.py
   ```

## Usage

1. Start a chat with the bot on Telegram
2. Use the /start command to begin
3. Navigate through the menu to browse available accounts
4. Select an account to purchase
5. Confirm your purchase
6. Receive the OTP for your purchased account

## Account Types

### Fresh Accounts
- Recently created accounts
- Available for immediate use

### Old Accounts
- Accounts from previous years
- Organized by year of creation
- May have established history

## Purchase Process

1. Select account type (fresh or old)
2. For old accounts, select the desired year
3. Browse available accounts
4. Select an account to purchase
5. Confirm the purchase
6. Bot retrieves the OTP automatically
7. OTP is displayed to the user

## Balance Management

- Users must have sufficient balance to make a purchase
- Balance is automatically deducted upon successful purchase

## OTP Retrieval

- The bot automatically retrieves the OTP using the account's session
- If 2FA is required, the user is notified to contact support

## Navigation

- Users can navigate through available accounts using "Previous" and "Next" buttons
- The current account number and price are displayed

## Additional Features

- Request new OTP for a purchased account
- Cancel a purchase before confirmation
- Automatic unlocking of numbers if a purchase fails or is cancelled

## Support

For any issues or questions, please contact our support team through the bot or open an issue in the GitHub repository.

## Disclaimer

This bot is for educational and demonstration purposes only. Ensure you comply with all relevant laws and regulations when using or modifying this bot.

## License

[MIT License](LICENSE)

