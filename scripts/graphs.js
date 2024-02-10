function statistik_test() {
     fetch('/graph/per_time_categories_percent')
        .then(response => response.text())
        .then(imageString => {
            console.log(imageString);
            var div = document.getElementById('graph_div');
            var imgElement = document.createElement('img');
            imgElement.src = 'data:image/png;base64,' + imageString;
            document.body.appendChild(imgElement);
     });
}

function set_ui_first_category() {
    var cat_select_div = document.getElementById('categorie_select');
    cat_select_div.innerHTML = '';

    const graph_list = document.getElementById('graph_list');

    var div = document.getElementById('categories2');
    div.innerHTML = '';
    div = document.getElementById('categories1');
    div.innerHTML = '';
    var categorie_list = ['Anzahl und Verteilung', 'Freundlichkeit', 'Sonstige'];
    for (const cat of categorie_list) {
        var button = document.createElement('button');
        button.innerHTML = cat;
        button.addEventListener('click', function(event) {
            set_ui_second_category(cat);
        });
        div.appendChild(button);
    }
}


function set_ui_second_category(first_category) {
    var cat_select_div = document.getElementById('categorie_select');
    cat_select_div.innerHTML = '';

    const graph_list = document.getElementById('graph_list');

    var div = document.getElementById('categories2');
    div.innerHTML = '';

    var category_list = {'Anzahl und Verteilung' : ['Rezensionen pro Kategorie (insgesamt)', 'Rezensionen pro Kategorie (in Prozent)', 'generelle Rezensionen', 'Kommentare pro Kategorie (in Prozent)', 'Kommentare pro ausgewählter Kategorie (in Prozent)'],
                          'Freundlichkeit' : ['Freundlichkeit pro Tag (insgesamt)', 'Freundlichkeit pro Tag (pro Kategorie)', 'Freundlichkeit (insgesamt)'],
                          'Sonstige' : []};
    for (const i of category_list[first_category]) {
        var button = document.createElement('button');
        button.innerHTML = i;
        button.addEventListener('click', function(event) {2
            categories_set(first_category, i);
        });
        div.appendChild(button);
    }
}

function categories_set(first_category, second_category) {
    var mehr_spezifizierung_notwendig = [['Anzahl und Verteilung', 'Rezensionen pro Kategorie (insgesamt)'],
                                        ['Anzahl und Verteilung', 'Rezensionen pro Kategorie (in Prozent)'],
                                        ['Anzahl und Verteilung', 'Kommentare pro ausgewählter Kategorie (in Prozent)'],
                                        ['Freundlichkeit', 'Freundlichkeit pro Tag (pro Kategorie)']];

    var string_to_path = {[JSON.stringify(['Anzahl und Verteilung', 'generelle Rezensionen'])] : 'per_time_all',
                          [JSON.stringify(['Anzahl und Verteilung', 'Rezensionen pro Kategorie (insgesamt)'])] : 'per_time_categories_total',
                          [JSON.stringify(['Anzahl und Verteilung', 'Rezensionen pro Kategorie (in Prozent)'])] : 'per_time_categories_percent',
                          [JSON.stringify(['Anzahl und Verteilung', 'Kommentare pro Kategorie (in Prozent)'])] : 'per_category_piechart',
                          [JSON.stringify(['Anzahl und Verteilung', 'Kommentare pro ausgewählter Kategorie (in Prozent)'])] : 'per_choosed_category_piechart',
                          [JSON.stringify(['Freundlichkeit', 'Freundlichkeit pro Tag (insgesamt)'])] : 'anger_score_per_time',
                          [JSON.stringify(['Freundlichkeit', 'Freundlichkeit pro Tag (pro Kategorie)'])] : 'anger_score_per_time_per_choosed_category',
                          [JSON.stringify(['Freundlichkeit', 'Freundlichkeit (insgesamt)'])] : 'anger_score_piechart'};

    var isContained = _.some(mehr_spezifizierung_notwendig, function(innerArray) {
      return _.isEqual(innerArray, [first_category, second_category]);
    });


    if (isContained != true) {
        var graph_path = string_to_path[[JSON.stringify([first_category, second_category])]]
        fetch('/graph/'+graph_path + '/["im_empty"]')
        .then(response => response.text())
        .then(imageString => {
            var list = document.getElementById('graph_list');
            var list_element = document.createElement('li');
            var imgElement = document.createElement('img');
            var delete_button = document.createElement('button');
            delete_button.classList.add('deleteButton');
            delete_button.innerHTML = 'X';
            delete_button.addEventListener('click', deleteListItem);

            imgElement.src = 'data:image/png;base64,' + imageString;
            list_element.appendChild(imgElement);
            list_element.appendChild(delete_button);
            list.appendChild(list_element);
     });
    } else {
        create_categorie_select(first_category, second_category, string_to_path)
    }
}

