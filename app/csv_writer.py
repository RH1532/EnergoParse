import csv

def write_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Region', 'District', 'Address', 'Start Date', 'Start Time', 'End Date', 'End Time', 'Type of Work', 'RES', 'Other', 'FIAS'])
        writer.writerows(data)
