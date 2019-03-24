from qiwi_api import Qiwi

token = input("Enter QiwiApi token: ")

api = Qiwi(token)

#получаем баланс, информацию о идентификации и кошельке
balance = api.balance(only_balance=True)
ident = api.get_identification()
info = api.get_profile(auth_info=True, contract_info=True, user_info=True)



#обрабатываем полученный запрос валюты
def qiwi_balance(inp):
 re = {}
 for bal in inp:
  if "qw_wallet_rub" in bal:
   re["rub"] = bal["qw_wallet_rub"]
  elif "qw_wallet_usd" in bal:
   re["usd"] = bal["qw_wallet_usd"]
  elif "qw_wallet_kzt" in bal:
   re["kzt"] = bal["qw_wallet_kzt"]
  elif "qw_wallet_eur" in bal:
   re["eur"] = bal["qw_wallet_eur"]
 return re

#просто красивенькая замена пиндоских слов на понятные русские
if ident["type"] == 'SIMPLE':
	ident["type"] = 'Основной ограниченный'
if ident["type"] == 'VERIFIED':
	ident["type"] = 'Основной'
if ident["type"] == 'FULL':
	ident["type"] = 'Профессиональный'



#выводим в терминал всю инфу которую получили в результате трех реквестов
print("Номер телефона: " + "+" + str(ident["id"]))
print("Статус кошелька: " + str(ident["type"]))
#если статус минимальный, то выводить ничего не будем, т.к. все значения будут 'None'
if ident["type"] != 'Основной ограниченный':
	print("Паспорт: " + str(ident["passport"]))
	print("Имя: " + str(ident["firstName"]))
	print("Фамилия: " + str(ident["lastName"]))
	print("Отчество: " + str(ident["middleName"]))
	print("Дата рождения: " + str(ident["birthDate"]))
	print("ИНН: " + str(ident["inn"]))
	print("СНИЛС: " + str(ident["snils"]))
	print("ОМС: " + str(ident["oms"]))
print("Баланс RUB: " + str(qiwi_balance(balance)["rub"]) + "₽")
print("Баланс USD: " + str(qiwi_balance(balance)["usd"]) + "$")

#небольшая проверка, если счетов не существует - скрипт не дропнет ошибку ($ и ₽ есть по умолчанию) 
try:
	print("Баланс KZT: " + str(qiwi_balance(balance)["kzt"]) + "₸")
except:
	print("Баланс KZT: Не создан")
try:
	print("Баланс EUR: " + str(qiwi_balance(balance)["eur"]) + "€")
except:
	print("Баланс EUR: Не создан")


print("SMS Подтверждение: " + str(info["contractInfo"]["smsNotification"]["enabled"]))
print("Дата Регистрации: " + str(info["contractInfo"]["creationDate"]))
print("Заблокирован: " + str(info["contractInfo"]["blocked"]))
print("Email: " + str(info["authInfo"]["boundEmail"]))
print("Email подтверждение: " + str(info["authInfo"]["emailSettings"]["use-for-security"]))
print("IP: " + str(info["authInfo"]["ip"]))

print("\n")
#Выводим всё в файлик, слишком легкая конструкция
makefile = input("Сохранить результаты в файл? (y/n): ")
if makefile == "y":
	outputfile = open(str(token) + '#qiwi-checker' + '.txt', 'w')
	outputfile.write("Токен: " + token + "\n")
	outputfile.write("Номер телефона: " + "+" + str(ident["id"]) + "\n")
	outputfile.write("Статус кошелька: " + str(ident["type"]) + "\n")
	if ident["type"] != 'Основной ограниченный':
		outputfile.write("Паспорт: " + str(ident["passport"]) + "\n")
		outputfile.write("Имя: " + str(ident["firstName"]) + "\n")
		outputfile.write("Фамилия: " + str(ident["lastName"]) + "\n")
		outputfile.write("Отчество: " + str(ident["middleName"]) + "\n")
		outputfile.write("Дата рождения: " + str(ident["birthDate"]) + "\n")
		outputfile.write("ИНН: " + str(ident["inn"]) + "\n")
		outputfile.write("СНИЛС: " + str(ident["snils"]) + "\n")
		outputfile.write("ОМС: " + str(ident["oms"]) + "\n")
	outputfile.write("SMS Подтверждение: " + str(info["contractInfo"]["smsNotification"]["enabled"]) + "\n")
	outputfile.write("Дата Регистрации: " + str(info["contractInfo"]["creationDate"]) + "\n")
	outputfile.write("Заблокирован: " + str(info["contractInfo"]["blocked"]) + "\n")	
	outputfile.write("Баланс RUB: " + str(qiwi_balance(balance)["rub"]) + "₽" + "\n")
	outputfile.write("Баланс USD: " + str(qiwi_balance(balance)["usd"]) + "$" + "\n")
	try:
		outputfile.write("Баланс KZT: " + str(qiwi_balance(balance)["kzt"]) + "₸" + "\n")
	except:
		outputfile.write("Баланс KZT: Не создан" + "\n")
	try:
		outputfile.write("Баланс EUR: " + str(qiwi_balance(balance)["eur"]) + "€" + "\n")
	except:
		outputfile.write("Баланс EUR: " + "Не создан" + "\n")
	outputfile.write("Email: " + str(info["authInfo"]["boundEmail"]) + "\n")
	outputfile.write("Email подтверждение: " + str(info["authInfo"]["emailSettings"]["use-for-security"]) + "\n")
	outputfile.write("IP: " + str(info["authInfo"]["ip"]) + "\n")
	outputfile.close()
	print("Success.")
	
elif makefile == "n":
	print("Exiting....")
	exit()