function create_categorie_select(first_category, second_category, string_to_path) {
    var categories_all = [
      {'value': ['Fehlerbericht', 'insgesamt'], 'label': 'Fehlerbericht (alle)'},
      {'value': ['Fehlerbericht', 'Softwarebug'], 'label': 'Fehlerbericht/Softwarebug'},
      {'value': ['Fehlerbericht', 'Druckfehler'], 'label': 'Fehlerbericht/Druckfehler'},
      {'value': ['Fehlerbericht', 'Logistikproblem'], 'label': 'Fehlerbericht/Logistikproblem'},
      {'value': ['Fehlerbericht', 'Sonstiges'], 'label': 'Fehlerbericht/Sonstiges'},
      {'value': ['Kritik', 'insgesamt'], 'label': 'Kritik (alle)'},
      {'value': ['Kritik', 'Vielfalt'], 'label': 'Kritik/Vielfalt'},
      {'value': ['Kritik', 'Qualitaet'], 'label': 'Kritik/Qualitaet'},
      {'value': ['Kritik', 'Benutzerfreundlichkeit'], 'label': 'Kritik/Benutzerfreundlichkeit'},
      {'value': ['Kritik', 'Service'], 'label': 'Kritik/Service'},
      {'value': ['Kritik', 'Preis'], 'label': 'Kritik/Preis'},
      {'value': ['Kritik', 'Sonstiges'], 'label': 'Kritik/Sonstiges'},
      {'value': ['Lob', 'insgesamt'], 'label': 'Lob (alle)'},
      {'value': ['Lob', 'Vielfalt'], 'label': 'Lob/Vielfalt'},
      {'value': ['Lob', 'Qualitaet'], 'label': 'Lob/Qualitaet'},
      {'value': ['Lob', 'Benutzerfreundlichkeit'], 'label': 'Lob/Benutzerfreundlichkeit'},
      {'value': ['Lob', 'Service'], 'label': 'Lob/Service'},
      {'value': ['Lob', 'Preis'], 'label': 'Lob/Preis'},
      {'value': ['Lob', 'Sonstiges'], 'label': 'Lob/Sonstiges'},
      {'value': ['Sonstiges', 'Sonstiges'], 'label': 'Sonstiges/Sonstiges'}
    ];


    var cat_select_div = document.getElementById('categorie_select');
    cat_select_div.innerHTML = '';

    var selectElement = document.createElement('select');
    selectElement.id = 'multiselect_categories';
    selectElement.multiple = true;
    selectElement.size = '10';

    for (const category of categories_all) {
      var optionElement = document.createElement('option');
      optionElement.value = JSON.stringify(category['value']);
      optionElement.text = category['label'];
      selectElement.appendChild(optionElement);
    }

    var submit_button = document.createElement('button');
    submit_button.textContent = 'Submit';
    submit_button.addEventListener('click', function(event){
        categories_submitted(first_category, second_category, string_to_path);
    });

    cat_select_div.appendChild(selectElement);
    cat_select_div.appendChild(submit_button);

    cat_select_div.style.display = "block";
}

function categories_submitted(first_category, second_category, string_to_path) {
    var selectElement = document.getElementById('multiselect_categories');
    var selectedOptions = [];

    for (var i = 0; i < selectElement.options.length; i++) {
        var option = selectElement.options[i];

        if (option.selected) {
          selectedOptions.push(JSON.parse(option.value));
        }
    }

    console.log(selectedOptions);
    console.log(JSON.stringify(selectedOptions));

    var graph_path = string_to_path[[JSON.stringify([first_category, second_category])]];
    fetch('/graph/'+graph_path + '/' + JSON.stringify(selectedOptions))
        .then(response => response.text())
        .then(imageString => {
            var list = document.getElementById('graph_list');
            var list_element = document.createElement('li');
            var imgElement = document.createElement('img');
            var delete_button = document.createElement('button');
            delete_button.classList.add('deleteButton');
            delete_button.innerHTML = 'X';
            delete_button.addEventListener('click', deleteListItem);

            imgElement.src = 'data:image/png;base64,' + imageString;
            list_element.appendChild(imgElement);
            list_element.appendChild(delete_button);
            list.appendChild(list_element);
     });
}

function deleteListItem() {
    var listItem = this.parentNode;
    listItem.parentNode.removeChild(listItem);
}