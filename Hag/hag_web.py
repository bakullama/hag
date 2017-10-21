from flask import Flask, request
import requests
import time
from colorama import init,Fore,Back,Style
import hag_get as h
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


init()

app = Flask(__name__)

bootstrap = '<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">'

state={
    'testaut-1-stb-1':[],
    'testaut-1-stb-2':[],
    'testaut-1-stb-3':[],
    'testaut-1-stb-4':[]
    }

checked={
    'testaut-1-stb-1':False,
    'testaut-1-stb-2':False,
    'testaut-1-stb-3':False,
    'testaut-1-stb-4':False,}

def slotchck(slot):
        response=requests.get('http://127.0.0.1:4000/fake-jenkins-status/'+slot)
        return response.text

def start(slot):
    requests.get('http://127.0.0.1:4000/fake-jenkins-do-something/START/'+slot)
    state[slot].append(slotchck(slot))

def input_check():
    if request.method=='POST':
        box_checked=dict(request.form).get('auto-restart',[])
        go_slots = dict(request.form)['slot']

        for slot in checked:
            is_checked = slot in box_checked
            checked[slot] = is_checked

        for slot in go_slots:
            if slot:
                start(slot)

    for slot in checked:
        if state[slot]:
            state[slot][-1]=slotchck(slot)

    for slot in checked:
        if checked[slot]:
            if slotchck(slot) in ['unknown', 'FAILURE']:
                start(slot)

def render():

    input_check()

    table_data=[]
    table_data.append({'box': 'BOX','button':'','checkbox':'AUTO','statii':[]})

    title = make_title('Fake Jenkins')

    for slot in h.slots:
        table_data.append({'box': slot,'button':make_button(slot),'checkbox':make_checkbox(slot,bool(checked[slot])),'statii':state[slot]})

    for slot in h.slots:
        table=make_table(table_data)
    return '<meta http-equiv="refresh" content="5"><image src="https://xebialabs.com/assets/files/plugins/jenkins.jpg"  style="width:340px;height:228px;" alt="There was meant to be a cool image here, but it didn\'t work">{bootstrap}{title}<form method="POST" id="run-form">{table}</form>'.format(
        bootstrap=bootstrap,
        title=title,
        table=table,
    )

def slotchck(slot):
        response=requests.get('http://127.0.0.1:4000/fake-jenkins-status/'+slot)
        return response.text

@app.route('/', methods=['GET', 'POST'])

def index():
    return render()

def make_checkbox(slot, checked):
    return'''
        <input name="auto-restart" value="{slot}" type="checkbox" {checked} onclick=document.getElementById("run-form").submit();></input>
    '''.format(slot=slot, checked='checked' if checked else '')

def make_button(slot):
    return '''
        <input align="center" id="{slot}-button" name="slot" value="" type="hidden" class="btn-primary"></input>
        <button onclick="document.getElementById('{slot}'+'-button').setAttribute('value', '{slot}')">GO</button>
    '''.format(slot=slot)

def make_title(title):
    html = '''
    <title>{title}</title>
    '''
    return html.format(title=title)

def make_statii_cells(statii):
    global slot
    return '\n'.join('<td align="center">{}</td>'.format(status) for status in statii)

def make_row(data):
    html = '''
    <tr>
        <td align="center" class="active"><b>{box}</b></td>
        <td align="center">{button}</td>
        <td align="center">{checkbox}</td>
        {statii_cells}
    </tr>
    '''
    return html.format(
        box=data['box'],
        button=data['button'],
        checkbox=data['checkbox'],
        statii_cells=make_statii_cells(data['statii']),
    )

def make_table(datas):
    rows = [make_row(data) for data in datas]
    rows = '\n'.join(rows)
    return '''
    <div class="row">
        <div class="col-md-5">
            <table class="table table-bordered">
                {}
            </table>
        </div>
    </div>
    '''.format(rows)

if __name__ == '__main__':
    app.run(port=1338, debug=True)
