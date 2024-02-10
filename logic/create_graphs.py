import matplotlib
import matplotlib.pyplot as plt

import numpy as np
import json
import io
import base64
import datetime


# Pfad zur JSON-Datei
json_file_path = 'logic/data/data_file.json'

# JSON-Datei einlesen
with open(json_file_path, 'r') as file:
    data_file = json.load(file)

colors = {('Fehlerbericht', 'Softwarebug'): (1.0, 0.0, 0.0),
         ('Fehlerbericht', 'Druckfehler'): (1.0, 0.2, 0.0),
         ('Fehlerbericht', 'Logistikproblem'): (1.0, 0.4, 0.0),
         ('Fehlerbericht', 'Sonstiges'): (1.0, 0.6, 0.0),
         ('Fehlerbericht', 'insgesamt') : 'red',
         ('Kritik', 'Vielfalt'): (0.0, 0.0, 1.0),
         ('Kritik', 'Qualitaet'): (0.0, 0.2, 1.0),
         ('Kritik', 'Benutzerfreundlichkeit'): (0.0, 0.4, 1.0),
         ('Kritik', 'Service'): (0.0, 0.6, 1.0),
         ('Kritik', 'Preis'): (0.0, 0.8, 1.0),
         ('Kritik', 'Sonstiges'): (0.0, 1.0, 1.0),
         ('Kritik', 'insgesamt'): 'blue',
          ('Lob', 'Vielfalt'): (0.0, 0.5, 0.0),
          ('Lob', 'Qualitaet'): (0.0, 0.7, 0.2),
          ('Lob', 'Benutzerfreundlichkeit'): (0.0, 0.8, 0.0),
          ('Lob', 'Service'): (0.1, 0.9, 0.2),
          ('Lob', 'Preis'): (0.2, 1.0, 0.2),
          ('Lob', 'Sonstiges'): (0.3, 1.0, 0.3),
         ('Lob', 'insgesamt'): 'green',
         ('Sonstiges', 'Sonstiges'): (1.0, 1.0, 0.0),
         ('Sonstiges', 'insgesamt'): (1.0, 1.0, 0.0)}

def generate_plot_and_decode(type='per_time_categories_percent', categories=[('Fehlerbericht', 'Softwarebug'), ('Kritik', 'Benutzerfreundlichkeit'), ('Fehlerbericht', 'Logistikproblem')], data=data_file):
    plot = generate_plot(type=type, categories=categories, data=data)

    buffer = io.BytesIO()
    plot.savefig(buffer, format='png')
    buffer.seek(0)

    image_string = base64.b64encode(buffer.read()).decode('utf-8')

    return image_string



def generate_plot(type='per_time_categories_percent', categories=[('Fehlerbericht', 'Softwarebug'), ('Kritik', 'Benutzerfreundlichkeit'), ('Fehlerbericht', 'Logistikproblem')], data=data_file):
    global colors

    matplotlib.use('Agg')

    for i in range(len(categories)):
        categories[i]=(categories[i][0], categories[i][1])


    numbers_per_day = create_list_of_comments_for_each_day(data)
    anger_score_per_day = create_list_of_anger_score_for_each_day(data)
    first_date, last_date = first_and_last(numbers_per_day)
    alle_daten = datespan(first_date, last_date)

    xAxis = []
    yAxis = []
    color_numb=0
    plt.figure(figsize=(13,6))

    if type == 'per_time_categories_total':
        per_time_categories_total(alle_daten, categories, color_numb, colors, numbers_per_day)
    elif type == 'per_time_categories_percent':
        per_time_categories_percent(alle_daten, categories, color_numb, colors, numbers_per_day)
    elif type == 'per_time_all':
        per_time_all(alle_daten, categories, color_numb, colors, numbers_per_day)
    elif type == 'per_category_piechart':
        per_category_piechart(alle_daten, colors, numbers_per_day)
    elif type == 'per_choosed_category_piechart':
        per_choosed_category_piechart(alle_daten, categories, colors, numbers_per_day)

    elif type == 'anger_score_per_time':
        per_time_all_anger(alle_daten, categories, color_numb, colors, anger_score_per_day)
    elif type == 'anger_score_per_time_per_choosed_category':
        per_time_categories_total_anger(alle_daten, categories, color_numb, colors, anger_score_per_day)
    elif type == 'anger_score_piechart':
        pass

    return plt





