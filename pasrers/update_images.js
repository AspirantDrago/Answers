l = $("ul").length;
for (i = 0; i < l; i++) {
    var h = $("span:contains(Номер:##)").eq(i).text().length;
    var c = parseInt($("span:contains(Номер:##)").eq(i).text()[h - 2]) - 1;
    $("ul:eq(" + i + ") li:gt(" + c + ")").remove();
}
var li = $("img").length;
var ci = 0;
var ci_pr = 0;
$("img").error(function () {
    var ni = parseInt($(this).attr("name").substr(4));
    if (document.images["img_" + ni].naturalWidth == 0) {
        document.images["img_" + ni].src = document.images["img_" + ni].src;
    }
});

$("img").load(function () {
    ci++;
    var ci_pr_new = Math.floor(100 * ci / li);
    if (ci_pr_new !== ci_pr) {
        ci_pr = ci_pr_new;
        console.log('Загружено изображений: ' + ci_pr + ' %');
    }
    if (ci === li) {
        alert('Изображения обновлены! Страница готова к сохранению.');
    }
})
for (i = 0; i < li; i++) {
    $("img").eq(i).attr("name", "img_" + i);
    document.images["img_" + i].src = document.images["img_" + i].src;
}