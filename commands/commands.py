from telegram import Update
from telegram.ext import ContextTypes

def command_list() -> list[str]:
  return command_functions().keys()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
  await update.message.reply_text("Heyy! Snowie is here buddy, what you want today?")

async def schedule(update: Update, context: ContextTypes.DEFAULT_TYPE):
  await update.message.reply_text("Command not supported yet")

def command_functions():
  return {
  "start": start,
  "schedule": schedule
}