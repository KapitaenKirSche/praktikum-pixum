import vertexai
from vertexai.language_models import TextGenerationModel
import google.auth
from logic.csv_read import read_csv
import json
import time
from logic import rezensionen as rez


def ordne_in_json(order_id_and_key, comment):
    with open('logic/data/data_file.json', 'r') as file:
        complete_dictionary = json.load(file)

    creds, _ = google.auth.default(quota_project_id='pixum-machine-learning')
    vertexai.init(project="pixum-machine-learning", location="europe-west3", credentials=creds)

    parameters = {
        "candidate_count": 1,
        "max_output_tokens": 2048,
        "temperature": 0,
        "top_p": 1
    }
    model = TextGenerationModel.from_pretrained("text-bison")

    resp_id = 1

    with open('logic/data/template1.json', 'r') as file:
        empty1 = file.read()
    with open('logic/data/example_a.json', 'r') as file:
        filled1 = file.read()

    response = model.predict(
        f"""
        Input: Kontext: Ordne die Rezension in das json-file ein.
                        Unter der Kategorie, die du als am passendsten für die Rezension erachtest (Beispiel für eine Kategorie: Kritik,Vielfalt; oder Fehlerbericht,Druckfehler) benutzt du die order-id als Schlüssel, schreibst zu folgenden Schlüsseln passende Werte.
                        die Schlüssel:  'keyWord', dort beschreibst du die Rezension in einem, oder zwei Wörtern. Bitte vermeide nichtsaussagende Worte wie zum Beispiel 'negativ', 'positiv', oder 'Softwarebug, beschreibe aber nicht so genau, wie in der Zusammefassung.
                                        'Dringlichkeit', dort schätzt du von mit einer ganzen Zahl von 1-10 ein, für wie wichtig du es erachtest, dass die Rezension schnell angesehen wird. Bugreports sollten z.B. schnell angesehen werden, sodass man sie beheben kann.
                                        'Zusammenfassung', dort fasst du die Rezension in einem kurzen Satz zusammen.
                                        'anger_score', hier beschreibst du, wie wütend, bzw. wie unfreundlich der Ton der Rezension war. Ordne sie dafür in einen Score von 1-10 ein, wobei 8-10 sehr wütend, 6-7 wütend, beziehhungsweise unfreundlich, 5 neutral, und alle Abstufungen darunter verschiedene Abstufungen von freundlich sind.
                        Einwenig Infos zu den Kategorien, in die du einsotieren sollst: 
                                        'Service', dort kommen nur kommentare rein, die den Service loben/kritisieren. Also z.B. kommentare über den Kundenservice, Kundenberatung(auch wenn über software(z.B. chaatbot), etc.), oder Lieferzeiträume, nicht aber um den Umgang mit der Software.
                                        'Benutzerfreundlichkeit', dort kommen nur kommentare die die Benutzerfreundlichkeit loben/kritisieren. Dazu gehört z.B. auch der Bestelvorgang.
                                        'Softwarebug', dort kommen wirklich nur Kommentare rein, die über einen Softwwarebug sprechen. Sollten sie z.B. darüber berichten, dass sie einen Button nicht finden, so ordne sie in Kritik/Benutzerfrendlichkeit ein.

        Kundenrezension: {2464993, rez.a}
        RezensionsID: {42}
        JSON-Datei zum einordnen: {empty1}
        output: {filled1}

        Input: Kontext: Ordne die Rezension in das json-file ein.
                        Unter der Kategorie, die du als am passendsten für die Rezension erachtest (Beispiel für eine Kategorie: Kritik,Vielfalt; oder Fehlerbericht,Druckfehler) benutzt du die order-id als Schlüssel, schreibst zu folgenden Schlüsseln passende Werte.
                        die Schlüssel:  'keyWord', dort beschreibst du die Rezension in einem, oder zwei Wörtern. Bitte vermeide nichtsaussagende Worte wie zum Beispiel 'negativ', 'positiv', oder 'Softwarebug, beschreibe aber nicht so genau, wie in der Zusammefassung.
                                        'Dringlichkeit', dort schätzt du von mit einer ganzen Zahl von 1-10 ein, für wie wichtig du es erachtest, dass die Rezension schnell angesehen wird. Bugreports sollten z.B. schnell angesehen werden, sodass man sie beheben kann.
                                        'Zusammenfassung', dort fasst du die Rezension in einem kurzen Satz zusammen.
                                        'anger_score', hier beschreibst du, wie wütend, bzw. wie unfreundlich der Ton der Rezension war. Ordne sie dafür in einen Score von 1-10 ein, wobei 8-10 sehr wütend, 6-7 wütend, beziehhungsweise unfreundlich, 5 neutral, und alle Abstufungen darunter verschiedene Abstufungen von freundlich sind.
                        Einwenig Infos zu den Kategorien, in die du einsotieren sollst: 
                                        'Service', dort kommen nur kommentare rein, die den Service loben/kritisieren. Also z.B. kommentare über den Kundenservice, Kundenberatung(auch wenn über software(z.B. chaatbot), etc.), oder Lieferzeiträume, nicht aber um den Umgang mit der Software.
                                        'Benutzerfreundlichkeit', dort kommen nur kommentare die die Benutzerfreundlichkeit loben/kritisieren. Dazu gehört z.B. auch der Bestelvorgang.
                                        'Softwarebug', dort kommen wirklich nur Kommentare rein, die über einen Softwwarebug sprechen. Sollten sie z.B. darüber berichten, dass sie einen Button nicht finden, so ordne sie in Kritik/Benutzerfrendlichkeit ein.

        Kundenrezension: {order_id_and_key, comment}
        JSON-Datei zum einordnen: {empty1}
        RezensionsID: {resp_id}
        output:
        """,
        **parameters
    )

    data_dict = json.loads(response.text)
    return_dict = {}

    for key1 in data_dict:
        nested_dict = data_dict[key1]
        for key2 in nested_dict:
            if nested_dict[key2] != {}:
                return_dict['kategorien'] = (key1,key2)
                for key3 in nested_dict[key2]:
                    complete_dictionary[key1][key2][key3] = nested_dict[key2][key3]
                    return_dict['dictionary']=nested_dict[key2][key3]
                    complete_dictionary[key1][key2][key3]["order_id"] = order_id_and_key
                    return_dict['dictionary']['order_id']=order_id_and_key
                    complete_dictionary[key1][key2][key3]["Datum"] = comment["date"]
                    return_dict['dictionary']['Datum'] = comment['date']
                    complete_dictionary[key1][key2][key3]["user_id"] = comment["user_id"]
                    return_dict['dictionary']['user_id'] = comment['user_id']
                    complete_dictionary[key1][key2][key3]["full_comment"] = comment["comment"]
                    return_dict['dictionary']['full_comment'] = comment['comment']
                    complete_dictionary[key1][key2][key3]["bearbeitet"] = False
                    return_dict['dictionary']['bearbeitet'] = False


    with open('logic/data/data_file.json', 'w') as file:
        json.dump(complete_dictionary, file, indent=4)



    return return_dict