def per_time_categories_percent(alle_daten, categories, color_numb, colors, numbers_per_day):
    xAxis = generate_x_axis(alle_daten)

    plt.figure(figsize=(10, 6))
    for cat_tuple in categories:
        yAxis = []
        for date in alle_daten:
            if date in numbers_per_day:
                if cat_tuple in numbers_per_day[date]:
                    yAxis.append((numbers_per_day[date][cat_tuple]/numbers_per_day[date]['insgesamt'])*100)
                else:
                    yAxis.append(0)
            else:
                yAxis.append(0)
        plt.plot(xAxis, yAxis, color=colors[cat_tuple], marker='o',
                 label=str(cat_tuple).replace("(", "").replace(")", "").replace("'", ""))

        color_numb += 1

    plt.grid(True)
    plt.legend(loc='upper left', frameon=True)
    plt.xlabel('Tag')
    plt.ylabel('Kommentare (in %)')
    plt.ylim(bottom=-0.12)


def per_time_categories_total(alle_daten, categories, color_numb, colors, numbers_per_day):
    xAxis = generate_x_axis(alle_daten)
    plt.figure(figsize=(10, 6))
    for cat_tuple in categories:
        yAxis = []
        for date in alle_daten:
            if date in numbers_per_day:
                if cat_tuple in numbers_per_day[date]:
                    yAxis.append(numbers_per_day[date][cat_tuple])
                else:
                    yAxis.append(0)
            else:
                yAxis.append(0)
        plt.plot(xAxis, yAxis, color=colors[cat_tuple], marker='o',
                 label=str(cat_tuple).replace("(", "").replace(")", "").replace("'", ""))

        color_numb += 1
    plt.grid(True)
    plt.legend(loc='upper left', frameon=True)
    plt.xlabel('Tag')
    plt.ylabel('Kommentare (insgesamt)')
    plt.ylim(bottom=-0.03)


def per_time_all(alle_daten, categories, color_numb, colors, numbers_per_day):
    xAxis = generate_x_axis(alle_daten)
    yAxis = []
    plt.figure(figsize=(10, 6))
    for date in alle_daten:
        if date in numbers_per_day:
            yAxis.append(numbers_per_day[date]['insgesamt'])
        else:
            yAxis.append(0)
    plt.plot(xAxis, yAxis, color='red', marker='o',
             label='alle Kommentare')

    color_numb += 1
    plt.grid(True)
    plt.legend(loc='upper left', frameon=True)
    plt.xlabel('Tag')
    plt.ylabel('Kommentare (insgesamt)')
    plt.ylim(bottom=-0.03)



def per_category_piechart(alle_daten, colors, numbers_per_day):
    categories = [('Fehlerbericht', 'insgesamt'), ('Kritik', 'insgesamt'), ('Lob', 'insgesamt'), ('Sonstiges', 'Sonstiges')]
    numbers = []
    labels=[]
    plt.figure(figsize=(10, 6))
    all_everyday = 0
    for date in alle_daten:
        if date in numbers_per_day:
            all_everyday += (numbers_per_day[date]['insgesamt'])

    for cat_tuple in categories:
        labels.append(cat_tuple[0])
        this_cat = 0
        for date in alle_daten:
            if date in numbers_per_day:
                if cat_tuple in numbers_per_day[date]:
                    this_cat+=(numbers_per_day[date][cat_tuple])
        numbers.append(this_cat)

    print(numbers)
    colors_for_pie=[]
    for i in categories:
        colors_for_pie.append(colors[i])

    fig, ax = plt.subplots(figsize=(10,6))
    ax.pie(numbers, labels=labels, autopct='%1.1f%%', colors=colors_for_pie, startangle=90)


