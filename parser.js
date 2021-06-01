universitet = "Уфимский государственный нефтяной технический университет"
universitet_inner = 1
institute = "СТФЛ"
institute_inner = 13
// subject = "Машины и аппараты химических производств"

server = "http://127.0.0.1"


function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function upload_image(text_in) {
    try {
        text = $(`<div>${text_in}</div>`);
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

async function main() {
    department = $('#bzkodkaf')[0].options[$('#bzkodkaf')[0].selectedIndex].text;
    department_inner = $('#bzkodkaf')[0].value;
    subject_inner = $('#bzekzamen')[0].value;
    subject = '' + subject_inner;
    $.ajax({
        type: "DELETE",
        url: `${server}/univer/${universitet_inner}/inst/${institute_inner}/dep/${department_inner}/sub/${subject_inner}`,
        async: false
    });
    l = $("ul").length;
    for (i = 0; i < l; i++) {

        var h = $("span:contains(Номер:##)").eq(i).text().length;
        var c = parseInt($("span:contains(Номер:##)").eq(i).text()[h - 2]);
        var ordered = parseInt($("span:contains(Номер:##)").eq(i).text()[h - 4]);
        var ztype = parseInt($("span:contains(Номер:##)").eq(i).text()[h - 6]);
        var inner_id = $(`ul:eq(${i})`)[0].id.substr(16);
        var text = $('#bz_zadantext' + inner_id)[0].innerHTML;
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
            try {
                data['answer_' + j] = upload_image($(`ul:eq(${i}) li`)[j].innerHTML);
            } catch (e) {
                c = j;
                break;
            }
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
        await sleep(20);
    }
}

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
        if (li) {
            alert('Изображения обновлены! Страница готова к сохранению.');
        }
        main();
    }
})
for (i = 0; i < li; i++) {
    $("img").eq(i).attr("name", "img_" + i);
    document.images["img_" + i].src = document.images["img_" + i].src;
}
// main();