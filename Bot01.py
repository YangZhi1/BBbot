import logging
from telegram.ext import (Updater, MessageHandler, Filters, CommandHandler,ConversationHandler)
from DisplayOntoBoard import callingRGB
from Auth import restricted
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

CHOICE, TEXT, PHOTO, PROCESSTEXT, PROCESSPHOTO, FINISH, HELP = range(7)

# TODO: modularize the code by adding the commands to another file (not sure how to approach this)


# TODO: CURRENT BUGS: Once enter TEXT state cannot exit that state (Find out how to get out)
# TODO: Once we enter finish state and we send /start, we go back to start state but it doesn't send user the information message
# TODO: TEXT state user can enter input but bot doesn't do anything with it (FIX THIS)
# TODO: Change function names to include underscores ('_') between words (Not urgent)
'''
Start state
Gives simple list of commands, asks user to choose between a text or a photo
Goes to respective state (TEXT/PHOTO)
'''

message_to_show = ""
user_choice = ""

def choice(update, context):
    update.message.reply_text(
        'Hi! This is BBbot. '
        'For the list of commands available, type \'/\'\n'
        'For help, please type the command /help')
    return HELP

def help(update, context):
    update.message.reply_text(
        'List of commands:\n'
        '/text - send me the text you want to display on the LED\n'
        '/photo - send me a photo you want to display on the LED\n'
        '/escape - if you wish to quit the current command')

# by adding this @restricted above the function setText, we only allow specific userIDs to use the setText function
@restricted
def setText(update, context):
    update.message.reply_text('Please enter the text you wish to display, '
                              'or send /escape if you do not want to proceed with this action')
    print("inside set text")
    return PROCESSTEXT

@restricted
def setPhoto(update, context):
    update.message.reply_text('Please upload the photo you wish to display, '
                              'or send /escape if you do not want to proceed with this action')
    print("inside set photo")
    return PROCESSPHOTO


def processText(update, context):
    user = update.message.text
    print("User input text:", user)
    #newDisplay = callingRGB()
    #newDisplay.callrgb(user)

    # TODO: the next lines will not be executed, find out why and fix it
    # TODO: callingRGB() will stop the next few lines from executing. Need to find some way around this
    update.message.reply_text('Your message is received, please wait while it is being uploaded')
    update.message.reply_text('If the board is not updated, please give it a moment. \n'
                              'Otherwise, please reupload your message using /text. \n'
                              'Press /escape to use other commands.')
    message_to_show = user
    # TODO: message_to_show will store the user input text, so use it for the display
    print(message_to_show)
    print("inside processing text")
    return FINISH

def processPhoto(update, context):
    user = update.message.from_user
    photo_file = update.message.photo[-1].get_file()
    photo_file.download('user_photo.jpg')
    update.message.reply_text('Uploading photo...')
    logger.info("Photo of %s: %s", user.first_name, 'user_photo.jpg')
    # TODO: do something with the photo lol
    print("inside processing photo")
    return FINISH

def finish(update, context):
    update.message.reply_text('Bot is currently idle, please send a new command \n'
                              'like /text or /photo to start')
    print("inside finish")
    return CHOICE

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

'''
Main function to "start" the program
Will be using states like the example in https://github.com/python-telegram-bot/python-telegram-bot/blob/master/examples/conversationbot.py 
to decide what next for the bot
'''
def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary

    # PUT YOUR TELEGRAM TOKEN HERE
    updater = Updater("YOUR_TOKEN_HERE", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', choice)],

        states={
            CHOICE: [MessageHandler(Filters.regex('^(Text|Photo)$'), choice),
                    CommandHandler('text', setText),
                    CommandHandler('photo', setPhoto)],

            HELP: [MessageHandler(Filters.text, help),
                   CommandHandler('escape', finish),
                   CommandHandler('text', setText),
                   CommandHandler('photo', setPhoto)],

            TEXT: [MessageHandler(Filters.text, setText),
                   CommandHandler('escape', finish),
                   CommandHandler('start', choice)],

            PHOTO: [MessageHandler(Filters.text, setPhoto),
                    CommandHandler('escape', finish),
                    CommandHandler('start', choice)],

            PROCESSTEXT: [MessageHandler(Filters.text, processText),
                          CommandHandler('escape', finish),
                          CommandHandler('text', setText),
                          CommandHandler('start', choice)],

            PROCESSPHOTO: [MessageHandler(Filters.photo, processPhoto),
                           CommandHandler('escape', finish),
                           CommandHandler('start', choice)],

            FINISH: [CommandHandler('start', choice)]
        },

        fallbacks=[CommandHandler('escape', finish),
                   CommandHandler('start', choice),
                   CommandHandler('help', help)]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()


print("Logging...")
