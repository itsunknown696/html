from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import os

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Welcome! Send me a .txt file with name:link pairs.")

def handle_file(update: Update, context: CallbackContext):
    # Download the file sent by the user
    file = update.message.document.get_file()
    file.download('input.txt')

    # Read the file and process each line
    with open('input.txt', 'r') as f:
        lines = f.readlines()

    # HTML template with a stylish UI
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Video Player</title>
        <style>
            body { background: linear-gradient(135deg, #1e1e1e, #3a3a3a); color: white; font-family: Arial, sans-serif; margin: 0; padding: 20px; }
            h1 { color: #bb86fc; }
            video { width: 100%; max-width: 800px; margin: 20px 0; }
            .controls { display: flex; gap: 10px; margin-top: 10px; }
            button { background: #bb86fc; border: none; padding: 10px 20px; color: white; cursor: pointer; border-radius: 5px; }
            button:hover { background: #9a67ea; }
        </style>
    </head>
    <body>
        <h1>Video Player</h1>
        <video id="videoPlayer" controls>
            <source src="LINK_PLACEHOLDER" type="video/mp4">
            Your browser does not support the video tag.
        </video>
        <div class="controls">
            <button onclick="skip(-10)">⏪ Skip -10s</button>
            <button onclick="skip(10)">⏩ Skip +10s</button>
            <button onclick="changeSpeed(0.5)">0.5x</button>
            <button onclick="changeSpeed(1)">1x</button>
            <button onclick="changeSpeed(1.5)">1.5x</button>
            <button onclick="changeSpeed(2)">2x</button>
        </div>
        <script>
            const video = document.getElementById('videoPlayer');
            function skip(seconds) { video.currentTime += seconds; }
            function changeSpeed(speed) { video.playbackRate = speed; }
        </script>
    </body>
    </html>
    """

    # Process each line in the file
    for line in lines:
        name, link = line.strip().split(':')
        # Replace the placeholder with the actual link
        updated_html = html_content.replace("LINK_PLACEHOLDER", link)
        # Save the HTML file
        with open(f'{name}.html', 'w') as html_file:
            html_file.write(updated_html)
        # Send the HTML file back to the user
        update.message.reply_document(document=open(f'{name}.html', 'rb'))
        # Clean up the generated HTML file
        os.remove(f'{name}.html')

    # Clean up the input file
    os.remove('input.txt')

def main():
    # Replace with your Telegram bot token (use environment variables for security)
    token = os.getenv("7782085620:AAG_ktDIMiH2DWIr0kO5DaeD8UjuTWOwN1U")
    if not token:
        print("Error: Telegram bot token not found. Please set the TELEGRAM_BOT_TOKEN environment variable.")
        return

    updater = Updater(token, use_context=True)
    dp = updater.dispatcher

    # Add handlers for commands and file uploads
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.document, handle_file))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
