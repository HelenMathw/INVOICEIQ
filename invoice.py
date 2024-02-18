import os
import cv2
import pytesseract
import re
import csv


img_dir = 'D:\invoiceimages'
out_path = 'D:\invoiceimages\ textfile.txt'

config = ('-l eng --oem 1 --psm 3')

# Regular expressions to extract relevant information

product_id_regex = r'PRODUCT\s*ID\s*:\s*(\d+)'
item_name_regex = r'ITEM\s*NAME\s*:\s*(.*)'
purchase_id_regex = r'PURCHASE\s*ID\s*:\s*(\d+)'
date_of_purchase_regex = r'DATE\s*OF\s*PURCHASE\s*:\s*(\d{2}/\d{2}/\d{4})'
due_date_regex = r'DUE\s*DATE\s*:\s*(\d{2}/\d{2}/\d{4})'
supplier_code_regex = r'SUPPLIER\s*CODE\s*:\s*(\d+)'
supplier_name_regex = r'SUPPLIER\s*NAME\s*:\s*(.*)'
contact_info_regex = r'CONTACT\s*INFO\s*:\s*(.*)'
#r'CGST\s*:\s*(.*)'
cgst_info_regex = r'CGST:\s*(\d+\.\d+)'
sgst_info_regex = r'SGST\s*:\s*(.*)'

# Function to extract text after encountering 'Item' until 'Contact Info'
def extract_text(text):
    item_index = text.upper().find('ITEM')  # Find index of 'Item'
    contact_info_match = re.search(contact_info_regex, text, re.IGNORECASE)  # Find 'Contact Info'
    
    if item_index != -1 and contact_info_match:
        start_index = item_index + len('ITEM')  # Start index after 'Item'
        end_index = contact_info_match.start()  # End index before 'Contact Info'
        extracted_text = text[start_index:end_index].strip()  # Extract text in between
    else:
        extracted_text = ""
    
    return extracted_text

# Open the output file
with open(out_path, 'w') as out_file:
    write_flag = False  # Flag to indicate when to start writing
    for img_name in os.listdir(img_dir):
        if img_name.endswith('.jpeg') or img_name.endswith('.jpg')or img_name.endswith('.png'):
            # Read the image
            img_path = os.path.join(img_dir, img_name)
            img = cv2.imread(img_path)

            # Perform OCR
            text = pytesseract.image_to_string(img, config=config)

            # Extract text between 'Item' and 'Contact Info'
            extracted_text = extract_text(text)
            product_id_match = re.search(product_id_regex, text, re.IGNORECASE)
            item_name_match = re.search(item_name_regex, text, re.IGNORECASE)
            purchase_id_match = re.search(purchase_id_regex, text, re.IGNORECASE)
            date_of_purchase_match = re.search(date_of_purchase_regex, text, re.IGNORECASE)
            due_date_match = re.search(due_date_regex, text, re.IGNORECASE)
            supplier_code_match = re.search(supplier_code_regex, text, re.IGNORECASE)
            supplier_name_match = re.search(supplier_name_regex, text, re.IGNORECASE)
            contact_info_match = re.search(contact_info_regex, text, re.IGNORECASE)
            cgst_info_match = re.search(cgst_info_regex, text, re.IGNORECASE)
            sgst_info_match = re.search(sgst_info_regex, text, re.IGNORECASE)

            # Write the extracted information to the output file
            out_file.write(f'--- {img_name} ---\n')
            if product_id_match:
                out_file.write(f'Product ID: {product_id_match.group(1)}\n')
            if purchase_id_match:
                out_file.write(f'Purchase ID: {purchase_id_match.group(1)}\n')
            if date_of_purchase_match:
                out_file.write(f'Date of Purchase: {date_of_purchase_match.group(1)}\n')
            if due_date_match:
                out_file.write(f'Due Date: {due_date_match.group(1)}\n')
            if supplier_code_match:
                out_file.write(f'Supplier Code: {supplier_code_match.group(1)}\n')
            if supplier_name_match:
                out_file.write(f'Supplier Name: {supplier_name_match.group(1)}\n')
            

            out_file.write('\n')
            

            # Check if 'Item' is found to start writing
            if "ITEM" in text.upper():
                write_flag = True

            if write_flag:
                # Write everything encountered after 'Item'
                out_file.write(extracted_text)

            # Stop writing if 'Contact Info' is encountered
            if "CONTACT INFO" in text.upper():
                write_flag = False

            #if contact_info_match:
                #out_file.write(f'Contact Info: {contact_info_match.group(1)}\n')
            if cgst_info_match:
                out_file.write(f'CGST:{cgst_info_match.group(1)}\n')
            if sgst_info_match:
                out_file.write(f'SGST:{sgst_info_match.group(1)}\n')
            out_file.write('\n')

            print(f"Extracted data from {img_name}")

print(f"Extracted data from all images saved to {out_path}")


import re
import csv

def extract_invoice_data1(invoice_text):
    pattern = r"Supplier Code: (\d+)\nSupplier Name: ([^\n]+)\nContact Info: ([^\n]+)"
    match = re.search(pattern, invoice_text)
    if match:
        return match.groups()
    else:
        return None

