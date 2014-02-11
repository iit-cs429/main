"""
A rudimentary web interface to the search engine, using Flask. You'll have to
install flask (if you have pip installed, you can do `pip install flask`; for
Windows, see
http://flask.pocoo.org/docs/installation/#pip-and-distribute-on-windows).

Run with `python run.py`. If successful, you should see a message like:
Running on http://127.0.0.1:5000/ . You can then view the page in your web
browser at the specified URL.

You should not need to modify this file.
"""
from flask import Flask
from flask import request

from searcher import Index

app = Flask(__name__)
my_index = Index('documents.txt')


def results2string(doc_ids):
    """ Return the top 100 search results as a string of <p> blocks, looking up each
    doc_id in the index. """
    res = ''
    for doc_id, score in doc_ids[:100]:
        res += "<p>%d: <b>%e</b> %s </p>" % (doc_id, score, my_index.documents[doc_id])
    return res


def form():
    """ Create a search form, optionally with the query box filled in."""
    query = request.form['query'] if request.form else ''
    champ = 'checked' if 'champion' in request.form else ''
    return '''
    <form action="/index" method="post">
      <input type="text" name="query" size="50" value="%s"/>
      <input type="checkbox" name="champion" value="champion" %s>use champion list<br>
      <input type="submit" value="search"/>
    </form>
   ''' % (query, champ)


@app.route('/')
@app.route('/index', methods=["POST"])
def index():
    """ Process search request and results. """
    result = "<html>\n<body>" + form()
    if request.method == 'POST':  # Respond to search request.
        champ = 'champion' in request.form
        print 'champ=', champ
        result += results2string(my_index.search(request.form['query'], champ))
    result += "<body></html>"
    return result


if __name__ == '__main__':
    app.run(debug=True)
