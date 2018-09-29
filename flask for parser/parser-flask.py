from flask import Flask, render_template, request        # render - отоброжает шаблоны jinja 2
from avitoparser import main_parsing


app = Flask(__name__)


@app.route('/')
@app.route('/entry')
def entry_page():
    return render_template('entry.html')


@app.route('/results', methods = ['POST']) 
def do_search() -> str:
    city = request.form['city'].upper()
    phrase = request.form['phrase'].upper()
    main_parsing(city, phrase)
    return render_template('results.html',  the_phrase = phrase,
                                            the_city = city,)


@app.route('/viewresults')
def view_the_parse():
    contents = []
    with open('parser-data.log') as log:
        for line in log:
            contents.append([])
            for item in line.split('|'):
                contents[-1].append(item)
    titles = ('Заголовок', 'Цена', 'Время', 'Место', 'URL')
    return render_template('viewresults.html', the_row_titles = titles,
                                               the_data = contents,)


def log_request(req, res):
    with open('search.log', 'a') as log:
        print(req.form, req.remote_addr, req.user_agent, res, file=log, sep='|')


if __name__ == '__main__':
    app.run(debug=True)