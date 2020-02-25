from telegram import (ReplyKeyboardMarkup, KeyboardButton)
from telegram.ext import (Updater, CommandHandler, MessageHandler,
                          ConversationHandler, PicklePersistence)
from telegram.ext.filters import (Filters)
import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

SERVICE, SUB_SERVICE, LOCATION, PHONENUM, ORDER = range(5)

localities_reply_keyboard = [['1. Addis Ketema', '2. Akaki Kality', '3. Arada'],
                  ['4. Bole', '5. Gulele', '6. Kirkos'], 
                  ['7. Kolfe Keranyo', '8. Lideta', '9. Nifas Silk Lafto'],
                  ['10. Yeka', 'cancel']]

services_reply_keyboard = [['Cleaning', 'Tap and Sinks'],
                  ['Drains','Electrical Faults'], 
                  ['Electrical Appliances', 'Finishing'],
                  ['cancel']]

sub_services_reply_keyboard_1 = [['cleaning 1', 'cleaning 2'], ['clearning 3','cleaning 4'], ['cancel']]
sub_services_reply_keyboard_2 = [['Tap and Sinks 1', 'Tap and Sinks 2'], ['Tap and Sinks 3','Tap and Sinks 4'], ['cancel']]
sub_services_reply_keyboard_3 = [['Drains 1', 'Drains 2'], ['Drains 3','Drains 4'], ['cancel']]
sub_services_reply_keyboard_4 = [['Electrical Faults 1', 'Electrical Faults 2'], ['cancel']]
sub_services_reply_keyboard_5 = [['Electrical Appliances 1', 'Electrical Appliances 2'], ['cancel']]
sub_services_reply_keyboard_6 = [['Finishing 1', 'Finishing 2'], ['Finishing 3','Finishing 4'], ['Finishing 5', 'Finishing 6'], ['cancel']]

services_markup = ReplyKeyboardMarkup(services_reply_keyboard, one_time_keyboard=True)
localities_markup = ReplyKeyboardMarkup(localities_reply_keyboard, one_time_keyboard=True)
# sub_services_markup = ReplyKeyboardMarkup(sub_services_reply_keyboard, one_time_keyboard=True)
# location_keyboard = KeyboardButton(text="send_location",  request_location=True)
# location_markup = ReplyKeyboardMarkup(location_keyboard)

def facts_to_str(user_data):
    facts = list()

    for key, value in user_data.items():
        facts.append('{} - {}'.format(key, value))

    return "\n".join(facts).join(['\n', '\n'])

