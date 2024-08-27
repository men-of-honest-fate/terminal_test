from telebot import TeleBot, types, custom_filters
from telebot.handler_backends import State, StatesGroup
from telebot.storage import StateMemoryStorage
from settings import get_settings
import requests
import hashlib
class MyStates(StatesGroup):
    wait_for_button = State()
    wait_for_summ = State()
    wait_for_login = State()
    wait_for_password = State()
    wait_for_changing = State()
    wait_for_changing_login_or_password = State()
class Bot:
    def __init__(self):
        self.login_hash: str
        self.password_hash: str
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
                reply_markup=self.markup, # дописать пользователю ручку для апдейта пароля или логина
            )
        @self.bot.message_handlers(commands = ["authorize"])
        def authorisation_start(message):
            if message.text == "Авторизоваться":
                self.bot.send_message(
                    message.chat.id, "Введите логин", reply_markup=self.markup
                )
                self.bot.set_state(message.from_user.id, MyStates.wait_for_login, message.chat.id)

        @self.bot.message_handler(state=MyStates.wait_for_login)
        def login_hashing(message):
                self.login_hash = hashlib.sha512(message.encode()).hexdigest()
                self.bot.send_message(message.chat.id, "Логин принят", reply_markup=self.markup)
                self.bot.set_state(message.from_user.id, MyStates.wait_for_password, message.chat.id)
                self.bot.send_message(
                message.chat.id, "Введите пароль", reply_markup=self.markup)
        @self.bot.message_handler(state = MyStates.wait_for_password)
        def password_hashing(message):
            self.password_hash = hashlib.sha512(message.encode()).hexdigest()
            self.bot.send_message(message.chat.id, "Пароль принят", reply_markup=self.markup)
            response = requests.post(f"{self.api_url}/authorize", data = {"input_login":self.login_hash, "input_password":self.password_hash})
            if response.status_code == 200:
                self.bot.send_message(message.chat.id, f"Данные приняты, Ваш токен сессии {response.request}", reply_markup=self.markup)
            else: 
                   self.bot.send_message(message.chat.id, "Вы незарегестрированы", reply_markup=self.markup)
            self.bot.set_state(message.from_user.id, MyStates.wait_for_changing, message.chat.id)
        @self.bot.message_handler(state = MyStates.wait_for_changing)
        def changing_data(message):
            self.bot.send_message(message.chat.id, "Хотите сменить логин или пароль?", reply_markup=self.markup)
            self.bot.send_message(message.chat.id, "Тогда введите токен одной из прошлых сессий", reply_markup=self.markup)
            response = requests.post(f"{self.api_url}/check_token", data = {"token":message})
            if response.status_code ==200:
                self.bot.set_state(message.chat.id, MyStates.wait_for_changing_login_or_password, message.chat.id)
            else: 
                self.bot.send_message(message.chat.id, "Ваш токен неверен", message.chat.id)
        @self.bot.message_handler(state = MyStates.wait_for_changing_login_or_password)
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
