import csv
html_opening_tags = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>SR Oversight</title>
</head>
<body>
<p> Days Open,Name,SR Link</p>
"""

html_closing_tags = """
</body>
</html>"""

#element names from salesforce report
name = 0
link = 1
company = 2
description = 3
days_open = 4
account_tier = 5
service_level = 6
sr_number = 7
sr_type = 8
status = 9

f_A = open('A.html', 'w+')
f_A.write(html_opening_tags)
f_B = open('B.html', 'w+')
f_B.write(html_opening_tags)
with open('report.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    i = 0
    for row in readCSV:
        if(i==0):
            i += 1
            continue
        if(i%2==0):
            f_A.write("<p> %s    %s,    %s </p>" % (row[days_open], row[name], row[link]))
        else:
            f_B.write("<p> %s    %s,    %s </p>" % (row[days_open], row[name], row[link]))    
        i += 1
    print("Total number of SRs: ", i)


f_A.write(html_closing_tags)
f_A.close
f_B.write(html_closing_tags)
f_B.close    