import sys
import time
import telepot
import os
from telepot.loop import MessageLoop

if 'TOKEN' in os.environ:
    TOKEN = os.environ.get('TOKEN')
else:
    TOKEN = ""

bot = telepot.Bot(TOKEN)

print("Enter/Paste your broadcast. Ctrl-D or Ctrl-Z (Windows) to save it.")
contents = []
while True:
    try:
        line = raw_input("")
    except EOFError:
        break
    contents.append(line)

b = "\n".join(contents)
f = open("chatids.txt", "r")
s = f.readlines()
f.close()

print("Broadcasting...")

for x in s:
  try:
    chat_id = int(x.split(":")[0])
    print(chat_id)
    if contents[0].startswith("http"):
      bot.sendPhoto(chat_id, contents[0], "\n".join(contents[1:]))
    else:
      bot.sendMessage(chat_id, b)
    time.sleep(1.5)
  except:
    pass

print("Done!")
