#!/usr/bin/python3

# This is free and unencumbered software released into the public domain.

# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.

# In jurisdictions that recognize copyright laws, the author or authors
# of this software dedicate any and all copyright interest in the
# software to the public domain. We make this dedication for the benefit
# of the public at large and to the detriment of our heirs and
# successors. We intend this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this
# software under copyright law.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

# For more information, please refer to <https://unlicense.org>

import csv
import math
import sys

report_name = "cash_app_report.csv"
round_decimals = 7
text_allign = 20

def round_down(n, decimals=0):
    multiplier = 10**decimals
    return math.floor(n * multiplier) / multiplier

with open(report_name) as csv_file:
    total_purchase = 0
    total_btc = 0
    btc_in_custody = 0
    total_transactions = 0
    btc_price = 0
    avg_btc_price = 0
    data = csv.DictReader(csv_file)
    for record in data:
        if record["Transaction Type"] == "Bitcoin Buy":
            total_purchase += abs(float(record["Net Amount"].replace("$", "")))
            total_btc += float(record["Asset Amount"])
            btc_price += float(record["Asset Price"].replace("$", "").replace(",", ""))
            total_transactions += 1
        if record["Transaction Type"] == "Bitcoin Withdrawal":
            btc_in_custody += float(record["Asset Amount"])
    
    avg_btc_price = btc_price / total_transactions
    if len(sys.argv) == 2:
        asset_value = round_down(float(sys.argv[1]) * total_btc, 2)
        asset_gain = "${}".format(
                           round_down(asset_value - total_purchase, 2))
        asset_gain_percentage = "{}%".format(
                                      round_down(
                                      ((asset_value - total_purchase) / total_purchase) * 100, 2
                                      ))
    
    total_purchase = "${}".format(total_purchase)
    avg_btc_price = "${}".format(round_down(avg_btc_price, 2))

print()
print("BTC Report".center(40, " "))
print("Total purchase: ".rjust(text_allign), total_purchase)
print("Average BTC price: ".rjust(text_allign), avg_btc_price)
if len(sys.argv) == 2:
    print("Asset value: ".rjust(text_allign), asset_value)
    print("Asset gain($): ".rjust(text_allign), asset_gain)
    print("Asset gain(%): ".rjust(text_allign), asset_gain_percentage)
print("Total BTC: ".rjust(text_allign), round_down(total_btc, round_decimals))
print("BTC in custody: ".rjust(text_allign), round_down(btc_in_custody, round_decimals))
print("Pending withdrawal: ".rjust(text_allign), 
                            round(total_btc - btc_in_custody, round_decimals))
print()
