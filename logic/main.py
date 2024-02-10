import copy
import json

with open('data/data_file.json', 'r') as file:
  data = json.load(file)

filters=[]
index_in_filtered_dic=0
output_kategorien=[]

filtered_comments_list = []
input_status_rezension=""

running=True

def input_in_categories(input):
    global output_kategorien
    if input in output_kategorien:
        return True
    else:
        return False

def init_filtered_dict(filters, data):
    global index_in_filtered_dic
    filtered = data #Nur der gefillterte Teil des Dictionaries.
    filtered_list=[]
    for filter in filters:
        filtered = filtered[filter]
    for comment_key in filtered:
        filtered_list.append(filtered[comment_key])
    index_in_filtered_dic=0
    return filtered_list

def output_new_comment(data_list):
    global index_in_filtered_dic, filters

    if len(data_list) > index_in_filtered_dic:
        while data_list[index_in_filtered_dic]["bearbeitet"]:
            index_in_filtered_dic+=1
        dic=data_list[index_in_filtered_dic]
        return f"\nKeywort: {dic['keyWord']}\nZusammenfassung: {dic['Zusammenfassung']}\n"
    else:
        filters=[]
        return "Du hast alle Rezensionen dieser Kategorie angesehen!\n"

def output_details_comment(data_list):
    global index_in_filtered_dic
    dic=data_list[index_in_filtered_dic]
    return f"\nBestellnummer: {dic['order_id']}\nKI-Einschätzung: {dic['Dringlichkeit']}\nGanze Rezension: {dic['full_comment']}\nDatum: {dic['Datum']}\nKeywort: {dic['keyWord']}\nZusammenfassung: {dic['Zusammenfassung']}\n"

def create_list_for_categories(filtered):
    output_kategorien = []
    for i in filtered:
        output_kategorien.append(i)
    return output_kategorien


def right_input_text(filters, data):
    global index_in_filtered_dic, output_kategorien, input_status_rezension

    filtered=data
    for filter in filters:
        filtered=filtered[filter]

    if len(filters) <= 1:
        output_kategorien=create_list_for_categories(filtered)
        output_str= f"Bitte wähle eine Kategorie aus: {', '.join([str(item) for item in output_kategorien])}\n"
    else:
        output_kategorien=[]
        if input_status_rezension == "m":
            print_comment=output_details_comment(filtered_comments_list)
        else:
            print_comment=output_new_comment(filtered_comments_list)
        if len(filters)==2:
            output_str= f"{print_comment}\nMoechtest du mehr Details dieser Rezension ansehen (m), oder zur naechsten Rezension kommen, und diese als bearbeitet markieren, oder unbearbeitet lassen(y/n)?\n"
        else:
            output_str=f"{print_comment}Bitte wähle eine Kategorie aus: {', '.join([str(item) for item in output_kategorien])}\n"
    return output_str

def verarbeite_input(input):
    global filters, data, filtered_comments_list, input_status_rezension, index_in_filtered_dic, filtered_comments_list, running
    if input != "":
        if input == "esc":
            running = False
        elif input == "back":
            if len(filters) >= 1:
                filters.pop(-1)
        elif input_in_categories(input):
            filters.append(input)
            if len(filters)==2:
                filtered_comments_list=init_filtered_dict(filters,data)
        elif len(filters)>=2:
            if input == "m":
                input_status_rezension="m"
            elif input == "y":
                input_status_rezension="y"
                filtered_comments_list[index_in_filtered_dic]["bearbeitet"]=True
                index_in_filtered_dic+=1
            elif input == "n":
                input_status_rezension="n"
                index_in_filtered_dic+=1
        else:
            print("Nicht in Kategorien.")



print("Filtere, durch die Befehle, die dir angezeigt werden. Gebe jederzeit 'esc' ein, um das Programm abzubrechen, und die Daten zu speichern, \nund schreibe 'back', um nocheinmal die Filterkategorien auszuwaehlen.\n")
while running:
    verarbeite_input(input(right_input_text(filters, data)))