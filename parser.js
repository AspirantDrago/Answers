universitet = "Уфимский государственный нефтяной технический университет"
institute = "СТФЛ"
institute_inner = 13
subject = "Что-то"

server = "http://127.0.0.1/api/add_new_question"


function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}


async function main() {
  department = $('#bzkodkaf')[0].options[$('#bzkodkaf')[0].selectedIndex].text;
  department_inner = $('#bzkodkaf')[0].value;
  subject_inner = $('#bzekzamen')[0].value;
  l = $("ul").length;
  for(i = 0; i < l; i++){
    
    var h = $("span:contains(Номер:##)").eq(i).text().length;
    var c = parseInt($("span:contains(Номер:##)").eq(i).text()[h - 2]);
    var ordered = parseInt($("span:contains(Номер:##)").eq(i).text()[h - 4]);
    var ztype = parseInt($("span:contains(Номер:##)").eq(i).text()[h - 6]);
    var inner_id = $(`ul:eq(${i})`)[0].id.substr(16);
    var text = $('#bz_zadantext' + inner_id)[0].innerHTML;
    $(`ul:eq(${i}) li:gt(${c - 1})`).remove();
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
    };
    
    
    for (var j = 0; j < c; j++) {
      data['answer_' + j] = $(`ul:eq(${i}) li`)[j].innerHTML;
    }
    
    $.post(server, data).done(
      function(response) { console.log(response);}
    ).fail(
      function(response) { console.log(response);}
    );
    await sleep(100);
  };
}

main();
