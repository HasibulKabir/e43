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

b = raw_input("Enter message to broadcast: ")
f = open("chatids.txt", "r")
s = f.read().split('\n').split(":")[0]
f.close()

print("Broadcasting...")

for x in s:
  try:
    chat_id = int(x)
    bot.sendMessage(chat_id, b)
    time.sleep(1.5)
  except:
    pass

print("Done!")
