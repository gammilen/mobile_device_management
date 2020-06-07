from mailmerge import MailMerge
import datetime
from docx2pdf import convert
import locale
from num2words import num2words
import os 
import sys


locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8') 

sys.path.append('../1/')
sys.path.append('../2/')

def internet():
    from script import prepare_charging, get_payment
    print("Получение данных об услуге 'Интернет'")
    c = prepare_charging()
    p = get_payment(c)
    print("Данные получены")
    return p

def tel():
    from program import calculate_tel
    print("Получение данных об услуге 'Телефония'")
    p = calculate_tel()
    print("Данные получены")
    return p

payment_int = round(internet(), 2)
payment_tel = round(tel(), 2)
full = payment_int + payment_tel

def form_full_num(number):
    import math
    from num2words import num2words
    cop, rub = math.modf(number)
    cop = round(cop*100)
    rub = int(rub)
    rub_num = num2words(rub, lang='ru')
    cop_num = num2words(cop, lang='ru')
    last_rub = rub % 10
    last_cop = cop % 10
    cops = {
        0: "копеек",
        1: "копейка",
        2: "копейки",
        3: "копейки",
        4: "копейки",
        5: "копеек",
        6: "копеек",
        7: "копеек",
        8: "копеек",
        9: "копеек",
    }
    rubs = {
        0: "рублей",
        1: "рубль",
        2: "рубля",
        3: "рубля",
        4: "рубля",
        5: "рублей",
        6: "рублей",
        7: "рублей",
        8: "рублей",
        9: "рублей",
    }
    return rub_num + " " + rubs[last_rub] + " " + cop_num + " " + cops[last_cop] + "."

print("Начата подготовка документа")
template = "template.docx"
doc = MailMerge(template)
doc.merge(
    year_00=str(datetime.datetime.now().year)[2:],
    bank_recipient="АО 'Стоун банк' г.Москва",
    accountant_fio="Семенов В.А.",
    account_number="82",
    month=datetime.datetime.now().strftime("%b"),
    full_payment=form_full_num(full),
    account2="40703810900000002353",
    day=str(datetime.datetime.now().day),
    provider="ООО 'Василек', ИНН 7722737733, КПП 773303001, 109052, Москва г., Добрынинская ул., дом 70, корпус 2",
    price_tel=str(payment_tel).replace(".", ","),
    kpp_recipient="772303001",
    head_fio="Семенов В.А.",
    base="№ 20023316 от 13.02.2020",
    recipient="ООО 'Василек'",
    bik_recipient="044525703",
    account1="30101810200000000300",
    price_internet=str(payment_int).replace(".", ","),
    inn_recipient="7722737363",
    customer_full="ООО Лагуна, ИНН 7714037338, КПП 777550001, 119361, Москва г., Тульская М ул., дом 4, строение 1",
)
doc.write("test-output.docx")
print("Сформирован временный файл")
convert("test-output.docx", "output.pdf")
print("Сформирован итоговый .pdf файл")

os.remove("test-output.docx")