def start(update, context):
    # reply_keyboard = [['Services', 'Change Language']]
    reply_keyboard = [['Services']]
    reply_text = "Hello! Welcome to Taskmoby."
    
    # logger.info('1 >>>>>>> {} \n'.format(context.user_data,))
    if context.user_data:
        reply_text += " You already used our service before {}.".format(", ".join(context.user_data.keys()))
    else:
        reply_text += " I will help you request the right service from Taskmoby."
    update.message.reply_text(reply_text, reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    # logger.info('2 >>>>>>> {} \n'.format(context.user_data,))

    # return ConversationHandler.END
    return SERVICE

def services(update, context):
    text = update.message.text.lower()
    context.user_data['choice'] = text
    # logger.info('>> {} \n >> {}'.format(text, context.user_data.get(text)))
    if context.user_data.get(text):
        reply_text = 'You requested for {} service.'.format(text)
    else:
        reply_text = 'please pick a sevice type.'

    update.message.reply_text(reply_text, reply_markup=services_markup)
    # update.message.reply_text(reply_text)

    return SUB_SERVICE

def sub_services(update, context):
    text = update.message.text.lower()
    context.user_data['service'] = text
    if context.user_data.get(text):
        reply_text = 'You requested for {} sub-service'.format(text, context.user_data[text])
    else:
        reply_text = 'You requested for {} service.'.format(text)

    logger.info(text)

    if text == 'cleaning':
        sub_services_markup = ReplyKeyboardMarkup(sub_services_reply_keyboard_1, one_time_keyboard=True)
    elif text == 'tap and sinks':
        sub_services_markup = ReplyKeyboardMarkup(sub_services_reply_keyboard_2, one_time_keyboard=True)
    elif text == 'drains':
        sub_services_markup = ReplyKeyboardMarkup(sub_services_reply_keyboard_3, one_time_keyboard=True)
    elif text == 'electrical faults':
        sub_services_markup = ReplyKeyboardMarkup(sub_services_reply_keyboard_4, one_time_keyboard=True)
    elif text == 'electrical appliances':
        sub_services_markup = ReplyKeyboardMarkup(sub_services_reply_keyboard_5, one_time_keyboard=True)
    elif text == 'finishing':
        sub_services_markup = ReplyKeyboardMarkup(sub_services_reply_keyboard_6, one_time_keyboard=True)


    update.message.reply_text(reply_text, reply_markup=sub_services_markup)

    return LOCATION

def get_location(update, context):
    # logger.info('>> {} \n >>'.format(update.message))
    text = update.message.text.lower()
    context.user_data['sub-service'] = text
    # if context.user_data.get(text):
        # reply_text = 'You requested for {} service'.format(text)
    # else:
        # reply_text = 'please pick a sevice type.'

    reply_text = 'Your locality?'
    update.message.reply_text(reply_text, reply_markup=localities_markup)
    # update.message.reply_text(reply_text)

    return PHONENUM

def get_contact(update, context):
    text = update.message.text.lower()
    context.user_data['locality'] = text

    contact_keyboard = KeyboardButton(text="Share Contact", request_contact=True)
    custom_keyboard = [[ contact_keyboard ], ['cancel']]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard)

    reply_text = 'Would you mind sharing your contact?'
    update.message.reply_text(reply_text, reply_markup=reply_markup)

    return ORDER

def do_order(update, context):
    # logger.info('test: >>> {}\n\n\n'.format(update.message.contact.phone_number))
    text = update.message.contact.phone_number
    context.user_data['contact'] = text

    logger.info('update: >>> {}'.format(context.user_data))

    update.message.reply_text('Thank you! One of our customer service personnel will contact you soon!.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END
    

def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s cancelled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END

def show_data(update, context):
    update.message.reply_text("This is what you already told me:"
                              "{}".format(facts_to_str(context.user_data)))

def done(update, context):
    if 'choice' in context.user_data:
        del context.user_data['choice']

    update.message.reply_text("I learned these facts about you:"
                              "{}"
                              "Until next time!".format(facts_to_str(context.user_data)))
    return ConversationHandler.END

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" \n\n caused error "%s"', update, context.error)

def main():
    # Create the Updater and pass it your bot's token.
    pp = PicklePersistence(filename='conversationbot')
    updater = Updater("1034923193:AAH4CjqTWTmXbzhrJm5q2FlupNLrMIwFHAg", persistence=pp, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            SERVICE: [MessageHandler(Filters.text, services),
                    CommandHandler('cancel', cancel)],
            SUB_SERVICE: [MessageHandler(Filters.text, sub_services),
                    CommandHandler('cancel', cancel)],
            LOCATION: [MessageHandler(Filters.text, get_location),
                    CommandHandler('cancel', cancel)],
            PHONENUM: [MessageHandler(Filters.text, get_contact),
                    CommandHandler('cancel', cancel)],
            ORDER: [MessageHandler(Filters.contact, do_order),
                    CommandHandler('cancel', cancel)],
        },
        # fallbacks=[MessageHandler(Filters.regex('^Done$'), done)],
        fallbacks=[CommandHandler('cancel', cancel)],
        # name="my_conversation",
        # persistent=True
    )

    dp.add_handler(conv_handler)

    # cancel_handler = CommandHandler('Cancel', cancel)
    # dp.add_handler(cancel_handler)
    
    # show_data_handler = CommandHandler('show_data', show_data)
    # dp.add_handler(show_data_handler)

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