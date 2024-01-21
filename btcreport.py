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
import argparse
from string import Template
from collections import OrderedDict
from prettytable import PrettyTable


html_document = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>BTC Report</title>
    <style>
        table, th, td {
            border: 1px solid black;
            border-collapse: collapse;
        }
        th, td {
            padding: 8px;
        }
    </style>
</head>
<body>
    <h1>BTC Report</h1>
    $table
</body>
</html>
"""

report_fields = {
    "total_purchase": "Total purchase",
    "avg_btc_price": "Average BTC price",
    "asset_value": "Asset value",
    "asset_gain_d": "Asset gain($)",
    "asset_gain_p": "Asset gain(%)",
    "total_btc": "Total BTC",
    "btc_in_custody": "BTC in custody",
    "pending_withdraw": "Pending withdrawal",
    "total_transactions": "Total transactions"
}

btc_report_file = "btcreport"

def round_down(n, decimals=0):
    multiplier = 10**decimals
    return math.floor(n * multiplier) / multiplier

def generate_html(report_details):
    report_html_file = btc_report_file + ".html"
    template = Template(html_document)
    table = PrettyTable()
    table.header = False
    for field in report_details:
        table.add_row([field, report_details[field]])
    
    with open(report_html_file, "w", encoding="utf-8") as html_file:
        html_file.write(template.substitute(
            table = table.get_html_string()
        ))

    print("Generated report file: {}".format(report_html_file))
    

def generate_pdf():
    pass

def get_report_details(csv_reader, btc_market_price):
    report_details = OrderedDict({
        report_fields["total_purchase"]: 0,
        report_fields["avg_btc_price"]: 0,
        report_fields["asset_value"]: 0,
        report_fields["asset_gain_d"]: 0,
        report_fields["asset_gain_p"]: 0,
        report_fields["total_btc"]: 0,
        report_fields["btc_in_custody"]: 0,
        report_fields["pending_withdraw"]: 0,
        report_fields["total_transactions"]: 0
    })

    btc_price = 0
    for record in csv_reader:
        if record["Transaction Type"] == "Bitcoin Buy":
            report_details[report_fields["total_purchase"]] += abs(float(record["Net Amount"].replace("$", "")))
            report_details[report_fields["total_btc"]] += float(record["Asset Amount"])
            btc_price += float(record["Asset Price"].replace("$", "").replace(",", ""))
            report_details[report_fields["total_transactions"]] += 1
        if record["Transaction Type"] == "Bitcoin Withdrawal":
            report_details[report_fields["btc_in_custody"]] += float(record["Asset Amount"])
    
    report_details[report_fields["avg_btc_price"]] = btc_price / report_details[report_fields["total_transactions"]]
    report_details[report_fields["total_btc"]] = round_down(report_details[report_fields["total_btc"]], 7)
    report_details[report_fields["btc_in_custody"]] = round_down(report_details[report_fields["btc_in_custody"]], 7)
    
    report_details[report_fields["asset_value"]] = round_down(float(btc_market_price) * report_details[report_fields["total_btc"]], 2)
    
    report_details[report_fields["asset_gain_d"]] = "${}".format(
                    round_down(report_details[report_fields["asset_value"]] - report_details[report_fields["total_purchase"]], 2))
    
    report_details[report_fields["asset_gain_p"]] = "{}%".format(
                    round_down(((report_details[report_fields["asset_value"]] - report_details[report_fields["total_purchase"]]) /
                                    report_details[report_fields["total_purchase"]]) * 100, 2))
    
    report_details[report_fields["total_purchase"]] = "${}".format(report_details[report_fields["total_purchase"]])
    report_details[report_fields["avg_btc_price"]] = "${}".format(round_down(report_details[report_fields["avg_btc_price"]], 2))

    return report_details
    

def generate_report(cash_app_csv, btc_market_price):
    with open(cash_app_csv, "r", encoding="utf-8", newline="") as csv_file:
        data = csv.DictReader(csv_file)
        return get_report_details(data, btc_market_price)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_file", help="Cash App CSV export")
    parser.add_argument("btc_price", help="BTC market price")
    parser.add_argument("--report_format", default="html", help="Output report format")
    args = parser.parse_args()

    report = generate_report(args.csv_file, args.btc_price)
    if args.report_format == "html":
        generate_html(report)
