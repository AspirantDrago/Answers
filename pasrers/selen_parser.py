from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.common.exceptions import NoSuchElementException, UnexpectedAlertPresentException
from collections import defaultdict
import requests

speciality = 'БТС'
kafedra_code = 109
test_name = 'Физика. Разделы "Механика и молекулярная физика"'

universitet = "Уфимский государственный нефтяной технический университет"
universitet_inner = 1
institute = "Вышка ИнСоТех"
institute_inner = 24
department = "Физики"
department_inner = 43
subject = "Физика"
subject_inner = 755
server = "http://127.0.0.1"

questions = list(range(1, 20 + 1))

LIMIT_FREE_INPUT = 10

def init():
    driver.get("https://testirov.rusoil.net/startrehearsal")
    input_spec = Select(driver.find_element_by_id('specy'))
    input_spec.select_by_value(speciality)
    input_kafedra = Select(driver.find_element_by_id('allkafedra'))
    input_kafedra.select_by_value(str(kafedra_code))
    wait.until(EC.element_located_selection_state_to_be((By.ID, 'discipline'), False))
    input_discipline = Select(driver.find_element_by_id('discipline'))
    input_discipline.select_by_visible_text(test_name)
    btn_go_test = driver.find_element_by_id('go_test')
    wait.until(EC.element_to_be_clickable((By.ID, 'go_test')))
    btn_go_test.click()
    wait.until(EC.element_located_selection_state_to_be((By.ID, 'click_answer'), False))
    for index in questions:
        ans_question(index)


def check_id(id_element):
    try:
        driver.find_element_by_id(id_element)
    except NoSuchElementException:
        return False
    return True


def ans_question(index):
    url = str(driver.current_url)
    url = '/'.join(url.split('/')[:-1] + [str(index)])
    driver.get(url)
    wait.until(EC.element_located_selection_state_to_be((By.ID, 'click_answer'), False))
    if check_question(index):
        print('   finded')
        return True
    btn_click_answer = driver.find_element_by_id("click_answer")
    btn_quest = driver.find_element_by_xpath(f"//div[@class='start_infohelp']/button[{index}]")
    btn_class = str(btn_quest.get_attribute('class'))
    if btn_class.endswith('RIGTH'):
        questions_good_ans[index] = questions_wait_ans[index]
        del questions_wait_ans[index]
        send_question(index)
        return True
    is_wrong = btn_class.endswith('WRONG')
    if is_wrong:
        questions_bad_ans[index].append(questions_wait_ans[index])
        del questions_wait_ans[index]
    if check_id("checkbox1"):
        if is_wrong:
            next_ans = 1 + max(questions_bad_ans[index])
            cnt = len(driver.find_elements_by_css_selector("input[type='checkbox']"))
            if (next_ans >= 2 ** cnt):
                return False
            i = 0
            questions_wait_ans[index] = next_ans
            driver.find_element_by_id("chancel_answer").click()
            while next_ans:
                i += 1
                is_check = next_ans % 2
                if is_check:
                    driver.find_element_by_id(f"checkbox{i}").click()
                next_ans //= 2
        else:
            driver.find_element_by_id("checkbox1").click()
            questions_wait_ans[index] = 1
    elif check_id("radio1"):
        if is_wrong:
            next_ans = 1 + max(questions_bad_ans[index])
            ans = driver.find_element_by_id(f"radio{next_ans}")
            questions_wait_ans[index] = next_ans
            ans.click()
        else:
            ans = driver.find_element_by_id("radio1")
            questions_wait_ans[index] = 1
            ans.click()
    else:
        if is_wrong:
            next_ans = 1 + max(questions_bad_ans[index])
            if next_ans > LIMIT_FREE_INPUT:
                print('   NOT FOUND!!!')
                return False
            inptext = driver.find_element_by_id("inptext")
            inptext.click()
            inptext.clear()
            inptext.send_keys(str(next_ans))
            questions_wait_ans[index] = next_ans
        else:
            driver.find_element_by_id("inptext").send_keys("0")
            questions_wait_ans[index] = 0
    wait.until(EC.element_to_be_clickable((By.ID, 'click_answer')))
    btn_click_answer.click()
    ans_question(index)


def check_question(index):
    inner_id = int(str(driver.find_element_by_css_selector('#testpage_Ajax > span:nth-child(1)').text).strip())
    data = {
        'universitet_id': universitet_inner,
        'institute_id': institute_inner,
        'departament_id': department_inner,
        'subject_id': subject_inner,
        'inner_id': inner_id
    }
    response = requests.post(server + '/api/check_question', data=data).json()
    return response.get('finded', '') == 'yes'


def send_question(index):
    try:
        driver.execute_script(js_update_images)
        alert = wait.until(EC.alert_is_present())
        alert.accept()
    except UnexpectedAlertPresentException:
        pass
    ordered = 0
    answers = []
    if check_id("checkbox1"):
        ztype = 2
        for element in driver.find_elements_by_css_selector("input[type=checkbox][checked] ~ label"):
            answers.append(element)
    elif check_id("radio1"):
        ztype = 1
        answers.append(driver.find_element_by_css_selector("input[type=radio][checked] ~ label"))
    else:
        ztype = 3
        answers.append(driver.find_element_by_id("inptext"))
    c = len(answers)
    inner_id = int(str(driver.find_element_by_css_selector('#testpage_Ajax > span:nth-child(1)').text).strip())
    text = upload_image(driver.find_element_by_css_selector("div.div_zadan"), 0)
    answers = list(map(lambda x: upload_image(x, ztype), answers))
    data = {
        'universitet': universitet,
        'institute': institute,
        'institute_inner': institute_inner,
        'department': department,
        'department_inner': department_inner,
        'subject': subject,
        'subject_inner': subject_inner,
        'ordered': ordered,
        'count': c,
        'type': ztype,
        'inner_id': inner_id,
        'text': text,
    }
    for i, answer in enumerate(answers):
        data[f'answer_{i}'] = answer
    response = requests.post(server + '/api/add_new_question', data=data).json()
    print(response)


def upload_image(element, ztype):
    imgs = element.find_elements_by_tag_name('img')
    if ztype == 3:
        text = str(element.get_attribute('value'))
    else:
        text = str(element.get_attribute('innerHTML'))
    for img in imgs:
        data = img.screenshot_as_base64
        response = requests.post(server + '/api/add_new_image_png', data={'data': data}).json()
        if (response.get('status', '') == 'ok'):
            text = text.replace(img.get_attribute('src'), '/' + response['path'])
        print('   upload_image', response)
    return text


with open('update_images.js', encoding='utf8') as f:
    js_update_images = f.read()
driver = webdriver.Firefox()
wait = WebDriverWait(driver, 10)
while True:
    questions_bad_ans = defaultdict(list)
    questions_good_ans = dict()
    questions_wait_ans = dict()
    try:
        init()
    except BaseException as e:
        print(e, type(e))
driver.close()
