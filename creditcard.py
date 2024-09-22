

# You should modify initialize()
def initialize():
    global cur_balance_owing_intst          #interest amount
    global cur_balance_owing_recent
    global last_update_day, last_update_month
    global last_update_month1               #variable used to check if interest
                                            #has already been applied
    global last_country, last_country2
    global enabled                          #toggle
    global counter                          #number of purchases

    #set the values to 0
    cur_balance_owing_intst = 0
    cur_balance_owing_recent = 0

    last_update_day, last_update_month, last_update_month1 = 0, 0, 0

    last_country = None
    last_country2 = None

    #enable the system after initilization
    enabled = True

    global interest

    #set the value of interest
    interest = 1.05

    counter = 0

def date_same_or_later(day1, month1, day2, month2):
    #if it is next month then date doesn't matter
    if month1 > month2:
        return True
    #if it is the same month then compare the dates
    elif month1 == month2:
        return day1 >= day2
    #otherwise return False
    else:
        return False


def all_three_different(c1, c2, c3):
    global counter
    if counter >= 3:
        #3 different countries in 3 purchases
        if c1 != c2 and c2 != c3 and c1 != c3:
            return False
        else:
            return True
    else:
        return True



def purchase(amount, day, month, country):
    global cur_balance_owing_intst, cur_balance_owing_recent
    global last_update_day, last_update_month
    global last_country, last_country2
    global enabled
    global counter

    #check if the purchased is enabled
    if enabled:
        if date_same_or_later (day, month, last_update_day, last_update_month):
            counter += 1
            #proceeds if all three countries are NOT different
            if all_three_different(country, last_country, last_country2):
                apply_interest(month, last_update_month)
                cur_balance_owing_recent += amount
                last_update_day = day
                last_update_month = month

                #update the last two countries
                last_country2 = last_country
                last_country = country

            #Otherwise disables the system
            else:
                enabled = False
                return "error"

        else:
            return "error"
    else:
        return "error"







def amount_owed(day, month):
    global last_update_day, last_update_month
    global cur_balance_owing_intst
    global cur_balance_owing_recent
    global interest

    if date_same_or_later(day, month, last_update_day, last_update_month):
        apply_interest(month, last_update_month)
        last_update_day = day
        last_update_month = month
        return cur_balance_owing_intst + cur_balance_owing_recent
    else:
        return "error"


def apply_interest(month1, month2):
    global cur_balance_owing_intst, cur_balance_owing_recent
    global interest
    global last_update_month1

    #ensures that no interest applied more than once within one month
    if last_update_month1 == month1:
        return cur_balance_owing_intst, cur_balance_owing_recent
    else:
        month_to_interest = month1 - month2

        #apply the interest
        cur_balance_owing_intst *= interest**month_to_interest
        cur_balance_owing_intst += cur_balance_owing_recent * interest ** (month_to_interest - 1)
        cur_balance_owing_recent = 0


    last_update_month1 = month1






def pay_bill(amount, day, month):
    global cur_balance_owing_intst, cur_balance_owing_recent
    global last_update_day, last_update_month

    if date_same_or_later(day, month, last_update_day, last_update_month):
        #check if there is interest amount owed
        if cur_balance_owing_intst > 0:
            left_over = amount - cur_balance_owing_intst

            #check if the interest is fully paid and there's still left over
            if left_over > 0:
                cur_balance_owing_intst = 0
                cur_balance_owing_recent = max (0, cur_balance_owing_recent - left_over)

            #otherwise return the interest the absolute amount of left over
            else:
                cur_balance_owing_intst = abs(left_over)
        #otherwise pay the recent amount owed, if fully paid return 0
        else:
            cur_balance_owing_recent = max (0, cur_balance_owing_recent - amount)
    else:
        return "error"







# Initialize all global variables outside the main block.
initialize()

