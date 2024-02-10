// Pfad zur JSON-Datei
const jsonFilePath = '/logic/data/data_file.json';

var filter1 = '';
var filter2 = '';

create_filter_and_sort_ui();
var filters_div = document.getElementById("filters_and_sorts");
filters_div.style.display = "none";

var insgesamte_kommentare = 0;
var bearbeitete_kommentare = 0;

// JSON-Daten laden und parsen
function set_ui_first_category() {
    var info_text = document.getElementById('info_text');
    info_text.innerHTML = '';
    var filters_div = document.getElementById("filters_and_sorts");
    filters_div.style.display = "none";
    fetch(jsonFilePath)
        .then(response => response.json())
        .then(data => {
            const itemsList = document.getElementById('items');
            itemsList.innerHTML = '';
            var filter_start_button = document.getElementById('filter_start_button')
            filter_start_button.innerHTML = 'Setze neue Filter'
            var div = document.getElementById('categories2');
            div.innerHTML = '';
            div = document.getElementById('categories1');
            div.innerHTML = '';
            for (const key in data) {
                var button = document.createElement('button');
                button.innerHTML = key;
                button.addEventListener('click', function(event) {2
                    set_ui_second_category(key);
                });
                div.appendChild(button);
            }
        });
}


// Elemente nach Kategorie filtern und anzeigen
function set_ui_second_category(category1) {
    var info_text = document.getElementById('info_text');
    info_text.innerHTML = '';
    var filters_div = document.getElementById("filters_and_sorts");
    filters_div.style.display = "none";

    fetch(jsonFilePath)
        .then(response => response.json())
        .then(data => {
            const itemsList = document.getElementById('items');
            itemsList.innerHTML = '';
            var filtered_data = data[category1];
            var div = document.getElementById('categories2');
            div.innerHTML = '';
            for (const key in filtered_data) {
                var button = document.createElement('button');
                button.innerHTML = key;
                button.addEventListener('click', function(event) {
                    filter_items_by_categories(category1, key);
                });
                div.appendChild(button);
            }
        });
}

function create_filter_and_sort_ui() {
    var div = document.getElementById('filters_and_sorts');
    div.innerHTML='';


    var label = document.createElement('label');
    label.htmlFor = 'checkbox_show_bearbeitet'

    var checkbox1 = document.createElement('input');
    checkbox1.type='checkbox';
    checkbox1.id =  'checkbox_show_bearbeitet';


    label.appendChild(checkbox1);
    var labelText = document.createTextNode('zeige auch bearbeitete Rezensionen');
    label.appendChild(labelText);
    div.appendChild(label);

    var neue_zeile = document.createElement('p');
    div.appendChild(neue_zeile);



    var label = document.createElement('label');
    label.htmlFor = 'checkbox_sort_date'

    var checkbox2 = document.createElement('input');
    checkbox2.type='checkbox';
    checkbox2.id =  'checkbox_sort_date';

    label.appendChild(checkbox2);
    var labelText = document.createTextNode('Sortiere nach Datum (neueste zuerst)');
    label.appendChild(labelText);
    div.appendChild(label);

    var neue_zeile = document.createElement('p');
    div.appendChild(neue_zeile);



    var label = document.createElement('label');
    label.htmlFor = 'checkbox_sort_bewertung';

    var checkbox3 = document.createElement('input');
    checkbox3.type='checkbox';
    checkbox3.id =  'checkbox_sort_bewertung';

    label.appendChild(checkbox3);
    var labelText = document.createTextNode('Sortiere nach der relevanz (wichtigste zuerst)');
    label.appendChild(labelText);
    div.appendChild(label);

    var neue_zeile = document.createElement('p');
    div.appendChild(neue_zeile);

    var filter_bearbeitet = document.getElementById('checkbox_show_bearbeitet');
    var sort_date = document.getElementById('checkbox_sort_date');
    var sort_relevanz = document.getElementById('checkbox_sort_bewertung');

    filter_bearbeitet.addEventListener('change', function() {
      filter_checkbox_changed('checkbox_show_bearbeitet');
    });

    sort_date.addEventListener('change', function() {
      filter_checkbox_changed('checkbox_sort_date');
    });

    sort_relevanz.addEventListener('change', function() {
      filter_checkbox_changed('checkbox_sort_bewertung');
    });

    random_button = document.createElement('button');
    random_button.innerHTML = 'random';
    random_button.addEventListener('click', function() {
      random_sort();
    });
    div.appendChild(random_button);
}



