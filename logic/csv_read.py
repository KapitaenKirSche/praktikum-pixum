import csv

def read_csv(csv_stream, limit=-1):
    csvreader = csv.reader(csv_stream, delimiter=",")

    rows = [] #Meine Tabelle

    for row in csvreader:
        rows.append(row)

    spalten_namen=rows[0] #Liste alle Elemente der ersten spalte
    del rows[0]

    spaltenname_to_index={

    }
    for i in range(len(spalten_namen)):
        spaltenname_to_index[spalten_namen[i]]=i

    comments={}
    rows=rows[0:limit]#---------------------------------------------------------
    for comment_line in rows:
        sti=spaltenname_to_index

        comment_dic={}
        comment_dic["comment"]=comment_line[sti['comment']]

        comment_dic["date"]=comment_line[sti['date_received']].split()[0]
        comment_dic["user_id"]=comment_line[sti['Property - user_id']]

        comments[comment_line[sti['Property - order_id']]] = comment_dic
    return comments


def ausgabe():

    comments=read_csv()

    print("\n \n")
    i=0
    for key in comments:
        i+=1
        print(f"Kaufnummer: {key}, Kommentar: '{comments[key]['comment']}', User: '{comments[key]['user_id']}' Datum: '{comments[key]['date']}'   Spalte: {i}")
        input()
#ausgabe()