if __name__ == '__main__':
    # Describe your testing strategy and implement it below.
    # What you see here is just the simulation from the handout, which
    # doesn't work yet.
    ##
    initialize()
    purchase(80, 8, 1, "Canada")
    print("Now owing:", amount_owed(8, 1))      # 80.0
    pay_bill(50, 2, 2)
    print("Now owing:", amount_owed(2, 2))      # 30.0     (=80-50)
    print("Now owing:", amount_owed(6, 3))      # 31.5     (=30*1.05)
    purchase(40, 6, 3, "Canada")
    print("Now owing:", amount_owed(6, 3))      # 71.5     (=31.5+40)
    pay_bill(30, 7, 3)
    print("Now owing:", amount_owed(7, 3))      # 41.5     (=71.5-30)
    print("Now owing:", amount_owed(1, 5))      # 43.65375 (=1.5*1.05*1.05+40*1.05)
    purchase(40, 2, 5, "France")
    print("Now owing:", amount_owed(2, 5))      # 83.65375
    print(purchase(50, 3, 5, "United States"))  # error    (3 diff. countries in
                                                #          a row)

    print("Now owing:", amount_owed(3, 5))      # 83.65375 (no change, purchase
                                                #           declined)
    print(purchase(150, 3, 5, "Canada"))        # error    (card disabled)
    print("Now owing:", amount_owed(1, 6))      # 85.8364375
                                                # (43.65375*1.05+40)
                                            ##

        # regular purchase (1 /month), pays back at beginning of next month
    print("TEST CASE 1")
    initialize()  # reset the code
    purchase(80, 1, 1, "Canada")
    print("Now owing:", amount_owed(31, 1))  # 80.0
    pay_bill(80, 1, 2)
    purchase(80, 1, 2, "Canada")
    print("Now owing:", amount_owed(29, 2))  # 80.0
    pay_bill(80, 1, 3)
    purchase(80, 1, 3, "Canada")
    print("Now owing:", amount_owed(31, 3))  # 80.0

    # regular purchase (1 /month), pays half at beginning of next month
    print("TEST CASE 2")
    initialize()  # reset the code
    purchase(80, 1, 1, "Canada")
    print("Now owing:", amount_owed(31, 1))  # 80.0
    pay_bill(40, 1, 2)  # 40
    purchase(80, 1, 2, "Canada")  # 120 (40 + 80)
    print("Now owing:", amount_owed(29, 2))  # 120.0 (40 interest, 80 non-interest)
    print("Now owing:", amount_owed(1, 3))  # 122.0 (40*1.05+80 interest, 0 non-interest)
    pay_bill(40, 1, 3)  # 82.0 (82 interest, 0 non-interest)
    purchase(80, 1, 3, "Canada")  # 162.0 (82 interest, 80 non-interest)
    print("Now owing:", amount_owed(31, 3))  # 162.0 (82 interest, 80 non-interest)
    print("Now owing:", amount_owed(1, 4))  # 166.1 (86.1+80 interest, 0 non-interest)

    # regular purchase (2 /month), pays back at beginning of next month
    print("TEST CASE 3")
    initialize()  # reset the code
    purchase(80, 1, 1, "Canada")
    purchase(80, 2, 1, "Canada")
    print("Now owing:", amount_owed(31, 1))  # 80.0
    pay_bill(160, 1, 2)
    purchase(80, 1, 2, "Canada")
    purchase(80, 2, 2, "Canada")
    print("Now owing:", amount_owed(29, 2))  # 80.0
    pay_bill(160, 1, 3)
    purchase(80, 1, 3, "Canada")
    purchase(80, 2, 3, "Canada")
    print("Now owing:", amount_owed(31, 3))  # 80.0

    # regular purchase (2 /month), pays half at beginning of next month
    print("TEST CASE 4")
    initialize()  # reset the code
    purchase(80, 1, 1, "Canada")
    purchase(80, 2, 1, "Canada")
    print("Now owing:", amount_owed(31, 1))  # 160.0
    pay_bill(80, 1, 2)  # 80
    purchase(80, 1, 2, "Canada")  # 160 (80 + 80)
    purchase(80, 2, 2, "Canada")
    print("Now owing:", amount_owed(29, 2))  # 240.0 (80 interest, 160 non-interest)
    print("Now owing:", amount_owed(1, 3))  # 244.0 (244 interest, 0 non-interest)
    pay_bill(80, 1, 3)  # 164.0 (164 interest, 0 non-interest)
    purchase(80, 1, 3, "Canada")  # 244.0 (164 interest, 80 non-interest)
    purchase(80, 2, 3, "Canada")
    print("Now owing:", amount_owed(31, 3))  # 324.0 (164 interest, 160 non-interest)
    print("Now owing:", amount_owed(1, 4))  # 332.2 (332.2 interest, 0 non-interest)

    # buy once, pay in june in full, check in december
    print("TEST CASE 5")
    initialize()  # reset the code
    purchase(80, 1, 1, "Canada")
    print("Now owing:", amount_owed(15, 6))  # 80->80->84->88.2->92.61->97.2405(in june)
    pay_bill(97.24050000000001, 15, 6)
    print("Now owing:", amount_owed(15, 6))
    print("Now owing:", amount_owed(31, 12))

    # buy once, pay in june in partial, check in december
    print("TEST CASE 6")
    initialize()  # reset the code
    purchase(80, 1, 1, "Canada")
    print("Now owing:", amount_owed(15, 6))  # 80->80->84->88.2->92.61->97.2405(in june)
    pay_bill(10, 15, 6)  # 87.2405 remaining
    print("Now owing:", amount_owed(15, 6))  # 87.2405->91.602525(july)->96.18265125->100.9917838125->106.0413730031->
    print("Now owing:", amount_owed(31, 12))  # 111.3434416533 in november -> 116.9106137359 in december

    # buy once, buy again in early june, pay in june in full for jan debt+interest, check in december
    print("TEST CASE 7")
    initialize()  # reset the code
    purchase(80, 1, 1, "Canada")
    purchase(80, 1, 6, "Canada")
    print("Now owing:", amount_owed(15, 6))  # (80->80->84->88.2->92.61->97.2405(in june)) + 80 new debt => 177.2405
    pay_bill(97.2405, 15, 6)  # 80 new debt remaining
    print("Now owing:", amount_owed(15, 6))  # 80
    print("Now owing:", amount_owed(31, 12))  # 80->80->84->88.2->92.61->97.2405->102.102525

    # buy once, buy again in early june, pay in june (slightly more than jan debt+interest), check in december
    print("TEST CASE 8")
    initialize()  # reset the code
    purchase(80, 1, 1, "Canada")
    purchase(80, 1, 6, "Canada")
    print("Now owing:", amount_owed(15, 6))  # (80->80->84->88.2->92.61->97.2405(in june)) + 80 new debt => 177.2405
    pay_bill(100, 15, 6)  # 77.2405 (all new debt) remaining
    print("Now owing:", amount_owed(15, 6))
    print("Now owing:", amount_owed(31, 12))  # 77.2405->77.2405->81.102525->85.15765125
    # ->89.4155338125->93.8863105031->98.5806260283 (at dec)

    # buy once, buy again in early june, pay in june (slightly less than jan debt+interest), check in december
    print("TEST CASE 9")
    initialize()  # reset the code
    purchase(80, 1, 1, "Canada")
    purchase(80, 1, 6, "Canada")
    print("Now owing:", amount_owed(15, 6))  # (80->80->84->88.2->92.61->97.2405(in june)) + 80 new debt => 177.2405
    pay_bill(90, 15, 6)  # 87.2405 remaining (7.2405 old debt)
    print("Now owing:", amount_owed(15, 6))
    print("Now owing:", amount_owed(31, 12))  # 80+7.2405(june)->80+7.602525 (87.602525)->91.98265125->96.5817838125
    # ->101.4108730031->106.4814166533->111.805487486

    # buy once, forget about the card
    print("TEST CASE 10")
    initialize()  # reset the code
    purchase(80, 1, 1, "Canada")
    print("Now owing:", amount_owed(31, 12))  # 80->80(feb)->(80*1.05^10)(dec)130.3115701422

    # buy once, pay back immediately forget about the card
    print("TEST CASE 11")
    initialize()  # reset the code
    purchase(80, 1, 1, "Canada")
    pay_bill(80, 1, 1)
    print("Now owing:", amount_owed(31, 12))  # 0

    # TEST 4 but with alternating 2 countries
    print("TEST CASE 12")
    initialize()  # reset the code
    purchase(80, 1, 1, "Canada")
    purchase(80, 2, 1, "France")
    print("Now owing:", amount_owed(31, 1))  # 160.0
    pay_bill(80, 1, 2)  # 80
    purchase(80, 1, 2, "Canada")  # 160 (80 + 80)
    purchase(80, 2, 2, "France")
    print("Now owing:", amount_owed(29, 2))  # 240.0 (80 interest, 160 non-interest)
    print("Now owing:", amount_owed(1, 3))  # 244.0 (244 interest, 0 non-interest)
    pay_bill(80, 1, 3)  # 164.0 (164 interest, 0 non-interest)
    purchase(80, 1, 3, "Canada")  # 244.0 (164 interest, 80 non-interest)
    purchase(80, 2, 3, "France")
    print("Now owing:", amount_owed(31, 3))  # 324.0 (164 interest, 160 non-interest)
    print("Now owing:", amount_owed(1, 4))  # 332.2 (332.2 interest, 0 non-interest)

    # TEST 4 but with alternating 3 countries
    print("TEST CASE 13")
    initialize()  # reset the code
    purchase(80, 1, 1, "Canada")
    purchase(80, 2, 1, "France")
    print("Now owing:", amount_owed(31, 1))  # 160.0
    pay_bill(80, 1, 2)  # 80 interest building debt
    purchase(80, 1, 2, "China")  # FRAUD - ERROR, still 80
    purchase(80, 2, 2, "France")  # ALREADY FRAUD - ERROR, still 80
    print("Now owing:", amount_owed(29, 2))  # 80 (80 interest, 0 non-interest)
    print("Now owing:", amount_owed(1, 3))  # 84.0 (84 interest, 0 non-interest)
    pay_bill(80, 1, 3)  # 4.0 (4 interest, 0 non-interest)
    purchase(80, 1, 3, "Canada")  # ALREADY FRAUD - ERROR, still 4
    purchase(80, 2, 3, "France")  # ALREADY FRAUD - ERROR, still 4
    print("Now owing:", amount_owed(31, 3))  # 4.0 (4 interest, 160 non-interest)
    print("Now owing:", amount_owed(1, 4))  # 4.2 (4.2 interest, 0 non-interest)

    # TEST 4 but with same country -> then 2 other countries
    print("TEST CASE 14")
    initialize()  # reset the code
    purchase(80, 1, 1, "Canada")
    purchase(80, 2, 1, "Canada")
    print("Now owing:", amount_owed(31, 1))  # 160.0
    pay_bill(80, 1, 2)  # 80
    purchase(80, 1, 2, "Canada")  # 160 (80 + 80)
    purchase(80, 2, 2, "Canada")
    print("Now owing:", amount_owed(29, 2))  # 240.0 (80 interest, 160 non-interest)
    print("Now owing:", amount_owed(1, 3))  # 244.0 (244 interest, 0 non-interest)
    pay_bill(80, 1, 3)  # 164.0 (164 interest, 0 non-interest)
    purchase(80, 1, 3, "China")  # 244.0 (164 interest, 80 non-interest)
    purchase(80, 2, 3, "France")  # FRAUD, STILL 244 (164 interest, 80 non-interest)
    print("Now owing:", amount_owed(31, 3))  # 244 (164 interest, 80 non-interest)
    print("Now owing:", amount_owed(1, 4))  # 252.2 (164*1.05+80 interest, 0 non-interest)

    # TEST 4 but with 3 countries, but each country purchase twice
    print("TEST CASE 15")
    initialize()  # reset the code
    purchase(80, 1, 1, "Canada")
    purchase(80, 2, 1, "Canada")
    print("Now owing:", amount_owed(31, 1))  # 160.0
    pay_bill(80, 1, 2)  # 80
    purchase(80, 1, 2, "France")  # 160 (80 + 80)
    purchase(80, 2, 2, "France")
    print("Now owing:", amount_owed(29, 2))  # 240.0 (80 interest, 160 non-interest)
    print("Now owing:", amount_owed(1, 3))  # 244.0 (244 interest, 0 non-interest)
    pay_bill(80, 1, 3)  # 164.0 (164 interest, 0 non-interest)
    purchase(80, 1, 3, "China")  # 244.0 (164 interest, 80 non-interest)
    purchase(80, 2, 3, "China")
    print("Now owing:", amount_owed(31, 3))  # 324.0 (164 interest, 160 non-interest)
    print("Now owing:", amount_owed(1, 4))  # 332.2 (332.2 interest, 0 non-interest)

    # Fraud early on, but don't pay back
    print("TEST CASE 16")
    initialize()  # reset the code
    purchase(80, 1, 1, "Canada")
    purchase(50, 2, 1, "France")
    purchase(30, 2, 1, "Germany")
    purchase(30, 3, 1, "Germany")
    print("Now owing:", amount_owed(31, 1))  # 130.0
    print("Now owing:", amount_owed(31, 2))  # 130.0
    print("Now owing:", amount_owed(31, 3))  # 130*1.05
    print("Now owing:", amount_owed(31, 12))  # 130*1.05**10=211.7563014811

    # Fraud early on, but pay back
    print("TEST CASE 17")
    initialize()  # reset the code
    purchase(80, 1, 1, "Canada")
    purchase(50, 2, 1, "France")
    purchase(30, 2, 1, "Germany")
    purchase(30, 3, 1, "Germany")
    pay_bill(130, 3, 1)
    print("Now owing:", amount_owed(31, 1))  # 0
    print("Now owing:", amount_owed(31, 2))  # 0
    print("Now owing:", amount_owed(31, 3))  # 0
    print("Now owing:", amount_owed(31, 12))  # 0

    # Fraud early on, but pay back
    print("TEST CASE 18")
    initialize()  # reset the code
    purchase(80, 1, 1, "Canada")
    purchase(50, 2, 2, "France")
    pay_bill(90, 3, 2)  # now owe 40 non interest
    purchase(30, 3, 3, "Germany")
    purchase(30, 4, 4, "Germany")
    print("Now owing:", amount_owed(31, 3))  # 40 interested money
    print("Now owing:", amount_owed(31, 12))  # 40*1.05**9
