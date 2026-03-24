from email.mime import message 
import os
import asyncio
import aiogram
from aiogram import Bot,Dispatcher,types
from aiogram.filters import Command
from aiogram import F  




from dotenv import load_dotenv

# import telegram token from .env file
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
# print(TELEGRAM_TOKEN)











bot=Bot(token=TELEGRAM_TOKEN)
dp=Dispatcher()



@dp.message(Command('start'))
async def start_command(message: types.Message):
    await message.reply("Hello bro welcome to the rohin bot! I can classify your card. Just send me a picture of your card and I'll tell you which card it is.")    


@dp.message(F.text)
async def chat_function(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing ")
    user_input = message.text.replace("/chat", "").strip()
    
    user_id=message.from_user.id
    if user_id not in chat_memory:
      chat_memory[user_id]=[
          {"role":"system","content":"you are an helpfull ai helper"}
      ]
    chat_memory[user_id].append({"role": "user","content": user_input})

    if not user_input:
        await message.reply("Please provide a message to chat with.")
        return  
    response = client.chat.completions.create(
     model="meta-llama/Meta-Llama-3-8B-Instruct",
     messages=chat_memory[user_id],
     
     max_tokens=400,
     temperature=0.7
   )


    reply =response.choices[0].message.content
    await message.reply(reply)
    chat_memory[user_id].append({"role":"assistant", "content": reply})
    

async def main():
    await dp.start_polling(bot)



#                              starting the bot
# if __name__ == "__main__":
#     import logging
#     logging.basicConfig(level=logging.INFO)
#     asyncio.run(main())
await main()