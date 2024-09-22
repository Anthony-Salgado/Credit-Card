# Credit-Card
# Credit Card System
# Authors: Anthony Salgado & Harry Nguyen
# Date Completed: October 16, 2022

This system models a credit card functionality where purchases can be made, interest is calculated on balances, and payments can be made. The system also tracks potential fraudulent activity based on the country where purchases are made.

## Features
- Tracks two types of balances:
  - `cur_balance_owing_intst`: Balance that accrues interest.
  - `cur_balance_owing_recent`: Balance from recent purchases that hasn't yet accrued interest.
- Interest is applied monthly on the outstanding balance.
- Fraud detection checks if purchases are made in three different countries consecutively.
- The system can be disabled when fraudulent activity is detected.
- Provides functionality to check the total amount owed at any given time.

## Global Variables
- `cur_balance_owing_intst`: The portion of the balance that accrues interest.
- `cur_balance_owing_recent`: The portion of the balance from recent purchases.
- `last_update_day` and `last_update_month`: The date of the last transaction or inquiry.
- `last_country` and `last_country2`: Tracks the last two countries for fraud prevention.
- `enabled`: A flag to indicate if the card is active or has been disabled due to fraud.
- `counter`: Tracks the number of consecutive purchases made.
- `interest`: The interest rate (set to 5%).

## Functions

### `initialize()`
- Resets the entire system to its initial state.
- Sets all balances to 0, re-enables the card, and resets the date and fraud tracking variables.

### `date_same_or_later(day1, month1, day2, month2)`
- Checks if the date `day1/month1` is the same as or later than `day2/month2`.
- Returns `True` if it is, and `False` otherwise.

### `all_three_different(c1, c2, c3)`
- Checks if three countries are all different.
- Used to detect potential fraud when purchases are made in three distinct countries in a row.
- Returns `False` if fraud is detected (i.e., purchases made in three different countries consecutively).

### `purchase(amount, day, month, country)`
- Records a purchase made on a specific day and in a specific country.
- Updates the `cur_balance_owing_recent` with the purchase amount.
- Applies interest if necessary and checks for fraud based on the country of the purchase.
- If fraud is detected, disables the system by setting `enabled = False` and returns `"error"`.

### `amount_owed(day, month)`
- Calculates the total amount owed, including balances that accrue interest.
- Applies any interest owed up until the given `day/month`.
- Returns the total balance, which is the sum of `cur_balance_owing_intst` and `cur_balance_owing_recent`.

### `apply_interest(month1, month2)`
- Applies interest to the `cur_balance_owing_intst` for the number of months between `month1` and `month2`.
- Moves the amount from `cur_balance_owing_recent` to `cur_balance_owing_intst` and applies interest to the total balance.

## Fraud Detection
- Fraud detection is based on purchases made in three different countries consecutively. If the system detects that a purchase is made in a third different country without returning to any of the previous two, it disables the card (`enabled = False`).

## Error Handling
- The system returns `"error"` if:
  - The card is disabled due to suspected fraud.
  - A transaction is attempted with a date earlier than the last recorded transaction.
