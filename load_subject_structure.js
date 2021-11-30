var kodkaf = 61;
var ekzamen = 37328;


function query(url, data) {
    data.kodkaf = kodkaf;
    data.ekzamen = ekzamen;
    var respText = $.ajax({
        type: 'POST',
        url: url,
        data: data,
        dataType: 'json',
        async: false
    }).responseText;
    return JSON.parse(respText);
}

function getRangs() {
    return query('https://testirov.rusoil.net/req_autocompletezadan',
        {'fid': 'rang'})['data'][0];
}

function getRazdels(rang) {
    return query('https://testirov.rusoil.net/req_autocompletezadan',
        {'fid': 'razdel', 'rang': rang})['data'][0];
}

function getTems(rang, razdel) {
    return query('https://testirov.rusoil.net/req_autocompletezadan',
        {'fid': 'tema', 'rang': rang, 'razdel': razdel})['data'][0];
}

function getCount(rang, razdel, tema) {
    return parseInt(query('https://testirov.rusoil.net/req_questioncountzadan',
        {'rang': rang, 'razdel': razdel, 'tema': tema})['data']);
}


var s = '';
var allCount = 0;
var rangs = getRangs();
rangs.forEach(function (rang) {
    s += `ранг ${rang}\n`;
    var razdels = getRazdels(rang);
    razdels.forEach(function (razdel) {
        s += `    раздел ${razdel}\n`;
        var tems = getTems(rang, razdel);
        tems.forEach(function (tema) {
            var count = getCount(rang, razdel, tema);
            s += `        тема ${tema}            ${count}\n`;
            allCount += count;
        });
    });
    console.log(s);
});
console.log(allCount);
