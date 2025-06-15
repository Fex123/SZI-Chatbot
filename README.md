# SZI-Chatbot

Im Rahmen einer umfassenden Studienarbeit mit einer Bearbeitungszeit von sechs Monaten wurde dieses Projekt an der DHBW-Lörrach im Studiengang Informatik durchgeführt.
Das Ziel bestand darin, einen KI-Chatbot zu entwickeln, der dazu in der Lage ist, Fragen über das Studienzentrum Informatik und insbesondere zu den Richtlinien für wissenschaftliches Arbeiten zu beantworten.
Die Realisierung des Chatbots sollte mit einem LLM erfolgen, der on-Premise auf den Systemen der DHBW implementiert wird (ohne den Einsatz von KI-APIs).

Das Endprodukt besteht aus 3 wesentlichen Komponenten:
1. Einem React Frontend, mit modernen Design und der visuellen Identität der DHBW.
2. Einem Flask Backend, zur Verwaltung der Chats, Anfragen und Nutzer
3. Einem KI-Backend uner Verwendung des Open-Source Tools [Dify](https://github.com/langgenius/dify).

Das Endresultat ist eine moderne Webanwendung, welche spezifische Fragen zu den Richtlinien beantworten und verständlich darstellen kann.

# Anleitung
## Projekt aufsetzen
1. Erstellen Sie zunächst einen Ordner, indem das Projekt aufgebaut wird
2. Klonen sie die SZI-Chatbot Repository von Github

```bash
git clone https://github.com/Fex123/SZI-Chatbot
```

3. Klonen sie die dify Repository von Github

```bash
git clone https://github.com/langgenius/dify.git --branch 1.0.1
```

4. Ersetzen sie die docker-compose.yaml von dify (dify/docker/) mit der docker-compose.yaml aus der SZI-Chatbot repository
5. Erstelle sie eine .env<br/>
_In Linux:_

```bash
cp .env.example .env
```

_In Windows:_

Erstellen sie  eine .env Datei und kopieren sie den kompletten Inhalt der
.env.example Datei  hinein
6. Stellen Sie in der .env Datei den “EXPOSE_NGINX_PORT” von 80 auf 3100 an (optional für lokales Aufsetzen)

7. Passen sie im SZI-Chatbot unter testapi die conf.py an (Siehe Kommentar in Zeile)
8. Starten sie die geänderte docker-compose in der dify Repository (dify/docker/)

```bash
docker-compose up -build
```

9. Gehen sie auf localhost:3100 (dify) und importieren sie den DSL Workflow, welcher in der SZI-Chatbot Repository liegt
10. Erstellen sie einen API-Key im Workflow und stoppen sie die docker-compose im docker Verzeichnis der dify Repository  (WICHTIG: Diesen Befehl beim stoppen immer verwenden) Deutscher wenns geht

```bash
docker-compose down
```

11. Fügen Sie folgende Zeile in die .env Datei, welche im gleichen Verzeichnis wie die docker-compose.yaml ist, ein und starten Sie anschließend die docker-compose:
DIFY_API_KEY = “euer_api_key” 


12. Führen Sie nun den folgenden command im docker Verzeichnis der dify Repository  aus: 

```bash
docker exec -it ollama ollama pull phi4
```

Beachten Sie, dass sowohl ein embedding Modell als auch ein LLM benötigt wird. Ideal sind phi4 (LLM, siehe command) und snowflake-arctic-embed2 (embedding Modell)


13. Gehen Sie auf dify (localhost:3100) und binden sie in den Einstellung unter Modell Provider die Modelle ein. Die URL für das Modell lautet: http://ollama:11434
14. Erstellen Sie eine Wissensbasis im Bereich Wissen (Knowledge) und ändern Sie es so wie im Screenshot oben beschrieben. Empfehlung: Markdown Dateien (.md)
15. Fügen Sie die Wissensbasis im Workflow hinzu und fragen Sie in Vorschau (Preview) eine beliebige Frage, damit die erfolgreiche Konfiguration von Dify und ollama durch eine Antwort validiert werden kann.
16. Öffnen Sie das SZI-Chatbot Frontend (localhost:3105) und testen Sie, ob eine Antwort angezeigt wird.

## Projekt starten
Wenn das Projekt aufgesetzt wurde, muss zum Starten in den Ordner dify/docker navigiert werden. Dort muss die docker-compose.yaml ausgeführt werden. Den Flag –build (2 Minus) wird nur benötigt, wenn im Backend oder Frontend was geändert wurde.


```bash
docker-compose up
```
```bash
docker-compose down
```

## Dify aktualisieren
Wenn dify auf den neuesten Stand gebracht werden soll, wird die docker-compose.yaml und die .env Datei eventuell verändert. Das bedeutet, dass sowohl die .env neu eingerichtet werden muss (erneutes copy paste der .env.example und einfügen von DIFY_API_KEY und EXPOSE_NGINX_PORT). Des Weiteren muss die alte docker-compose (liegt im SZI-Chatbot) sorgfältig mit der neuen (nach pull der neuen Dify Version) verglichen werden und vor allem der untere Teil, welche services von uns erstellt wurden, komplett neu eingefügt werden. Folgende Änderungen wurden vorgenommen:
* ssrf_proxy_network zur Kommunikation in einige Container hinzufügen
* SZI-Chatbot Frontend, Backend, MongoDB und Ollama services komplett aus der alten docker-compose.yaml,   welche sich in der SZI-Chatbot Repository befindet, übernommen
* Unter networks die app_network bridge setzen
* MongoDB Volumes setzen
