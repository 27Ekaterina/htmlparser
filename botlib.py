from os.path import exists
import telebot
from parser import parse
import time
from myfile import TOKEN

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.reply_to(message, "Привет!\n Готовы отправиться в незабываемое путешествие?\n Приступим к выбору тура!")

@bot.message_handler(commands=['help'])
def send_welcome(message):
	bot.reply_to(message, "@Tour_for_you_bot позволяет вывести подборку туров по региону с сайта https://youtravel.me/\n "
						  "Для этого используйте команды: \n "
						  "/parse - для начала поиска (пример: /parse altai) (выводится подборка из 5 туров);\n "
						  "/admin - с правами администратора осуществляется вывод всей подборки туров с интервалом 0,5 с (пример: /admin chukotka);\n "
						  "/file - позволяет получить файл, содержащий название тура, цену, количество дней, тип тура и ссылку на сайте в формате json;\n")

@bot.message_handler(commands=['parse'])
def parse_tours(message):
	text = message.text.split()[1]
	result = parse(text.lower())
	if len(result) != 0:
		for n in result[:5]:
			bot.send_message(message.chat.id, f'{n[0]} - {n[1]}')
	else:
		bot.send_message(message.chat.id, "Нет ответа от сайта. Попробуйте другое написание региона (например не baykal, а baikal).")



@bot.message_handler(commands=['admin'])
def admin(message):
	if message.from_user.username == 'EkaterinaGaydamakina':
		text = message.text.split()[1]
		result = parse(text.lower())
		if len(result) != 0:
			for n in result:
				time.sleep(0.5)
				bot.send_message(message.chat.id, f'{n[0]} - {n[1]}')
		else:
			bot.send_message(message.chat.id, "Нет ответа от сайта. Попробуйте другое написание региона (например не baykal, а baikal).")
	else:
		bot.reply_to(message, 'Метод недоступен, нет прав')

@bot.message_handler(commands=['file'])
def send_file(message):
	if exists('htmlparsing.json'):
		with open('htmlparsing.json') as f:
			bot.send_document(message.chat.id, f)
	else:
		bot.send_message(message.chat.id, 'Файл отсутствует. Сначала воспользуйтесь командой /parse для формирования файла с результатом поиска.')

@bot.message_handler(content_types=['sticker'])
def send_sticker(message):
	FILE_ID = 'CAACAgIAAxkBAAO4YtRkslFghtQmjKjfRAtdpwGHUz4AAvUTAALaMaFLiGee62_s1rYpBA'
	bot.send_sticker(message.chat.id, FILE_ID)

@bot.message_handler(content_types='text')
def reverse_text(message):
	text = message.text[::-1]
	bot.reply_to(message, f'<<>>{text.upper()}!<<>>\n Воспользуйтесь командой /help для подсказки по поиску туров:)')

bot.infinity_polling()