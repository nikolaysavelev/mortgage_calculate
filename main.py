import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from datetime import date

#TODO: ask about input this variable
property_value = int(input('Введите стоимость недвижимости (руб.): '))

#TODO: ask about input this variable
loan_term_year = int(input('Введите срок ипотеки (лет): '))
loan_term_month = loan_term_year * 12 # transit to months

#TODO: ask about input this variable
start_capital = int(input('Введите первоначальный взнос (руб.): '))

#TODO: in future, ask about influence
#type_of_building = input('Введите тип жилья (новостройка / вторичка / гараж): ')

#TODO : choose bank by inline-button
bank_name = input('Выберите банк, в котором хотите взять ипотеку: ')

#TODO: choose interest_rate from google spreadsheet
if bank_name == 'Зеленый банк':
    interest_rate = 8.6
elif bank_name == 'Синий банк':
    interest_rate = 7.9
elif bank_name == 'Желтый банк':
    interest_rate = 9.6
elif bank_name == 'ой':
    interest_rate = 10.0

# Monthly loan rate
monthly_loan_rate = interest_rate/12/100

# General rate
general_rate = round(((1 + monthly_loan_rate) ** loan_term_month), 2)
print('Общая ставка: ', general_rate)

# Monthly payment
monthly_payment = (property_value - start_capital) * monthly_loan_rate * general_rate / (general_rate - 1)

# Overpayment
overpayment = monthly_payment * loan_term_month - (property_value - start_capital)

# Output
print()
print('Мой ежемесячный платеж: ', round(monthly_payment, 2))
print('Моя переплата составляет (руб.): ', round(overpayment, 2))

# Declare current date
current_date = date.today()

# Create list of dates
timestamp = pd.date_range(start=current_date, periods=loan_term_month, freq='M')

# Payment left for the 1st month
payment_left = (property_value - start_capital)

# Create lists
percentage_amount_list = [payment_left * monthly_loan_rate]
main_amount_list = [monthly_payment - (payment_left * monthly_loan_rate)]
payment_left_list = [payment_left]
monthly_payment_list = [monthly_payment]

# Mining data for table
for i in range(0, loan_term_month - 1):
    percentage_amount = payment_left * monthly_loan_rate
    main_amount = monthly_payment - percentage_amount
    payment_left -= main_amount
    percentage_amount_list.append(round(percentage_amount, 2))
    main_amount_list.append(round(main_amount, 2))
    payment_left_list.append(round(payment_left, 2))
    monthly_payment_list.append(round(monthly_payment, 2))

# Create plot
plt.scatter(timestamp, payment_left_list)
plt.show()

# Create table
table = pd.DataFrame({'Дата': timestamp, 'Остаток долга': payment_left_list, 'Платеж': monthly_payment_list,
                      'Процентная часть': percentage_amount_list, 'Основная часть': main_amount_list})
print(table)
