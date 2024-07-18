from datetime import datetime
import os
import fnmatch
import csv

#Getting current date
def get_date():
    date = datetime.today().strftime("%d.%m.%Y")
    date_day = date[:2]
    date_month = date[3:5]
    date_year = date[-4:]
    return date_day, date_month, date_year

class txt_operations:
    #Creating monthly invoice counter as .txt file if needed
    def create_invoice_counter():
        if not os.path.isfile(f'invoices_counter.txt'):
            with open(f"invoices_counter.txt", 'w') as fv_counter_file:
                fv_counter_file.write('0')

    #Getting current invoice number from .txt file
    def get_invoice_counter():
        with open(f"invoices_counter.txt", "r+") as fv_counter_file:
            fv_counter_file = open(f"invoices_counter.txt", "r+")
            fv_counter = fv_counter_file.read()
            fv_counter = int(fv_counter)
            fv_counter_file.close()
        return fv_counter

    # Updating invoices counter
    def update_invoice_counter(fv_counter):
        with open(f"invoices_counter.txt", "w") as fv_counter_file:
            fv_counter_file.write(f"{fv_counter}")
            fv_counter_file.close()

def deleting_previous_pdfs():
    for file in os.listdir(f'Invoices'):
        if fnmatch.fnmatch(file, '*.pdf'):
            os.remove(os.path.join(f'Invoices', file))

#Opening .csv file generated via Allegro representing account balance changes, in following subpage ->
def read_csv(file_path):
    #1. 'Funds and Operations History' [eng]
    #2. 'Środki i historia operacji' [pl]
    #3. Кошти та історія операцій' [ukr]
    with open(file_path, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        #Reversed to properly keep orders chronology
        #in file, newest records are on top
        records = list(csv_reader)
        records.reverse()

        #Creating table //orders// which only includes orders, selecting from all records on account
        orders = []
        for record in records:
            #'operacja' - transl. operation
            #'wplata' - transl. income
            if record['operacja'] == 'wpłata' and 'refund' not in record['oferta']:
                orders.append(record)

        return orders

#Creating folder for created invoices
def create_invoices_folder():
    if not os.path.isdir(f'Invoices'):
        os.makedirs(f'Invoices')