def per_choosed_category_piechart(alle_daten, choosed_categories, colors, numbers_per_day):
    categories = [('Fehlerbericht', 'insgesamt'), ('Kritik', 'insgesamt'), ('Lob', 'insgesamt'), ('Sonstiges', 'Sonstiges')]
    numbers = []
    labels=[]
    plt.figure(figsize=(10, 6))
    all_everyday = 0
    for date in alle_daten:
        if date in numbers_per_day:
            all_everyday += (numbers_per_day[date]['insgesamt'])

    for cat_tuple in categories:
        labels.append(cat_tuple[0])
        this_cat = 0
        for date in alle_daten:
            if date in numbers_per_day:
                if cat_tuple in numbers_per_day[date]:
                    this_cat+=(numbers_per_day[date][cat_tuple])
        numbers.append([this_cat, cat_tuple[0], []])

    for cat_tuple in choosed_categories:
        this_cat=0
        for date in alle_daten:
            if date in numbers_per_day:
                if cat_tuple in numbers_per_day[date]:
                    this_cat+=(numbers_per_day[date][cat_tuple])
        for list in numbers:
            if list[1]==cat_tuple[0]:
                list[2].append((this_cat, cat_tuple[1]))
    print(numbers)

    final_numbers=[]
    final_labels=[]
    colors_for_pie=[]
    main_index=0
    for main_kategorie in numbers:
        main_kategorie_ausser_allgemein=0
        for kategorie2_tuple in main_kategorie[2]:
            if kategorie2_tuple[1] != 'insgesamt':
                final_numbers.append(kategorie2_tuple[0])
                main_kategorie_ausser_allgemein += kategorie2_tuple[0]
                final_labels.append(kategorie2_tuple[1])
                colors_for_pie.append(colors[(main_kategorie[1], kategorie2_tuple[1])])
        if main_kategorie[0]-main_kategorie_ausser_allgemein >= 1:
            final_numbers.append(main_kategorie[0]-main_kategorie_ausser_allgemein)
            final_labels.append('Rest '+main_kategorie[1])
            colors_for_pie.append(colors[(main_kategorie[1], 'insgesamt')])

        main_index += 1


    fig, ax = plt.subplots(figsize=(10,6))
    wedges, labels, autopct = ax.pie(final_numbers, labels=final_labels, autopct='%1.1f%%', colors=colors_for_pie, startangle=90)


    for label in labels:
        label.set_visible(False)
    for i in autopct:
        i.set_visible(False)

    legend_elements = []

    insgesamt=sum(final_numbers)
    for wedge, size, label in zip(wedges, final_numbers, labels):
        if size >= 1:
            legend_elements.append((wedge, label))  # Füge Kuchenstück zur Legende hinzu
            center = wedge.center
            angle = (wedge.theta2 - wedge.theta1) / 2.0 + wedge.theta1  # Winkel des Kuchenstücks
            radius = wedge.r * 1.1  # Abstand für die Text- und Pfeilposition

            # Füge die Prozentzahl als Text hinzu
            x = 1.1 * np.cos(np.deg2rad(angle))  # X-Koordinate für den Text
            y = 1.1 * np.sin(np.deg2rad(angle))  # Y-Koordinate für den Text
            ax.text(center[0] + x * radius, center[1] + y * radius, f'{round(((size/insgesamt)*100), 1)}%', ha='center', va='center')

            dx = 0.5 * np.cos(np.deg2rad(angle))  # X-Komponente für die Pfeillänge
            dy = 0.5 * np.sin(np.deg2rad(angle))  # Y-Komponente für die Pfeillänge
            ax.arrow(center[0] + x * radius / 2, center[1] + y * radius / 2, dx, dy, width=0.00005, head_length=0.04,
                     head_width=0.025,
                     length_includes_head=True, fc='black', ec='black')

    if len(legend_elements) > 0:
        legend_elements, labels = zip(*legend_elements)
        print((legend_elements))
        print(labels)
        labels = [str(label)[4:] for label in labels]
        labels = [eval(label) for label in labels]

        print(labels)
        labels = [label[2] for label in labels]
        ax.legend(handles=legend_elements, labels=labels, loc="best", bbox_to_anchor=(1, 1, 0, 0))
    plt.rcParams.update({'font.size': 11})




