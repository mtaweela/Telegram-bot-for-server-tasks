from telebot import types
from decouple import config
import telebot
from settings import configurations
from aws_handlers import Ec2Servers


TELEGRAM_TOKEN = config("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = config("TELEGRAM_CHAT_ID")

bot = telebot.TeleBot(TELEGRAM_TOKEN, parse_mode=None)


@bot.message_handler(commands=['start', 'help'])
def start_help(message):
    bot.send_message(message.chat.id, """
you can use one of the commands below:
/start - get help
/help - get help
/restart_ec2
/stop_ec2
/start_ec2
    """
                     )


# ........................   REBOOT INSTANCES ........................


@bot.message_handler(commands=['restart_ec2'])
def restart_ec2(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)

    buttons = [
        "/confirm_restart_ec2 %s" % (item)
        for item in configurations.get("ec2").keys()
    ]

    for i in buttons:
        itembtna = types.KeyboardButton(i)
        markup.row(itembtna)

    bot.send_message(TELEGRAM_CHAT_ID, "Choose one:", reply_markup=markup)


@bot.message_handler(commands=['confirm_restart_ec2'])
def confirm_restart_ec2(message):
    command, instance_name = message.text.rsplit(" ", 1)
    r = Ec2Servers(
        configurations.get("ec2").get(instance_name)
    ).reboot()
    bot.reply_to(message, "Done !! %s" % (r))

# ........................   STOP INSTANCES ........................


@bot.message_handler(commands=['stop_ec2'])
def stop_ec2(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)

    buttons = [
        "/confirm_stop_ec2 %s" % (item)
        for item in configurations.get("ec2").keys()
    ]

    for i in buttons:
        itembtna = types.KeyboardButton(i)
        markup.row(itembtna)

    bot.send_message(TELEGRAM_CHAT_ID, "Choose one:", reply_markup=markup)


@bot.message_handler(commands=['confirm_stop_ec2'])
def confirm_stop_ec2(message):
    command, instance_name = message.text.rsplit(" ", 1)
    r = Ec2Servers(
        configurations.get("ec2").get(instance_name)
    ).stop()
    bot.reply_to(message, "Done !! %s" % (r))


# ........................   START INSTANCES ........................

@bot.message_handler(commands=['start_ec2'])
def start_ec2(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)

    buttons = [
        "/confirm_start_ec2 %s" % (item)
        for item in configurations.get("ec2").keys()
    ]

    for i in buttons:
        itembtna = types.KeyboardButton(i)
        markup.row(itembtna)

    bot.send_message(TELEGRAM_CHAT_ID, "Choose one:", reply_markup=markup)


@bot.message_handler(commands=['confirm_start_ec2'])
def confirm_start_ec2(message):
    command, instance_name = message.text.rsplit(" ", 1)
    r = Ec2Servers(
        configurations.get("ec2").get(instance_name)
    ).start()
    bot.reply_to(message, "Done !! %s" % (r))


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.send_message(TELEGRAM_CHAT_ID, "message ..")


bot.infinity_polling()
