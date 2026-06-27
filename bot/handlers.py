from telegram import Update
from ai.agent import ai_client
from telegram.ext import ContextTypes
from config.settings import MODEL_NAME, MAX_TOKENS
from commands.commands import command_list, command_functions

async def handle_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
  print(f"Handling input: {update.message.text}")
  try:
    if update.message.text.startswith("/"):
      command = update.message.text.split(" ")[0].replace("/", "")
      await execute_command(update, context, command)
    else:
      await handle_message(update, context)
  except Exception as e:
    print(f"Error: {e}")
    await update.message.reply_text("Something went wrong, i'm not able to process this input")

async def execute_command(update: Update, context: ContextTypes.DEFAULT_TYPE, command: str):
  print(f"Executing command: {command}")
  try:
    if command in command_list():
          await command_functions()[command](update, context)
  except KeyError:
      await update.message.reply_text(f"Command {command} not found")
  except Exception as e:
      print(f"Error: {e}")
      await update.message.reply_text("Something went wrong, i'm not able to execute this command")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
  print(f"Handling message: {update.message.text}")
  try:
    response = ai_client.chat.completions.create(
      messages=[{"role": "user", "content": update.message.text}],
      model=MODEL_NAME,
      max_tokens=MAX_TOKENS
    )
    await update.message.reply_text(response.choices[0].message.content)
  except Exception as e:
    print(f"Error: {e}")
    await update.message.reply_text("Something went wrong, i'm not able to process this message")