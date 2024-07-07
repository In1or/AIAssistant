from AIAssistant.AIAssistant import AIAssistantRemote
import telebot
import json
import time

class TelegramBot:
    def __init__(self, token):
        self.__bot = telebot.TeleBot(token)
        self.__assistant = AIAssistantRemote()
        self.__user_question = None


    def start(self):
        @self.__bot.message_handler(commands=['start'])
        def __send_welcome(message):
            self.__bot.send_message(message.chat.id, "Привет! \nНапиши нам свой вопрос, а мы постараемся на него ответить\nЕсли тебе что-то непонятно или есть вопросы по работе бота напиши команду /help")
            
            self.__bot.send_chat_action(message.chat.id, 'typing')
            time.sleep(1)            
            
            self.__bot.send_message(message.chat.id, "Что вы хотите узнать?")


        @self.__bot.message_handler(commands=['help'])
        def __handle_help(message):
            self.__bot.send_message(message.chat.id, "Тут будет помощь)")

        @self.__bot.message_handler(content_types=['audio', 'document', 'photo', 'sticker', 'video', 'video_note', 'voice', 'location', 'contact'])
        def __handle_media(message):
            self.__bot.send_message(message.chat.id, "Извините, я могу обрабатывать только текстовые сообщения.")


        @self.__bot.message_handler(func=lambda message: True)
        def __listen_and_response_all(message):
            answer = self.__send_request(message)
            self.__bot.send_message(message.chat.id, answer)
                
        self.__bot.polling()
        

    def __send_request(self, message):
        self.__user_question = {
            "username": message.from_user.username,
            "question": message.text,
            "user_firstname": message.from_user.first_name,
        }
        
        self.__bot.send_chat_action(message.chat.id, 'typing')
        answer  = self.__assistant.get_answer(self.__user_question)

        return answer



token = "7314438727:AAEWvm7XJScQMrAweLtlAFA7Vs1vxuTVIww"
bot = TelegramBot(token)
bot.start()