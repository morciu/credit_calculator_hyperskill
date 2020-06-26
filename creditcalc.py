import sys
import math

args = sys.argv

# Set the first argument to the payment type
payment_type = args[1].split(sep='=')


def param_error():
    print("Incorrect parameters")

if len(args) < 5:
    param_error()

elif payment_type[1] == 'annuity':
    # Split arguments in a binary list cotaining description and value
    arg_2 = args[2].split(sep='=')
    arg_3 = args[3].split(sep='=')
    arg_4 = args[4].split(sep='=')
    # Set conditions for calculating "period"
    period_count = ['--principal', '--payment', '--interest']
    req_period = False
    if (arg_2[0] in period_count) and (arg_3[0] in period_count) and (arg_4[0] in period_count):
        req_period = True
    # Set conditions for calculating "monthly pay"
    ann_monthly_pay = ['--principal', '--periods', '--interest']
    req_annuity = False
    if (arg_2[0] in ann_monthly_pay) and (arg_3[0] in ann_monthly_pay) and (arg_4[0] in ann_monthly_pay):
        req_annuity = True
    # Set conditions for calculating "credit principal"
    cred_princ_lst = ['--payment', '--periods', '--interest']
    req_credit_principal = False
    if (arg_2[0] in cred_princ_lst) and (arg_3[0] in cred_princ_lst) and (arg_4[0] in cred_princ_lst):
        req_credit_principal = True

    if req_period:
        credit_principal = int(arg_2[1])
        monthly_pay = int(arg_3[1])
        credit_interest = float(arg_4[1])

        nom_interest = (credit_interest / 100) / (12 * (100 / 100))
        month_count = math.ceil(
            math.log(monthly_pay / (monthly_pay - nom_interest * credit_principal), (1 + nom_interest)))
        overpayment = monthly_pay * month_count - credit_principal

        years = month_count // 12
        months = month_count % 12

        if years == 0:
            print(f"You need {months} months to repay this credit!")
        elif months == 0:
            print(f"You need {years} years to repay this credit!")
        else:
            print(f"You need {years} years and {months} months to repay this credit!")
        print(f'Overpayment = {overpayment}')

    elif req_annuity:
        credit_principal = int(arg_2[1])
        month_count = int(arg_3[1])
        credit_interest = float(arg_4[1])
        nom_interest = (credit_interest / 100) / (12 * (100 / 100))
        annuity = credit_principal * (
                (nom_interest * (1 + nom_interest) ** month_count) / ((1 + nom_interest) ** month_count - 1))
        print(f'Your annuity payment = {math.ceil(annuity)}!')
        overpayment = (math.ceil(annuity) * month_count) - credit_principal
        print(f'Overpayment = {overpayment}')

    elif req_credit_principal:
        annuity = float(arg_2[1])
        month_count = int(arg_3[1])
        credit_interest = float(arg_4[1])

        nom_interest = (credit_interest / 100) / (12 * (100 / 100))
        credit_principal = annuity / (
                (nom_interest * ((1 + nom_interest) ** month_count)) / ((1 + nom_interest) ** month_count - 1)
        )
        overpayment = annuity * month_count - math.floor(credit_principal)
        print(f'Your credit principal = {math.floor(credit_principal)}')
        print(f'Overpayment = {int(overpayment)}')

elif payment_type[1] == 'diff':
    # Split arguments in a binary list cotaining description and value
    arg_2 = args[2].split(sep='=')
    arg_3 = args[3].split(sep='=')
    arg_4 = args[4].split(sep='=')

    # Set conditions for calculating differentiated payments
    diff_payments = ['--principal', '--periods', '--interest']
    req_diff_pay = False
    if (arg_2[0] in diff_payments) and (arg_3[0] in diff_payments) and (arg_4[0] in diff_payments):
        req_diff_pay = True

    if req_diff_pay:
        credit_principal = int(arg_2[1])
        month_count = int(arg_3[1])
        credit_interest = float(arg_4[1])
        nom_interest = (credit_interest / 100) / (12 * (100 / 100))
        total_pay = 0
        for m in range(1, month_count+1):
            diff = (credit_principal / month_count) + nom_interest * (credit_principal - ((credit_principal * (m - 1)) / month_count))
            print(f"Month {m}: paid out {math.ceil(diff)}")
            total_pay += math.ceil(diff)
        overpayment = total_pay - credit_principal
        print(f"Overpayment = {overpayment}")

    # Display error message if one of the arguments is 'payment' (can't be used in this situation)
    if arg_2[0] == '--payment' or arg_3[0] == '--payment' or arg_4[0] == '--payment':
        param_error()


else:
    param_error()
