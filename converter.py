from telegram import Update
   from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
   import os

   def start(update: Update, context: CallbackContext):
       update.message.reply_text("Welcome! Send me a .txt file with name:link pairs.")

   def handle_file(update: Update, context: CallbackContext):
       file = update.message.document.get_file()
       file.download('input.txt')

       with open('input.txt', 'r') as f:
           lines = f.readlines()

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

       for line in lines:
           name, link = line.strip().split(':')
           html_content = html_content.replace("LINK_PLACEHOLDER", link)
           with open(f'{name}.html', 'w') as html_file:
               html_file.write(html_content)
           update.message.reply_document(document=open(f'{name}.html', 'rb'))
           os.remove(f'{name}.html')

       os.remove('input.txt')

   def main():
       token = "7782085620:AAG_ktDIMiH2DWIr0kO5DaeD8UjuTWOwN1U"
       updater = Updater(token, use_context=True)
       dp = updater.dispatcher

       dp.add_handler(CommandHandler("start", start))
       dp.add_handler(MessageHandler(Filters.document, handle_file))

       updater.start_polling()
       updater.idle()

   if __name__ == "__main__":
       main()