def per_time_all_anger(alle_daten, categories, color_numb, colors, anger_per_day):
    xAxis = generate_x_axis(alle_daten)
    yAxis = []
    plt.figure(figsize=(10, 6))
    for date in alle_daten:
        if date in anger_per_day:
            yAxis.append(berechne_durchschnitt(anger_per_day[date]['insgesamt']))
        else:
            yAxis.append(0)
    plt.plot(xAxis, yAxis, color='red', marker='o',
             label='alle Kommentare')

    color_numb += 1
    plt.grid(True)
    plt.legend(loc='upper left', frameon=True)
    plt.xlabel('Tag')
    plt.ylabel('Unfreundlichkeit (Durchschnitt)')
    plt.ylim(bottom=-0.03)


def per_time_categories_total_anger(alle_daten, categories, color_numb, colors, anger_per_day):
    xAxis = generate_x_axis(alle_daten)
    plt.figure(figsize=(10, 6))
    for cat_tuple in categories:
        yAxis = []
        for date in alle_daten:
            if date in anger_per_day:
                if cat_tuple in anger_per_day[date]:
                    yAxis.append(berechne_durchschnitt(anger_per_day[date][cat_tuple]))
                else:
                    yAxis.append(0)
            else:
                yAxis.append(0)
        plt.plot(xAxis, yAxis, color=colors[cat_tuple], marker='o',
                 label=str(cat_tuple).replace("(", "").replace(")", "").replace("'", ""))

        color_numb += 1
    plt.grid(True)
    plt.legend(loc='upper left', frameon=True)
    plt.xlabel('Tag')
    plt.ylabel('Unfreundlichkeit (Durchschnitt)')
    plt.ylim(bottom=-0.03)



def generate_x_axis(datespan):
    x_axis = []
    for date_str in datespan:
        append_text = ''
        current_date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
        append_text += (current_date.strftime('%a')) + '.'
        append_text += ' ' + (current_date).strftime('%d.%m')
        x_axis.append(append_text)
    return x_axis

def first_and_last(data):
    datetime_dates = [datetime.datetime.strptime(date, '%Y-%m-%d') for date in data.keys()]
    min_date = min(datetime_dates).strftime('%Y-%m-%d')
    max_date = max(datetime_dates).strftime('%Y-%m-%d')
    return min_date, max_date

def datespan(kleinstes_datum, groesstes_datum):
    alle_daten = []

    start = datetime.datetime.strptime(kleinstes_datum, '%Y-%m-%d')
    end = datetime.datetime.strptime(groesstes_datum, '%Y-%m-%d')

    while start <= end:
        formatted_date = start.strftime('%Y-%m-%d')
        if formatted_date[5] == '0':
            if formatted_date[8] == '0':
                formatted_date = formatted_date[:8] + formatted_date[9:]
            formatted_date = formatted_date[:5] + formatted_date[6:]  # Führende Null im Monat entfernen
        elif formatted_date[8] == '0':
            formatted_date = formatted_date[:8] + formatted_date[9:]

        alle_daten.append(formatted_date)
        start += datetime.timedelta(days=1)
    return alle_daten

def create_list_of_comments_for_each_day(data):
    numbers_per_day = {}
    for key1 in data:
        for key2 in data[key1]:
            for comment_key in data[key1][key2]:
                if data[key1][key2][comment_key]['Datum'] not in numbers_per_day:
                    numbers_per_day[data[key1][key2][comment_key]['Datum']] = {}
                    numbers_per_day[data[key1][key2][comment_key]['Datum']][(key1, key2)] = 0
                    numbers_per_day[data[key1][key2][comment_key]['Datum']]['insgesamt'] = 0
                    numbers_per_day[data[key1][key2][comment_key]['Datum']][(key1, 'insgesamt')] = 0
                elif (key1, key2) not in numbers_per_day[data[key1][key2][comment_key]['Datum']]:
                    numbers_per_day[data[key1][key2][comment_key]['Datum']][(key1, key2)] = 0
                if (key1, 'insgesamt') not in numbers_per_day[data[key1][key2][comment_key]['Datum']]:
                    numbers_per_day[data[key1][key2][comment_key]['Datum']][(key1, 'insgesamt')] = 0

                numbers_per_day[data[key1][key2][comment_key]['Datum']][(key1, 'insgesamt')] += 1
                numbers_per_day[data[key1][key2][comment_key]['Datum']][(key1, key2)] += 1
                numbers_per_day[data[key1][key2][comment_key]['Datum']]['insgesamt'] += 1

    return numbers_per_day


