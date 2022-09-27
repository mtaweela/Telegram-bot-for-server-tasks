from telebot import types
from decouple import config
import telebot
from settings import configurations
from aws_handlers import Ec2Servers


TELEGRAM_TOKEN = config("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = config("TELEGRAM_CHAT_ID")

bot = telebot.TeleBot(TELEGRAM_TOKEN, parse_mode=None)


def auth_middleware_handler(handler):
    def decorator(message):
        if str(message.chat.id) == TELEGRAM_CHAT_ID:
            return handler(message)

        bot.reply_to(message, "stop playing !!")

    return decorator


@bot.message_handler(commands=['start', 'help'])
@auth_middleware_handler
def start_help(message):
    bot.send_message(message.chat.id, """
you can use one of the commands below:
/start - get help
/help - get help
/status_ec2
/restart_ec2
/stop_ec2
/start_ec2
    """
                     )


# ........................   REBOOT INSTANCES ........................


@bot.message_handler(commands=['restart_ec2'])
@auth_middleware_handler
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
@auth_middleware_handler
def confirm_restart_ec2(message):
    command, instance_name = message.text.rsplit(" ", 1)
    r = Ec2Servers(
        configurations.get("ec2").get(instance_name)
    ).reboot()
    bot.reply_to(message, "Done !! %s" % (r))

# ........................   STOP INSTANCES ........................


@bot.message_handler(commands=['stop_ec2'])
@auth_middleware_handler
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
@auth_middleware_handler
def confirm_stop_ec2(message):
    command, instance_name = message.text.rsplit(" ", 1)
    r = Ec2Servers(
        configurations.get("ec2").get(instance_name)
    ).stop()
    bot.reply_to(message, "Done !! %s" % (r))


# ........................   START INSTANCES ........................

@bot.message_handler(commands=['start_ec2'])
@auth_middleware_handler
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
@auth_middleware_handler
def confirm_start_ec2(message):
    command, instance_name = message.text.rsplit(" ", 1)
    r = Ec2Servers(
        configurations.get("ec2").get(instance_name)
    ).start()
    bot.reply_to(message, "Done !! %s" % (r))


# ........................   INSTANCES STATUS ........................

@bot.message_handler(commands=['status_ec2'])
@auth_middleware_handler
def status_ec2(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)

    buttons = [
        "/confirm_status_ec2 %s" % (item)
        for item in configurations.get("ec2").keys()
    ]

    for i in buttons:
        itembtna = types.KeyboardButton(i)
        markup.row(itembtna)

    bot.send_message(TELEGRAM_CHAT_ID, "Choose one:", reply_markup=markup)


@bot.message_handler(commands=['confirm_status_ec2'])
@auth_middleware_handler
def confirm_status_ec2(message):
    command, instance_name = message.text.rsplit(" ", 1)
    r = Ec2Servers(
        configurations.get("ec2").get(instance_name)
    ).status()
    bot.reply_to(message, "Done !! %s" % (r))

# ........................   ECHO ALL ........................


@bot.message_handler(func=lambda m: True)
@auth_middleware_handler
def echo_all(message):
    bot.reply_to(message, "Hello, do /start")


bot.infinity_polling()
