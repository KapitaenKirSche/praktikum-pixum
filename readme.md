<h1>Projekt zum Kategorisieren und Filtern von Kundenrezensionen</h1>

Das Projekt ist im Ramen meines Praktikums bei Pixum entstanden.

Auszuführende Datei ist "flasktest.py".

Um den Chatbot, oder das Einkategorisieren neuer Dateien zu verwenden, muss man in den Dateien <code>ordne_rezensionen_in_json.py</code> bzw. <code>ordne_rezensionen_in_json_openai.py</code> und <code>chatbot.py</code> bzw. <code>chatbot_openai.py</code> einen Zugriff der Google Vertex AI, bzw. openai, konfigurieren. Zudem müssen die import in Z. 3 und 4 in <code>flasktest.py</code> natürlich auf die files zum jeweils richtigen KI-Modell angepasst werden.

<p>Jeglicher Code wurde im Rahmen des Praktikums geschrieben, einzig und allein <code>ordne_rezensionen_in_json_openai.py</code> und <code>chatbot_openai.py</code> (so wie dieses Readme, und screenshots) sind nach dem Praktikum erstellt wurden, und erstellen eine alternative Llm-Schnittstelle zu der im Praktikum benutzten vertex-AI dar. Openai wurde in den Screenshots fúr das einkategorisieren, und den Chatbot benutzt.
Jegliche Kundendaten, die in den Rezensionen enthalten sind, sind ausgedacht.

Screenshots und videos sind im Verzeichnis <code>screenshots</code> zu finden.
