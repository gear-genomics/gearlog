const API_URL = process.env.API_URL

var toolsel = document.getElementById('btn-key-list')
var spin1 = document.getElementById('spinner1')
var spin2 = document.getElementById('spinner2')

$('#mainTab a').on('click', function (e) {
  e.preventDefault()
  $(this).tab('show')
})

var spinnerHtml = '<i class="fa fa-spinner fa-pulse fa-3x fa-fw"></i>'
var sectionResults = document.getElementById('results')
var resHelp = -1;

document.addEventListener("DOMContentLoaded", function() {
    var today = new Date();
    var last = new Date();
    today.setDate(today.getDate()-1);
    last.setDate(today.getDate()-99);
    var endDate = document.getElementById('dateEnd');
    endDate.value = date2string(today);
    var startDate = document.getElementById('dateStart');
    startDate.value = date2string(last);

    var submitButton = document.getElementById('btn-submit');
    submitButton.addEventListener('click', submit);
    var selButton = document.getElementById('btn-key-list');
    selButton.addEventListener('click', submit);
    submit();
});

function date2string(date) {
    var dd = date.getDate();
    var mm = date.getMonth()+1; //January is 0!
    var yyyy = date.getFullYear();
    if (dd<10) {
        dd = '0' + dd;
    } 
    if(mm<10) {
        mm = '0' + mm;
    } 
    return yyyy + '-' + mm + '-' + dd;
}


function submit () {
    var primKey = document.getElementById('primKey').value;
    var dateStart = document.getElementById('dateStart').value;
    var dateEnd = document.getElementById('dateEnd').value;
    var data = new FormData();
    data.append('primKey', primKey);
    data.append('dateStart', dateStart);
    data.append('dateEnd', dateEnd);
    doSubmit (data);
}

function doSubmit (data) {
    var req = new XMLHttpRequest();
    req.addEventListener('load', displayResults);
    req.open('POST', `${API_URL}/upload`, true);
    req.send(data);
    spin1.innerHTML = spinnerHtml;
    spin2.innerHTML = spinnerHtml;
}

function displayResults() {
    spin1.innerHTML = "";
    spin2.innerHTML = "";
    if (this.status === 200) {
        displayData(this.response)
    } else {
        displayError(this.response)
    }
}

function displayData(data) {
    var res = JSON.parse(data);
    var pKey = res["data"]['primKeys'];
    var rhtml = "";
    for (var i = 0; i < pKey.length; i++) {
        rhtml += '<a class="dropdown-item" href="#" onclick="bgiUp(\'' + pKey[i] + '\')">' + pKey[i] + '</a>';
    }
    toolsel.innerHTML = rhtml;
    var tdata = res["data"]['counts'];
    var cols = tdata[0].length;
    rhtml = '<table style="width:100%">\n';
    for (var i = 0; i < tdata.length; i++) {
	rhtml += '  <tr>\n';
        for (var c = 0; c < cols; c++) {
            rhtml += '    <td>' + tdata[i][c] + '</td>\n';
	}
        rhtml += '  </tr>\n';
    }
    rhtml += '</table>\n';
    document.getElementById('usage').innerHTML = rhtml;
    var cdata = res["data"]['countries'];
    rhtml = '<table style="width:100%">\n';
    for (var i = 0; i < cdata.length; i++) {
        rhtml += '  <tr>\n';
        rhtml += '    <td>' + cdata[i][0] + '</td>\n';
        rhtml += '    <td>' + cdata[i][1] + '</td>\n';
        rhtml += '  </tr>\n';
    }
    rhtml += '</table>\n';
    document.getElementById('country').innerHTML = rhtml;

}

function displayError(data) {
    var res = JSON.parse(data)
    for (var i = 0; i < res["errors"].length; i++) {
	document.getElementById('usage').innerHTML = '<br /><div class="error">' + res["errors"][i]['title'] + '</div><br />'
    }
}

window.bgiUp = bgiUp;
function bgiUp(tKey) {
    document.getElementById('primKey').value = tKey;
    document.getElementById('btn-primKey').innerHTML = tKey;
}


