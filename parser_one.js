universitet = "Уфимский государственный нефтяной технический университет"
universitet_inner = 1
institute = "ТФ"
institute_inner = 3
department = "НХТ"
department_inner = 61
subject = "Теория химико-технологических процессов органического и нефтехимического синтеза"
subject_inner = 27200
server = "http://127.0.0.1"


function upload_image(text_in) {
    try {
        text = $(`<p>${text_in}</p>`);
        var imgs = text.find('img');
        var imgs_size = imgs.size();
        for (j = 0; j < imgs_size; j++) {
            var img = imgs[j];
            var canvas = document.createElement("canvas");
            canvas.width = img.naturalWidth;
            canvas.height = img.naturalHeight;
            var context = canvas.getContext('2d');
            context.drawImage(img, 0, 0);
            var data = canvas.toDataURL("image/png");
            $.ajax({
                type: "POST",
                url: server + '/api/add_new_image_png',
                async: false,
                data: {data: data}
            }).done(function (data) {
                if (data.status == 'ok') {
                    img.src = '/' + data.path;
                }
            });
        }
        return text.html();
    } catch (e) {
        console.log(`ERROR "${text_in}"`);
        return text_in;
    }
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
        main();
    }
})
for (i = 0; i < li; i++) {
    $("img").eq(i).attr("name", "img_" + i);
    document.images["img_" + i].src = document.images["img_" + i].src;
}


function main() {
    ordered = 0;
    // TODO: необходимость выбора правильных ответов в строгой последовательности
    c = 1;
    ztype = undefined;
    answers = [];
    if (Boolean($("#checkbox1").length)) {
        ztype = 2;
        c = $("input[type=checkbox][checked]").length;
        for (var j = 0; j < c; j++) {
            answers.push($("input[type=checkbox][checked] ~ label")[j].innerHTML);
        }
    } else if (false) { // TODO: открытые задания

    } else {
        ztype = 1;
        answers.push($("input[type=radio][checked] ~ label")[0].innerHTML);
    }

    inner_id = parseInt($('#testpage_Ajax > span:nth-child(1)').text());
    text = $("div.div_zadan")[0].innerHTML;
    text = upload_image(text);

    data = {
        universitet: universitet,
        institute: institute,
        institute_inner: institute_inner,
        department: department,
        department_inner: department_inner,
        subject: subject,
        subject_inner: subject_inner,
        ordered: ordered,
        count: c,
        type: ztype,
        inner_id: inner_id,
        text: text,
    }

    for (var j = 0; j < c; j++) {
        data['answer_' + j] = upload_image(answers[j]);
    }

    $.post(server + '/api/add_new_question', data).done(
        function (response) {
            console.log(response);
        }
    ).fail(
        function (response) {
            console.log(response);
        }
    );
}