// Elemente nach Kategorie filtern und anzeigen
function filter_items_by_categories(category1, category2, random=false) {
  filter1 = category1;
  filter2 = category2;
  var filters_div = document.getElementById("filters_and_sorts");
  filters_div.style.display = "block";

  var filter_bearbeitet = document.getElementById('checkbox_show_bearbeitet');
  var sort_date = document.getElementById('checkbox_sort_date');
  var sort_relevanz = document.getElementById('checkbox_sort_bewertung');

  fetch(jsonFilePath)
    .then(response => response.json())
    .then(data => {
        var filteredItems = data[category1][category2];
        var sorted_key_list = [];

        insgesamte_kommentare = Object.keys(filteredItems).length;
        bearbeitete_kommentare = 0;

        for (const key in filteredItems) {
            if (filteredItems[key]['bearbeitet'] == true) {
                bearbeitete_kommentare += 1;
                if (filter_bearbeitet.checked == false) {
                    delete filteredItems[key];
                }
            }
        }


      for (const key in filteredItems) {
        sorted_key_list.push(key);
      }


      if (sort_date.checked == true) {
        var list_to_sort = [];
        for (const key in filteredItems) {
            var days = 0;
            var splited_date = filteredItems[key]['Datum'].split('-');
            days += splited_date[0]*365
            days += splited_date[1]*30
            days += splited_date[2]
            list_to_sort.push([days, key]);
        }

        list_to_sort.sort(function(a, b) {
          return b[0] - a[0];
        });

        sorted_key_list = [];
        for (index in list_to_sort) {
            sorted_key_list.push(list_to_sort[index][1]);
        }
      }


      if (sort_relevanz.checked == true) {
        var list_to_sort = [];
        for (const key in filteredItems) {
            list_to_sort.push([filteredItems[key]['Dringlichkeit'], key]);
        }

        list_to_sort.sort(function(a, b) {
          return b[0] - a[0];
        });

        sorted_key_list = [];
        for (index in list_to_sort) {
            sorted_key_list.push(list_to_sort[index][1]);
        }
      }

      if (random){
        sorted_key_list = shuffleList(sorted_key_list);
        sort_date.checked = false;
        sort_relevanz.checked = false;
      }


      showItems(filteredItems,sorted_key_list);
    });
}



// Elemente in der Liste anzeigen
function showItems(items, sorted_keys) {
  const itemsList = document.getElementById('items');
  itemsList.innerHTML = '';
  for (const key of sorted_keys) {
    var listItem = document.createElement('li');
    listItem.className = "comment_li";
    var details_in_li = document.createElement('details');
    var summary = document.createElement('summary');
    summary.innerHTML = items[key]["keyWord"];
    var ul_in_details = document.createElement('ul');

    var zusammenfassung = document.createElement('li');
    zusammenfassung.innerHTML = '<b>Zusammenfassung: </b>'+items[key]['Zusammenfassung'];
    var dringlichkeit = document.createElement('li');
    dringlichkeit.innerHTML = '<b>Dringlichkeit: </b>'+items[key]['Dringlichkeit'];
    var datum = document.createElement('li');
    datum.innerHTML = '<b>Datum: </b>'+items[key]['Datum'];
    var ganzer_comment = document.createElement('li');
    ganzer_comment.innerHTML = '<b>Ganzer Kommentar: </b>'+items[key]['full_comment'];
    var order_id = document.createElement('li');
    order_id.innerHTML = '<b>order-id: </b>'+items[key]['order_id'];
    var user_id = document.createElement('li');
    user_id.innerHTML = '<b>user-id: </b>'+items[key]['user_id'];

    var bearbeitet_button = document.createElement("button");
    if (items[key]['bearbeitet'] == true) {
        bearbeitet_button.innerHTML = 'nichtmehr bearbeitet';
        bearbeitet_button.addEventListener('click', function() {
          var json_key = key;
          bearbeitet_button_clicked(json_key, typ=false);
        });

    }else {
        bearbeitet_button.innerHTML = 'bearbeitet';
        bearbeitet_button.addEventListener('click', function() {
          var json_key = key;
          bearbeitet_button_clicked(json_key);
        });
    }

    var info_text = document.getElementById('info_text');
    info_text.innerHTML = 'Es gibt insgesamt <b>' + insgesamte_kommentare.toString() + '</b> Kommentare. Davon sind schon <b>' + bearbeitete_kommentare.toString() + '</b> bearbeitet und werden dir ggf. nicht angezeigt.'



    ul_in_details.appendChild(zusammenfassung);
    ul_in_details.appendChild(dringlichkeit);
    ul_in_details.appendChild(datum);
    ul_in_details.appendChild(ganzer_comment);
    ul_in_details.appendChild(order_id);
    ul_in_details.appendChild(user_id);
    ul_in_details.appendChild(bearbeitet_button);

    details_in_li.appendChild(summary);
    details_in_li.appendChild(ul_in_details);
    listItem.appendChild(details_in_li)
    itemsList.appendChild(listItem);
  };
}

function bearbeitet_button_clicked(json_key, typ = true) {
    fetch(jsonFilePath)
    .then(response => response.json())
    .then(data => {
      data[filter1][filter2][json_key]['bearbeitet'] = typ;
      var modifiedJson = JSON.stringify(data);

      return fetch('/upload/json', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: modifiedJson
      });
    })

    .then(uploadResponse => {
      if (uploadResponse.ok) {
        filter_items_by_categories(filter1, filter2);
      } else {
        throw new Error('Fehler beim Hochladen des JSON');
      }
    })

}

function filter_checkbox_changed (checkbox_id) {
    console.log(checkbox_id);
    var sort_date = document.getElementById('checkbox_sort_date');
    var sort_relevanz = document.getElementById('checkbox_sort_bewertung');
    if (checkbox_id == 'checkbox_sort_date') {
        if (sort_date.checked == true) {
            sort_relevanz.checked = false;
        }
    }else if (checkbox_id == 'checkbox_sort_bewertung') {
        if (sort_relevanz.checked == true) {
            sort_date.checked = false;
        }
    }
    filter_items_by_categories(filter1, filter2);
}

function random_sort() {
    filter_items_by_categories(filter1, filter2, random=true);
}

function shuffleList(list) {
  for (let i = list.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [list[i], list[j]] = [list[j], list[i]];
  }

  return list;
}