def extract_product_data1(invoice_text):
    product_data = []
    lines = invoice_text.split('\n')
    for line in lines[4:]:
        if line.startswith("CGST") or line.startswith("Total"):
            break  # Stop processing when reaching CGST or Total lines
        parts = line.split()
        if len(parts) >= 5:  # Assuming correct format for product lines
            try:
                # Try to convert parts[-4] to an integer
                order_quantity = int(parts[-4])
                item_name = " ".join(parts[:-4])  # Extract all words of the product name
                product_data.append({
                    'ProductID': len(product_data) + 1,
                    'ItemName': item_name,
                    'orderquantity': order_quantity,
                    'priceperitem': float(parts[-3]),
                    'totalprice': float(parts[-1]),  # Swapped with taxpercentage
                    #'suppliercode': extract_invoice_data(invoice_text)[0],
                    'taxpercentage': float(parts[-2])  # Swapped with totalprice
                })
            except ValueError:
                # Skip the line if parts[-4] cannot be converted to an integer
                continue
    return product_data

def parse_products_to_csv1(invoice_texts, csv_filename):
    fieldnames = ['ProductID', 'ItemName', 'orderquantity', 'priceperitem', 'totalprice', 'taxpercentage']
    with open(csv_filename, mode='w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for invoice_text in invoice_texts:
            product_data = extract_product_data1(invoice_text)
            for product in product_data:
                writer.writerow(product)

def read_invoices_from_file1(file_name):
    with open(file_name, 'r') as file:
        invoice_texts = file.read().split("---")
        return invoice_texts[1:]  # Skipping the first element which is empty
    return []

invoice_texts = read_invoices_from_file1(out_path)
csv_filename = "products.csv"
parse_products_to_csv1(invoice_texts, csv_filename)

from datetime import datetime

def extract_invoice_data2(invoice_text):
    pattern = r"Purchase ID: (\d+)"
    match = re.search(pattern, invoice_text)
    if match:
        return match.group(1)
    else:
        return None

def extract_due_date2(invoice_text):
    pattern = r"Pay by: ([^\n]+)"
    match = re.search(pattern, invoice_text)
    if match:
        date_str = match.group(1)
        return datetime.strptime(date_str, "%d %B %Y").date()
    else:
        return None

def extract_cgst_sgst2(invoice_text):
    cgst = sgst = None
    lines = invoice_text.split('\n')
    for line in lines:
        if line.startswith("CGST"):
            cgst_match = re.match(r"CGST (\d+(\.\d+)?)", line)
            if cgst_match:
                cgst = float(cgst_match.group(1))
        elif line.startswith("SGST"):
            sgst_match = re.match(r"SGST (\d+(\.\d+)?)", line)
            if sgst_match:
                sgst = float(sgst_match.group(1))
    return cgst, sgst

def extract_product_data2(invoice_text):
    product_data = []
    lines = invoice_text.split('\n')
    for line in lines:
        if line.startswith("Total"):
            break  # Stop processing when reaching Total line
        parts = line.split()
        if len(parts) >= 5:  # Assuming correct format for product lines
            try:
                # Try to convert parts[-4] to an integer
                order_quantity = int(parts[-4])
                item_name = " ".join(parts[:-4])  # Extract all words of the product name
                product_data.append({
                    'ProductID': len(product_data) + 1,
                    'ItemName': item_name,
                    'orderquantity': order_quantity,
                    'priceperitem': float(parts[-3]),
                    'totalprice': float(parts[-1]),  # Swapped with taxpercentage
                    'suppliercode': extract_invoice_data2(invoice_text),
                    'taxpercentage': float(parts[-2]),  # Swapped with totalprice
                })
            except ValueError:
                # Skip the line if parts[-4] cannot be converted to an integer
                continue
    return product_data

def parse_products_to_csv2(invoice_texts, csv_filename):
    fieldnames = ['purchaseid', 'productid', 'dateofpurchase', 'duedate', 'cgst', 'sgst']
    with open(csv_filename, mode='w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for invoice_text in invoice_texts:
            purchase_id = extract_invoice_data2(invoice_text)
            if purchase_id is None:
                continue  # Skip this invoice if we couldn't extract the purchase ID
            due_date = extract_due_date2(invoice_text)
            cgst, sgst = extract_cgst_sgst2(invoice_text)
            product_data = extract_product_data2(invoice_text)
            for product in product_data:
                writer.writerow({
                    'purchaseid': purchase_id,
                    'productid': product['ProductID'],
                    'dateofpurchase': datetime.now().date(),
                    'duedate': due_date,
                    'cgst': cgst,
                    'sgst': sgst
                })

def read_invoices_from_file2(file_name):
    with open(file_name, 'r') as file:
        invoice_texts = file.read().split("---")
        return invoice_texts[1:]  # Skipping the first element which is empty
    return []

invoice_texts = read_invoices_from_file2(out_path)
csv_filename = "purchases.csv"
parse_products_to_csv2(invoice_texts, csv_filename)




'''def extract_invoice_data3(invoice_text):
    pattern = r"Supplier Code: (\d+)\nSupplier Name: ([^\n]+)\nContact Info: ([^\n]+)"
    match = re.search(pattern, invoice_text)
    if match:
        return match.groups()
    else:
        return None'''
with open(out_path, 'r') as file:
    lines = file.readlines()
    # Extract relevant information
    products = []
    purchase_id = supplier_code = supplier_name =  None
    for line in lines:
        if line.startswith('---'):
            purchase_id = supplier_code = supplier_name =None
        elif line.startswith('Supplier Code:'):
            supplier_code = line.split(':')[1].strip()
        elif line.startswith('Supplier Name:'):
            supplier_name = line.split(':')[1].strip()
            products.append([ supplier_code, supplier_name,])
# Write the parsed information into a CSV file
with open('supplier.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([ 'Supplier Code', 'Supplier Name'])
    for product in products:
        writer.writerow(product)