def create_list_of_anger_score_for_each_day(data):
    numbers_per_day = {}
    for key1 in data:
        for key2 in data[key1]:
            for comment_key in data[key1][key2]:
                if data[key1][key2][comment_key]['Datum'] not in numbers_per_day:
                    numbers_per_day[data[key1][key2][comment_key]['Datum']] = {}
                    numbers_per_day[data[key1][key2][comment_key]['Datum']][(key1, key2)] = []
                    numbers_per_day[data[key1][key2][comment_key]['Datum']]['insgesamt'] = []
                    numbers_per_day[data[key1][key2][comment_key]['Datum']][(key1, 'insgesamt')] = []
                elif (key1, key2) not in numbers_per_day[data[key1][key2][comment_key]['Datum']]:
                    numbers_per_day[data[key1][key2][comment_key]['Datum']][(key1, key2)] = []
                if (key1, 'insgesamt') not in numbers_per_day[data[key1][key2][comment_key]['Datum']]:
                    numbers_per_day[data[key1][key2][comment_key]['Datum']][(key1, 'insgesamt')] = []

                numbers_per_day[data[key1][key2][comment_key]['Datum']][(key1, 'insgesamt')].append(data[key1][key2][comment_key]['anger_score'])
                numbers_per_day[data[key1][key2][comment_key]['Datum']][(key1, key2)].append(data[key1][key2][comment_key]['anger_score'])
                numbers_per_day[data[key1][key2][comment_key]['Datum']]['insgesamt'].append(data[key1][key2][comment_key]['anger_score'])

    return numbers_per_day

def daten_in_json_hochladen():
    numbers_per_day = create_list_of_comments_for_each_day(data_file)
    anger_score_per_day = create_list_of_anger_score_for_each_day(data_file)
    first_date, last_date = first_and_last(numbers_per_day)
    alle_daten = datespan(first_date, last_date)

    new_numbers_per_day = {}
    for key1, value1 in numbers_per_day.items():
        new_numbers_per_day[key1] = {}
        for key, value in value1.items():
            new_key = str(key[0]+'/'+key[1])
            if key == 'insgesamt':
                new_key='insgesamt'
            new_numbers_per_day[key1][new_key] = value

    new_anger_per_day = {}
    for key1, value1 in anger_score_per_day.items():
        new_anger_per_day[key1] = {}
        for key, value in value1.items():
            new_key = str(key[0] + '/' + key[1])
            if key == 'insgesamt':
                new_key = 'insgesamt'
            new_anger_per_day[key1][new_key] = {}
            new_anger_per_day[key1][new_key]['Durchschnitt'] = berechne_durchschnitt(value)
            new_anger_per_day[key1][new_key]['Median'] = berechne_median(value)

    with open('logic/data/alle_daten.json', 'w') as file:
        json.dump(alle_daten, file, indent = 4)
    with open('logic/data/rezensionen_pro_tag.json', 'w') as file:
        json.dump(new_numbers_per_day, file, indent = 4)
    with open('logic/data/unfreundlichkeit_pro_tag.json', 'w') as file:
        json.dump(new_anger_per_day, file, indent = 4)

def berechne_durchschnitt(liste):
    summe = sum(liste)
    durchschnitt = summe / len(liste)
    return durchschnitt

def berechne_median(numbers):
    sorted_numbers = sorted(numbers)
    n = len(sorted_numbers)
    if n % 2 == 0:
        mid = n // 2
        median = (sorted_numbers[mid - 1] + sorted_numbers[mid]) / 2
    else:
        mid = n // 2
        median = sorted_numbers[mid]
    return median

#generate_plot(type='per_time_categories_total').show()
#generate_plot(type='per_time_categories_percent').show()
#generate_plot(type='per_time_all').show()
#print('fertig')