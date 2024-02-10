import csv

rezensionen_csv = open('../Website_CSAT_DE_answers_at_2024-01-15T14 03 56.csv', encoding='utf-8')
csvreader=csv.reader(rezensionen_csv)

spalten_namen=next(csvreader)

rows = []
for row in csvreader:
   rows.append(row)

spaltenname_to_index={

}
for i in range(len(spalten_namen)):
    spaltenname_to_index[spalten_namen[i]]=i
print(spaltenname_to_index)

zeile=1
spalte=1

for comment_line in rows:
    sti=spaltenname_to_index
    print(comment_line[7])

while True:
    if input():
        print(f"Zeile {zeile} Spalte {spalte}: '{rows[zeile][spalte-1]}'    Spaltename: '{spalten_namen[spalte-1]}'")
        spalte+=1
        if spalte > len(rows[0]):
            spalte=1
            zeile+=1
            if zeile > len(rows):
                print("Ende")
                break