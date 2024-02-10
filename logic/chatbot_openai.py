from logic.csv_read import read_csv
import json
import time
from logic import rezensionen as rez
from openai import OpenAI
import os

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)
def answer(verlauf, prompt):




    with open('logic/data/template1.json', 'r') as file:
        empty = json.load(file)
    with open('logic/data/data_file.json', 'r') as file:
        data_file = json.load(file)
    with open('logic/data/alle_daten.json', 'r') as file:
        alle_daten = json.load(file)
    with open('logic/data/rezensionen_pro_tag.json', 'r') as file:
        rezensionen_pro_tag = json.load(file)
    with open('logic/data/unfreundlichkeit_pro_tag.json', 'r') as file:
        unfreundlichkeit_pro_tag = json.load(file)

    prompt = f"""
        Kontext: Du bist ein chatbot, mit dem sich unterhalten wird. Du gehörst zur Firma 'Pixum' und hast Zugriff auf die Rezensionen dieser. Zudem weißt du, wieviele Rezensionen es an welchem Tag gab, wie freundich die Rezensionen sind, etc. Versuche mit diesen infos alle Fragen zu Rezensionen, wie z.B. Zusammenfassungen einer bestimmten Kategorie, möglichst gut zu beantworten, und dem User so gut, wie es geht zu helfen. Dabei sind die Daten, die gleich folgen sehr wichtig. Denke dir aber auf keinen Fall Daten über Rezensionen aus, sondern benutze nur die, die du gleich bekommst. Sollte die Nachricht allerdings nichts mit den rezensionen/Kunden von 'Pixum' zutun haben, so antworte einfach ganz normal als Freund.
                Alle Kategorien, in die Rezensionen fallen könnten: {empty}.
                Dies sind alle Tage, in denen potentiell Rezensionen geschrieben wurden: {alle_daten}, und hier siehst du, wieviele Rezension pro Kategorie/insgesamt pro Tag geschrieben wurden: {rezensionen_pro_tag}.
                Hier findest du, wie unfreundlich die Rezensionen verfass wurden, pro Kategorie und Tag. 10 heißt sehr unfreundlich, und 1 bedeutet sehr freundlich: {unfreundlichkeit_pro_tag}
                Dies ist der vorangegangene chatverlauf zwischen dir (bot) und dem user: {verlauf}. Oft stehen Nachrichten des Users mit der letzten Nachricht, die du geschrieben hast zusammen.
                Bitte schreibe deine Antwort als gültigen json-string, der so aussieht: {'{ "antwort" : "Hier dann deine Antwort.", "statistik" : null, "kategorien" : null }'}. Halte dich strikt an dieses json-string Format, und ändere daran nichts. Füge auch nicht etwas, wie '```json' ein, da man deine Antwort dann nicht mehr sehen kann.
                Du besitzt die Möglichkeit zusätzlich zu deiner Text-Antwort mt einer Statistik zu den Rezensionen zu antworten. Benutze eine Statistik, um dem User deinen Punkt klarer zu machen. Entscheide selbst, wann eine Statistik angebracht ist, und wähle dann eine aus. Gehe dann auch gerne in deiner Text-antwort auf die Statistik ein. Du musst aber natürlich eine benutzen. Füge zu deinem Antwort-json noch den Schlüssel 'statistik' hinzu, und setze dort als Wert den String, der zu der jeweiligen statistik passt:
                "per_time_all" - Gibt eine Statistik zurück, die pro Tag zeigt, wieviele Rezensionen an diesem Tag geschrieben wurden. Zählt dabei alle Kategorien zusammen.
                "per_category_piechart" - Gibt ein Kuchendiagramm zurück, das Insgesamt zeigt, wieviel Prozent der Statistiken zu welcher überkategorie gehört (Kritik, Fehlerbericht, Lob, Sonstiges.)
                "anger_score_per_time" - Gibt die generelle Freundlichkeit aller Rezensionen pro Tag wieder.
                Für die folgenden Statistiken werden Kategorien benötigt. Verwende immer mindestens eine Kategorie, und denke dir keine aus, sondern nehme nur welche aus den existierenden. Schreibe Kategorien in eine Liste aus Listen. Beispiel: [["Fehlerbericht", "Softwarebug"],["Kritik", "Qualitaet"]]. Diese kann so lang sein, wie du möchtest.
                "per_time_categories_total" - Gibt eine Statistik zurück, die pro Tag die totale Menge der Rezensionen aus ausgewählten Kategorien angibt.
                "per_time_categories_percent" - Dasselbe wie die davor, nur statt totale Menge, wird die menge in Prozent zu der gesamen Menge des Tages wiedergegeben.
                "per_choosed_category_piechart" - Gibt pro ausgewählter Kategorie wieder, wieviel Prozent der allgemeinen Rezensionen zu dieser Kategorie gehören.
                "anger_score_per_time_per_choosed_category" - Zeigt pro ausgewählte Kategorie, was die Durchschnittliche Unfreundlichkeit der Rezensionen pro Tag ist.

                Du kannst in deiner Textantwort auch Leerzeilen verwenden, um die Antwort strukturierter zu machen. Mache einfach ein \\n

        Input: Der User schreibt: {prompt}
        """

    chat_completion = client.chat.completions.create( messages=[
        {
            "role": "user",
            "content": prompt,
        }
    ],
    model="gpt-4",
    )

    print(chat_completion.choices[0].message.content)
    return_dict = json.loads(chat_completion.choices[0].message.content)

    return return_dict
