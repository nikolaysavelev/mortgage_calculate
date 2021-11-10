# Matplotlib section, plt for plot, PdfPages for create .pdf
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
# Pandas section, pd for table, dfi for dataframe -> image
import pandas as pd
import dataframe_image as dfi
from datetime import date


class MortgageCalculator:

    def __init__(self, interest_rate, loan_term_year, property_value, start_capital):
        """ Initializing parameters

        :param interest_rate: float (0.01 %)
        :param loan_term_year:  number of years, int
        :param property_value: int
        :param start_capital: int
        """
        self.interest_rate = interest_rate
        self.loan_term = loan_term_year
        # Credit calculation
        self.credit = property_value - start_capital
        # Monthly rate
        self.monthly_loan_rate = self.interest_rate / (12*100)
        # Number of months
        self.loan_term_month = self.loan_term * 12
        self.general_rate = ((1 + self.monthly_loan_rate) ** self.loan_term_month)

    def monthly_percentage(self):
        """
        Method of output general rate
        :return:
        """
        return 'Общая ставка = {:.2f} %'.format(self.general_rate)

    def number_payments(self):
        """
        Method of output number of payments
        :return:
        """
        return 'Количество месяцев оплаты: ' + str(self.loan_term_month)

    def annuity_calc(self):
        """
        Method calculate annuity payment
        :return: monthly payment, overpayment, monthly payment list
        """
        # Create list with monthly payment to each month
        monthly_payment_ann = []

        # Formula to calculate MP
        monthly_payment = ((self.credit * self.monthly_loan_rate * self.general_rate) /
                           (self.general_rate - 1))

        # Formula to calculate OP
        overpayment = monthly_payment * self.loan_term_month - self.credit

        # Append MP to MP list with each month
        while self.loan_term_month != 0:
            monthly_payment_ann.append(round(monthly_payment, 2))
            self.loan_term_month -= 1

        # Reset number of months
        self.loan_term_month = self.loan_term * 12
        return [round(monthly_payment, 2), round(overpayment, 2), monthly_payment_ann]

    # Declare variables from return
    #monthly_payment_ann, overpayment_ann, monthly_payment_ann_list = annuity_calc()

    def diff_calc(self):
        """
        Method calculate differential payment
        :return: monthly payment list
        """
        # Create list with monthly payment to each month
        monthly_payment_diff = []

        # Declare variable for payment left
        rest = self.credit

        # Declare variable for differential monthly_payment
        monthly_payment_real = self.credit / self.loan_term_month

        # Append MP to MP list with each month
        while self.loan_term_month != 0:
            # Calculate MP by formula
            monthly_payment = monthly_payment_real + (rest * self.monthly_loan_rate)
            monthly_payment_diff.append(round(monthly_payment, 2))
            rest -= monthly_payment_real
            self.loan_term_month -= 1

        # Reset number of months
        self.loan_term_month = self.loan_term * 12
        return monthly_payment_diff

    def create_timestamp(self):
        """
        Method create timestamp for plot and tables
        :return:
        """
        # Declare current date
        current_date = date.today()
        # Create list of dates
        timestamp = pd.date_range(start=current_date, periods=self.loan_term_month, freq='M')
        return timestamp

    def create_annuity_data(self):
        """
        Method to mine annuity payment data
        :return: data_table - ann dataframe, payment_left_list - list with payment_left
        """
        # Payment left for the 1st month
        payment_left = self.credit

        # Percentage amount for the 1st month
        percentage_amount_start = payment_left * self.monthly_loan_rate

        # Main amount for the 1st month
        main_amount = self.annuity_calc()[0] - percentage_amount_start

        # Payment left for the end of period
        payment_left_end = payment_left - main_amount

        # Create lists
        percentage_amount_list = []
        main_amount_list = []
        payment_left_list = [payment_left]
        payment_left_end_list = [payment_left_end]

        # Mining data for table
        for i in range(0, self.loan_term_month):
            # Formulas to ann payment
            percentage_amount = payment_left * self.monthly_loan_rate
            main_amount = self.annuity_calc()[0] - percentage_amount
            payment_left -= main_amount
            payment_left_end = payment_left - main_amount
            percentage_amount_list.append(round(percentage_amount, 2))
            main_amount_list.append(round(main_amount, 2))
            payment_left_list.append(round(payment_left, 2))
            payment_left_end_list.append(round(payment_left_end, 2))

        # Crutch for correct table
        payment_left_list = payment_left_list[:-1]
        payment_left_end_list = payment_left_end_list[:-1]

        # Create table
        data_table = pd.DataFrame({'Дата': self.create_timestamp(),
                                   'Остаток долга': payment_left_list,
                                   'Платеж': self.annuity_calc()[2],
                                   'Процентная часть': percentage_amount_list,
                                   'Основная часть': main_amount_list,
                                   'Остаток долга на конец периода': payment_left_end_list})

        return data_table, payment_left_list

    def create_diff_data(self):
        """
        Function to mine diff payment data
        :return: data_table - diff dataframe, payment_left_list - list with payment_left
        """
        # Payment left for the 1st month
        payment_left = self.credit

        # Percentage amount
        percentage_amount_start = payment_left * self.monthly_loan_rate

        # Main amount for the 1st month
        main_amount = self.diff_calc()[0] - percentage_amount_start

        # Payment left for the end of the period
        payment_left_end = payment_left - main_amount

        # Create lists
        percentage_amount_list = []
        main_amount_list = []
        payment_left_list = [payment_left]
        payment_left_end_list = [payment_left_end]

        # Mining data for table
        for i in range(0, self.loan_term_month):
            # Formulas for diff payment
            percentage_amount = payment_left * self.monthly_loan_rate
            main_amount = self.diff_calc()[0] - percentage_amount_start
            payment_left -= main_amount
            payment_left_end = payment_left - main_amount
            percentage_amount_list.append(round(percentage_amount, 2))
            main_amount_list.append(round(main_amount, 2))
            payment_left_list.append(round(payment_left, 2))
            payment_left_end_list.append(round(payment_left_end, 2))

        # Crutch for correct table
        payment_left_list = payment_left_list[:-1]
        payment_left_end_list = payment_left_end_list[:-1]

        # Create table
        data_table = pd.DataFrame({'Дата': self.create_timestamp(),
                                   'Остаток долга': payment_left_list,
                                   'Платеж': self.diff_calc(),
                                   'Процентная часть': percentage_amount_list,
                                   'Основная часть': main_amount_list,
                                   'Остаток долга на конец периода': payment_left_end_list})

        return data_table, payment_left_list

    def create_plot(self, payment_list_ann, payment_list_diff):
        """
        Function to create plot with annuity and differential payments
        :param payment_list_ann: list with all annuity payments
        :param payment_list_diff: list with all diff payments
        :return: name of plot
        """
        # Create figure
        plt.figure()
        # Create plot with 2 lines, timestamp - ox, payment_lists - oy
        plt.plot(self.create_timestamp(), payment_list_ann)
        plt.plot(self.create_timestamp(), payment_list_diff)
        # Set plot title
        plt.title('График выплат ипотеки')
        # Set plot legend
        plt.legend(labels=['Аннуитетные платежи', 'Дифференцированные платежи'])
        # Set axis labels
        plt.xlabel('Временной промежуток')
        plt.ylabel('Выплаты, руб.')
        # Create plot name
        plot_name = 'new_plot.png'
        # Save plot to directory
        plt.savefig(plot_name)
        return plot_name

    def create_table(self, data_table_ann, data_table_diff):
        """
        Function to create table with condition: if years < 8 then .png else .pdf
        :param data_table_ann: ann dataframe from return create_ann_data
        :param data_table_diff: diff dataframe from return create_diff data
        :return: names of files, if years < 8 then name of .png(s) else name of ann and diff .pdf
        """
        # Number of years < 8
        if data_table_ann.shape[0] <= 100:
            data_table_annuity = dfi.export(data_table_ann, 'table_ann.png')
            data_table_different = dfi.export(data_table_diff, 'table_diff.png')
            return data_table_annuity, data_table_different

        # Create pdf if df.rows > 100
        else:
            # create pdf for ann
            fig_table_ann, ax_table_ann = plt.subplots(figsize=(12, 4))
            ax_table_ann.axis('tight')
            ax_table_ann.axis('off')
            the_table_ann = ax_table_ann.table(cellText=data_table_ann.values, colLabels=data_table_ann.columns,
                                               loc='center')
            name_ann_pdf = 'ann_table.pdf'
            pp = PdfPages(name_ann_pdf)
            pp.savefig(fig_table_ann, bbox_inches='tight')
            pp.close()

            # create pdf for diff
            fig_table_diff, ax_table_diff = plt.subplots(figsize=(12, 4))
            ax_table_diff.axis('tight')
            ax_table_diff.axis('off')
            the_table_diff = ax_table_diff.table(cellText=data_table_diff.values, colLabels=data_table_diff.columns,
                                                 loc='center')
            name_diff_pdf = 'diff_table.pdf'
            pp = PdfPages(name_diff_pdf)
            pp.savefig(fig_table_diff, bbox_inches='tight')
            pp.close()
            return name_ann_pdf, name_diff_pdf
