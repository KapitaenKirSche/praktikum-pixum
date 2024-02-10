import vertexai
from vertexai.language_models import TextGenerationModel
import google.auth
import rezensionen
from csv_read import read_csv
import json
import time
import test_functions

comments=read_csv()

with open('../../logic/data/data_file.json', 'r') as file:
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

resp_id=1



with open('../../logic/data/template1.json', 'r') as file:
    empty1 = file.read()
with open('../../logic/data/example_a.json', 'r') as file:
    filled1 = file.read()

i=0
for key in comments:
    i+=1
    response = model.predict(
        f"""
        Input: Kontext: Ordne die Rezension in das json-file ein.
                        Unter der Kategorie, die du als am passendsten für die Rezension erachtest (Beispiel für eine Kategorie: Kritik,Vielfalt; oder Fehlerbericht,Druckfehler) benutzt du die order-id als Schlüssel, schreibst zu folgenden Schlüsseln passende Werte.
                        die Schlüssel:  'keyWord', dort beschreibst du die Rezension in einem Wort.
                                        'Dringlichkeit', dort schätzt du von mit einer ganzen Zahl von 1-10 ein, für wie wichtig du es erachtest, dass die Rezension schnell angesehen wird. Bugreports sollten z.B. schnell angesehen werden, sodass man sie beheben kann.
                                        'Zusammenfassung', dort fasst du die Rezension in einem kurzen Satz zusammen.
                        Einwenig Infos zu den Kategorien, in die du einsotieren sollst: 
                                        'Service', dort kommen nur kommentare rein, die den Service loben/kritisieren. Also z.B. kommentare über den Kundenservice, Kundenberatung(auch wenn über software(z.B. chaatbot), etc.), oder Lieferzeiträume, nicht aber um den Umgang mit der Software.
                                        'Benutzerfreundlichkeit', dort kommen nur kommentare die die Benutzerfreundlichkeit loben/kritisieren. Dazu gehört z.B. auch der Bestelvorgang.

        Kundenrezension: {2464993, rezensionen.a}
        RezensionsID: {42}
        JSON-Datei zum einordnen: {empty1}
        output: {filled1}
        
        Input: Kontext: Ordne die Rezension in das json-file ein.
                        Unter der Kategorie, die du als am passendsten für die Rezension erachtest (Beispiel für eine Kategorie: Kritik,Vielfalt; oder Fehlerbericht,Druckfehler) benutzt du die order-id als Schlüssel, schreibst zu folgenden Schlüsseln passende Werte.
                        die Schlüssel:  'keyWord', dort beschreibst du die Rezension in einem Wort.
                                        'Dringlichkeit', dort schätzt du von mit einer ganzen Zahl von 1-10 ein, für wie wichtig du es erachtest, dass die Rezension schnell angesehen wird. Bugreports sollten z.B. schnell angesehen werden, sodass man sie beheben kann.
                                        'Zusammenfassung', dort fasst du die Rezension in einem kurzen Satz zusammen.
                        Einwenig Infos zu den Kategorien, in die du einsotieren sollst: 
                                        'Service', dort kommen nur kommentare rein, die den Service loben/kritisieren. Also z.B. kommentare über den Kundenservice, Kundenberatung(auch wenn über software(z.B. chaatbot), etc.), oder Lieferzeiträume, nicht aber um den Umgang mit der Software.
                                        'Benutzerfreundlichkeit', dort kommen nur kommentare die die Benutzerfreundlichkeit loben/kritisieren. Dazu gehört z.B. auch der Bestelvorgang.

        Kundenrezension: {key,comments[key]}
        JSON-Datei zum einordnen: {empty1}
        RezensionsID: {resp_id}
        output:
        """,
        **parameters
    )


    data_dict = json.loads(response.text)

    for key1 in data_dict:
        nested_dict=data_dict[key1]
        for key2 in nested_dict:
            if nested_dict[key2] != {}:
                for key3 in nested_dict[key2]:

                    complete_dictionary[key1][key2][key3]=nested_dict[key2][key3]
                    complete_dictionary[key1][key2][key3]["order_id"] = key
                    complete_dictionary[key1][key2][key3]["Datum"]=comments[key]["date"]
                    complete_dictionary[key1][key2][key3]["user_id"]=comments[key]["user_id"]
                    complete_dictionary[key1][key2][key3]["full_comment"]=comments[key]["comment"]
                    complete_dictionary[key1][key2][key3]["bearbeitet"]=False

    print(f"Fertig mit Nummer {i}")
    print("\n")
    time.sleep(8)

print("\n\n\n")
print(test_functions.calc_dif(complete_dictionary))
with open('../../logic/data/data_file.json', 'w') as file:
    json.dump(complete_dictionary, file, indent=4)