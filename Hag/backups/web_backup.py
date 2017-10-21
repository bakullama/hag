from flask import Flask, request
import requests
import hag_get as h
app = Flask(__name__)
def slotchck(slot):
        resp=requests.get('http://127.0.0.1:4000/fake-jenkins-status/'+slot)
        return resp.text

bootstrap = '<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print dict(request.form)
    table_data=[]
    for slot in h.slots:
        chck=slotchck(slot)
        table_data.append({'box': slot,'break':'|', 'status': chck})
        link=make_link('http://127.0.0.1:4000/fake-jenkins-status/'+slot)

    title = make_title('Fake-Jenkins')
    table=make_table(table_data)
    return '{bootstrap}{title}{table}{link}{form}'.format(
        bootstrap=bootstrap,
        title=title,
        table=table,
        link=link,
        form=make_form(),
    )

def make_form():
    return '''
    <form method="POST">
        <input name="slot" value="testaut-1-stb-1" type="hidden"></input>
        <button>GO</button>
    </form>'''

def make_title(title):
    html = '''
    <title>{title}</title>
    '''
    return html.format(title=title)

def make_row(data):
    html = '''
    <tr>
        <td><b>{box}</b></td>
        <td>{break}</td>
        <td>{status}</td>
    </tr>
    '''
    return html.format(**data)

def make_table(datas):
    rows = [make_row(data) for data in datas]
    rows = '\n'.join(rows)
    return '''
    <div class="row">
        <div class="col-md-8">
            <table class="table">
                {}
            </table>
        </div>
    </div>
    '''.format(rows)

def make_link(url):
    html = '''
    <a href={link}>{link}</a>
    '''
    return html.format(link=url)

def make_table_header(header):
    return True

if __name__ == '__main__':
    app.run(port=1337, debug=True)
