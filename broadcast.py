import sys
import time
import telegram
import logging
from telegram.error import NetworkError, Unauthorized
import os

if 'TOKEN' in os.environ:
    TOKEN = os.environ.get('TOKEN')
else:
    TOKEN = ""
if 'ALLOWUNSUBS' in os.environ:
    ALLOWUNSUBS = os.environ.get('ALLOWUNSUBS')
else:
    ALLOWUNSUBS = 'TRUE'

print("Enter/Paste your broadcast. Ctrl-D or Ctrl-Z (Windows) to save it.")
contents = []
while True:
    try:
        line = input("")
    except EOFError:
        break
    contents.append(line)

b = "\n".join(contents)
f = open("chatids.txt", "r")
s = f.read()
f.close()
f = open("chatids2.txt", "r")
s = s + f.read()
f.close()
if not ALLOWUNSUBS == 'TRUE':
  f = open("subsoff.txt", "r")
  s = s + f.read()
  f.close()
s = s.split("\n")

print("Broadcasting...")

def handle(bot):
  for x in s:
    try:
      chat_id = int(x.split(":")[0])
      print(chat_id)
      if contents[0].startswith("http"):
        bot.sendPhoto(chat_id, contents[0], "\n".join(contents[1:]), parse_mode="Markdown")
      else:
        bot.sendMessage(chat_id, b, parse_mode="Markdown")
      time.sleep(1.5)
    except:
      pass

def main():
    global update_id
    bot = telegram.Bot(TOKEN)
    try:
        update_id = bot.get_updates()[0].update_id
    except IndexError:
        update_id = None

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    try:
        handle(bot)
    except NetworkError:
        time.sleep(1)
    except Unauthorized:
        update_id += 1

if __name__ == '__main__':
    main()

print("Done!")
