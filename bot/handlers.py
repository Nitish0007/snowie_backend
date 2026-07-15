from telegram import Update
from ai.agent import ai_client
from telegram.ext import ContextTypes
from config.settings import MODEL_NAME, MAX_TOKENS
from commands.commands import command_list, command_functions

from ai.router import AIRouter
from plugins.registry import build_plugins
from bot.conversation import get_history, append_turn
import traceback
router = AIRouter(build_plugins())

async def handle_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
  print(f"Handling input: {update.message.text}")
  try:
    if update.message.text.startswith("/"):
      command = update.message.text.split(" ")[0].replace("/", "")
      await execute_command(update, context, command)
    else:
      await handle_message(update, context)
  except Exception as e:
    print(f"Error in handle_input: {traceback.format_exc()}")
    await update.message.reply_text("Something went wrong, i'm not able to process this input")

async def execute_command(update: Update, context: ContextTypes.DEFAULT_TYPE, command: str):
  print(f"Executing command: {command}")
  try:
    if command in command_list():
          await command_functions()[command](update, context)
  except KeyError:
      await update.message.reply_text(f"Command {command} not found")
  except Exception as e:
      print(f"Error in execute_command: {traceback.format_exc()}")
      await update.message.reply_text("Something went wrong, i'm not able to execute this command")

async def handle_message(update, context):
    try:
      user_text = update.message.text
      history = get_history(context)
      reply = await router.route(user_text, history=history)
      append_turn(context, user_text, reply)
      print(f"-===================================================================")
      print(f"History: {history}")
      print(f"Reply: {reply}")
      print(f"User text: {user_text}")
      print(f"-===================================================================")
      await update.message.reply_text(reply)
    except Exception as e:
      print(f"Error in handle_message: {traceback.format_exc()}")
      await update.message.reply_text("Something went wrong, i'm not able to process this message")