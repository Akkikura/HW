import csv
import re

with open("phonebook_raw.csv", encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=",")
    next(rows, None)
    contacts_list = list(rows)

contacts = {}

for element in contacts_list:
    component = element
    full_name = component[0].split()

    if len(full_name) == 1:
        last_name, name, surname = full_name[0], '', ''
    elif len(full_name) == 2:
        last_name, name, surname = full_name[0], ',', full_name[1]
    else:
        last_name, name, surname = full_name[0], full_name[1], full_name[2]

    phone = component[5]
    phone = re.sub('(\+7|8)?\s*\((\d+)\)\s*(\d+)[\s-](\d+)[\s-](\d+)(\s+)(\()?(\w+)(\.)(\s+)(\d+)',
                   r"+7(\2)\3-\4-\5 \8\9 \11", phone)

    if phone not in contacts:
        contacts[phone] = {
            'last_name': last_name,
            'name': name,
            'surname': surname,
            'organization': component[3],
            'position': component[4],
            'email': component[6]
        }

        
with open("phonebook.csv", "w", encoding='utf-8') as f:
    fieldnames = ['last_name', 'name', 'surname', 'organization', 'position', 'phone', 'email']
    datawriter = csv.DictWriter(f, fieldnames=fieldnames)
    datawriter.writeheader()
    for phone, contact_info in contacts.items():
        datawriter.writerow({
            'last_name': contact_info['last_name'],
            'name': contact_info['name'],
            'surname': contact_info['surname'],
            'organization': contact_info['organization'],
            'position': contact_info['position'],
            'phone': phone,
            'email': contact_info['email']

        })
print('Data updated.')
