async function process_csv(csv_file) {
    const response = await fetch("/process/comments/csv", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ csv_file })
    });
    const data = await response.text();
    console.log(data);
}

function readFile(file) {

  // FileReader-Objekt initialisieren
  /*const reader = new FileReader();

  // Event-Listener für das Abschließen des Dateiladevorgangs
  reader.onload = function(e) {
    const csvData = e.target.result;

    // Hier kannst du die csvData an deine Verarbeitungsfunktion übergeben
    process_csv(csvData);
  };

  // CSV-Datei lesen
  reader.readAsText(file);*/
  const reader = new FileReader();

  reader.onload = function(e) {
    const text = e.target.result;
    processCSV(text);
  };

  reader.readAsText(file);

  function processCSV(text) {
  // Split the text into an array of lines
  const lines = text.split('\\n');
  lines.forEach(line => {
    const columns = line.split(',');
    // Handle the columns array
  });
}
    console.log();
  //process_csv(file);

}

function submit_button() {
    var x = document.getElementById("fileInput");
    var txt = "";
    console.log(x)
    if ('files' in x) {
        if (x.files.length == 0) {
            txt = "Select one or more files.";
        } else {
            for (var i = 0; i < x.files.length; i++) {
                txt += "<br><strong>" + (i+1) + ". file</strong><br>";
                var file = x.files[i];
                if ('name' in file) {
                    txt += "name: " + file.name + "<br>";
                }
                if ('size' in file) {
                    txt += "size: " + file.size + " bytes <br>";
                }
            }

            for (var i = 0; i < x.files.length; i++) {
                var file = x.files[i];
                readFile(file)
            }
        }
    }
    else {
        if (x.value == "") {
            txt += "Select one or more files.";
        } else {
            txt += "The files property is not supported by your browser!";
            txt  += "<br>The path of the selected file: " + x.value; // If the browser does not support the files property, it will return the path of the selected file instead.
        }
    }
    document.getElementById("demo").innerHTML = txt;

}
