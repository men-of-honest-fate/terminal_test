from telebot import TeleBot, types, custom_filters
from telebot.handler_backends import State, StatesGroup
from telebot.storage import StateMemoryStorage
from settings import get_settings
import requests

class MyStates(StatesGroup):
    wait_for_button = State()
    wait_for_summ = State()


class Bot:
    def __init__(self):
        self.state_storage = StateMemoryStorage()
        self.token = get_settings().BOT_TOKEN
        self.bot = TeleBot(self.token, state_storage=self.state_storage)
        self.markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        self.button1 = types.KeyboardButton("Оплатить")
        self.button2 = types.KeyboardButton("Отмена")
        self.api_url = get_settings().API_URL

        @self.bot.message_handler(commands=["start"])
        def start_message(message):
            self.markup.add(self.button1, self.button2)
            self.bot.set_state(message.from_user.id, MyStates.wait_for_button, message.chat.id)
            self.bot.send_message(
                message.chat.id,
                '''Я - телеграм бот, помощник для автоматизации работы терминалов.\nДля начала работы нажмите на кнопку "Оплатить"''',
                reply_markup=self.markup,
            )

        @self.bot.message_handler(state=MyStates.wait_for_button)
        def button_message(message):
            if message.text == "Оплатить":
                self.markup = types.ReplyKeyboardRemove()
                self.markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                self.markup.add(self.button2)

                self.bot.set_state(message.from_user.id, MyStates.wait_for_summ, message.chat.id)
                self.bot.send_message(
                    message.chat.id, "Для оплаты введите сумму", reply_markup=self.markup
                )
            elif message.text == "Отмена":
                self.bot.send_message(message.chat.id, "Ваша оплата была отменена. \nДля того чтобы оплатить снова нажмите кнопку оплатить", reply_markup=self.markup)
                self.bot.set_state(message.from_user.id, MyStates.wait_for_button, message.chat.id)

        @self.bot.message_handler(state=MyStates.wait_for_summ)
        def cancel_payment(message):
            if message.text.isdigit():
                self.bot.send_message(message.chat.id, "Ваша оплата была принята в обработку. Скоро мы отправим Вам QR код СБП")
                try:
                    response = requests.post(f"http://{self.api_url}/purchase/{int(message.text)}")
                    self.bot.send_message(message.chat.id, response.text)
                except Exception as e:
                    print(e)
                    self.bot.send_message(message.chat.id, "Сервер недоступен, повторите попытку позже")
            else:
                if message.text == "Отмена":
                    self.markup.add(self.button1)
                    self.bot.send_message(message.chat.id, "Ваша оплата была отменена. \nДля того чтобы оплатить снова нажмите кнопку оплатить", reply_markup=self.markup)
                    self.bot.set_state(message.from_user.id, MyStates.wait_for_button, message.chat.id)
                else:
                    self.bot.send_message(message.chat.id, "Введена неверная сумма для оплаты. Повторите попытку")

    def run(self):
        self.bot.add_custom_filter(custom_filters.StateFilter(self.bot))
        self.bot.add_custom_filter(custom_filters.IsDigitFilter())
        self.bot.infinity_polling()


Bot = Bot()
Bot.run()
