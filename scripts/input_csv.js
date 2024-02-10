import { io } from "https://cdn.socket.io/4.7.4/socket.io.esm.min.js";

const socket = io();

var current = 0;
var all = 0;

var time_insgesamt = 0;
var time_till_end = 0;

socket.on('processing_started', function(data) {
    if (data['started']) {
        initProcessing();
    }
});

socket.on('zeit', function(data) {
    time_insgesamt = data['insgesamt'];
    time_till_end = data['till_end'];
});

socket.on('processing_status_update', function(data) {
  current = data['files'];
  all = data['insgesamt'];
  new_file_processed(current, all);
});

socket.on('sortierter_kommentar', function(data) {
    var json = JSON.parse(data['json_string']);
    output_kommentar(json);
});


function initProcessing() {
    var headline = document.getElementById('headline');
    headline.innerHTML = 'Hochladen erfolgreich!';
    var info_text = document.getElementById('info_text');
    info_text.innerHTML = 'Das Analysieren kann etwa 8 Sekunden pro Kommentar dauern. Bitte schau dir doch schonmal die fertigen Kommentare an. Schließe aber auf keinen Fall das Fenster. Öffne gerne folgende Seite in einem neuen Fenster, um alte, schon eingereichte Kommentare anzuschauen, dieser Prozess läuft im Hintergrund weiter: <a href="/html/show_comments.html" target="_blank">LINK</a>';
    var upload_form = document.getElementById('upload_form');
    upload_form.style.display = 'none';

    var div = document.getElementById('progress_div');
    var progressbar=document.createElement('progress');
    progressbar.max=100;
    progressbar.value=0;
    progressbar.id='progressbar_fileupload';
    div.appendChild(progressbar);
}

function output_kommentar(json_kommentar) {
    const itemsList = document.getElementById('items');

    var items = json_kommentar;

    var listItem = document.createElement('li');
    listItem.className = "comment_li";
    var details_in_li = document.createElement('details');
    var summary = document.createElement('summary');
    summary.innerHTML = items['dictionary']["keyWord"];
    var ul_in_details = document.createElement('ul');

    var kategorien = document.createElement('li');
    kategorien.innerHTML = '<b>Kategorien: </b>'+items['kategorien'][0]+', '+items['kategorien'][1];
    var zusammenfassung = document.createElement('li');
    zusammenfassung.innerHTML = '<b>Zusammenfassung: </b>'+items['dictionary']['Zusammenfassung'];
    var dringlichkeit = document.createElement('li');
    dringlichkeit.innerHTML = '<b>Dringlichkeit: </b>'+items['dictionary']['Dringlichkeit'];
    var datum = document.createElement('li');
    datum.innerHTML = '<b>Datum: </b>'+items['dictionary']['Datum'];
    var ganzer_comment = document.createElement('li');
    ganzer_comment.innerHTML = '<b>Ganzer Kommentar: </b>'+items['dictionary']['full_comment'];
    var order_id = document.createElement('li');
    order_id.innerHTML = '<b>order-id: </b>'+items['dictionary']['order_id'];
    var user_id = document.createElement('li');
    user_id.innerHTML = '<b>user-id: </b>'+items['dictionary']['user_id'];

    var time_info_element = document.getElementById('time_info_text');
    var time_text = 'Vermutlich Zeit bis zum Ende: ' + (Math.round(time_till_end/60)).toString() + ' Minuten. Zeit insgesamt: ' + (Math.round(time_insgesamt/60)).toString() + ' Minuten.';
    console.log(time_till_end);
    console.log(time_insgesamt);
    console.log((time_till_end | 0)/60);
    if (time_till_end != 0) {
        time_info_element.innerHTML = time_text;
    }

    ul_in_details.appendChild(kategorien);
    ul_in_details.appendChild(zusammenfassung);
    ul_in_details.appendChild(dringlichkeit);
    ul_in_details.appendChild(datum);
    ul_in_details.appendChild(ganzer_comment);
    ul_in_details.appendChild(order_id);
    ul_in_details.appendChild(user_id);

    details_in_li.appendChild(summary);
    details_in_li.appendChild(ul_in_details);
    listItem.appendChild(details_in_li);
    itemsList.appendChild(listItem);
}

function new_file_processed(aktuell, maximal) {
    if (aktuell != null) {
        var progressbar = document.getElementById('progressbar_fileupload');
        progressbar.max=maximal;
        progressbar.value = aktuell;
    }
}