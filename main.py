import csv
from dotenv import load_dotenv
import os

load_dotenv()


def is_numeric(value):
    try:
        float(value)
        return True
    except ValueError:
        if value.isdigit():
            return True
        else:
            return False

def get_valid_version(version_parts):
    if len(version_parts) == 6:
        if is_numeric(version_parts[3]):
            return version_parts[3]
        else:
            return version_parts[4]

    elif len(version_parts) == 7:
        return version_parts[4]

    elif len(version_parts) == 5:
        return version_parts[3]

    return None

def get_transifex_version_from_url(url):
    
    if url == "https://docs.python.org/" or url == "https://docs.python.org/pt-br/":
        return url

    python_version = get_valid_version(url.split('/'))
    if python_version == "dev":
        return
    
    transifex_version = "python-"+ str(python_version).replace('.', '')

    return transifex_version
    
def get_python_lib_from_url(url):
    if url == "https://docs.python.org/" or url == "https://docs.python.org/pt-br/":
        return url
    
    return url.split('/')[-1]

def mount_transifex_link(transifex_version, python_lib):

    transifex_link = "https://www.transifex.com/python-doc/"+ transifex_version + "/translate/#pt_BR/" + python_lib
    return transifex_link

def process_csv(input_csv):
    priorities_list = []

    with open(input_csv, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
    
        for row in reader:
            
            original_url = row[0]
            
            transifex_version = get_transifex_version_from_url(original_url)
            python_lib = get_python_lib_from_url(original_url)

            if transifex_version is not  None:        
                transifex_link = mount_transifex_link(transifex_version, python_lib)

                priorities_list.append(transifex_link)

    return priorities_list


input_csv_path = 'csv_file.csv'
priorities_list = process_csv(input_csv_path)

for url in priorities_list:
    print(url)