from mortgage_calculator import MortgageCalculator

# For test
property_value = int(input('Введите стоимость недвижимости (руб.): '))
loan_term_year = int(input('Введите срок ипотеки (лет): '))
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
elif bank_name == '1':
    interest_rate = 12.0
elif bank_name == 'ой':
    interest_rate = 10.0
else:
    print('Ошибка, товарищ.')
    interest_rate = 0

#TODO: Input from user
mortgage_output = MortgageCalculator(interest_rate, loan_term_year, property_value, start_capital)

#TODO: Messages to user
print('Аннуитетный платеж: ')
print(mortgage_output.number_payments())
print(mortgage_output.monthly_percentage())
print('Мой ежемесячный платеж:  {:.2f} руб.'.format(mortgage_output.annuity_calc()[0]))
print('Моя переплата составляет {:.1f} руб.'.format(mortgage_output.annuity_calc()[1]))

# diff
print()
print('Дифференцированный платеж: ')
print(mortgage_output.number_payments())
print(mortgage_output.monthly_percentage())

# I dont know how to realize double return better :,)
diff_table, diff_payment_list = mortgage_output.create_diff_data()
ann_table, ann_payment_list = mortgage_output.create_annuity_data()

# Functions return name of files/plot, so you can send it to user
#TODO: plot and tables to user
mortgage_output.create_table(ann_table, diff_table)
mortgage_output.create_plot(ann_payment_list, diff_payment_list)
