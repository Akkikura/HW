import csv
import itertools
import operator
import re

i = 0
contacts_dict = []
with open('phonebook_raw.csv', encoding="utf8") as f:
    reader = csv.reader(f, delimiter=",")
    contacts_list = list(reader)
    for items in contacts_list:
        pattern_phone = r'(\+7|8)?\s*\(?(\d{3})\)?[\s*-]?(\d{3})[\s*-]?(\d{2})[\s*-]?(\d{2})(\s*)\(?(доб\.?)?\s*(\d*)?\)?'
        fixed_phone = re.sub(pattern_phone, r'+7(\2)\3-\4-\5\6\7\8', items[5])
        contacts_list[i][5] = fixed_phone
        try:
            i += 1
        except IndexError:
            break

    keys = contacts_list[0]
    values = contacts_list[1:]
    for num, vals in enumerate(values):
        contacts_dict.append({})
        for key, val in zip(keys, vals):
            contacts_dict[num].update({key: val})
    for v in contacts_dict:
        splt = v['lastname'].split(' ')
        if len(splt) > 1:
            v['lastname'] = splt[0]
            v['firstname'] = splt[1]
            if len(splt) > 2:
                v['surname'] = splt[2]

        splt = v['firstname'].split(' ')
        if len(splt) > 1:
            v['firstname'] = splt[0]
            v['surname'] = splt[1]
    all_keys = set(contacts_dict[0].keys())
    group_list = ['firstname', 'lastname']
    group = operator.itemgetter(*group_list)
    cols = operator.itemgetter(*(all_keys ^ set(group_list)))
    contacts_dict.sort(key=group)
    grouped = itertools.groupby(contacts_dict, group)

    merge_data = []
    for (firstname, lastname), g in grouped:
        merge_data.append({'lastname': lastname, 'firstname': firstname})
        for gr in g:
            d1 = merge_data[-1]
            for k, v in gr.items():
                if k not in d1 or d1[k] == '':
                    d1[k] = v
keys = list(merge_data[0].keys())
with open('phonebook.csv', "w", encoding="utf8") as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerow(keys)
    for d in merge_data:
        datawriter.writerow(d.values())

print('Data updated.')
