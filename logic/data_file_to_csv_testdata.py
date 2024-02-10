import json
import csv


with open('logic/data/data_file_v1.json', 'r') as file:
    data_file = json.load(file)
    id_numb=42
    headers = ['comment','date_received', 'Property - user_id', 'Property - order_id']
    rows=[]
    for kat1 in data_file:
        for kat2 in data_file[kat1]:
            for key in data_file[kat1][kat2]:
                id=data_file[kat1][kat2][key]
                rows.append([id['full_comment'], id['Datum']+' uhr', 'ausgedacht:'+str(id_numb), id_numb])
                id_numb += 42
    print(headers)
    print(rows)
    with open('logic/data/rezensionen_csv.csv', 'w') as f:
        write = csv.writer(f)
        
        write.writerow(headers)
        write.writerows(rows)
