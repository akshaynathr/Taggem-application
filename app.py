import re
import string
from urlparse import urlparse

from flask import (
    Flask,Markup,
    render_template,
    jsonify,
    request
)

from extractor import extract

app = Flask(__name__)

style =" p { display:inline !important; }"
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/extract')
def extract_url():
    url = request.args.get('url', '')
    if not URL_REGEX.match(url):
        return jsonify({
            'type': 'error',
            'message': 'Invalid URL'
        }), 406
    myFile=open('news.html','w')
#    myFile.write(extract(url)['text'])
    myFile.close()
    html=extract(url)['html']
    print html
    type(html)
    #html.replace('Image caption','')
    value=Markup(html)
    parsed_uri=urlparse(url)
    domain='{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
#    return jsonify(type='success', message=extract(url))
    return render_template('news.html',message=extract(url),url=domain)
    return jsonify(type='success', message=value,style=style)

if __name__ == '__main__':
    app.run(debug=True, port=8000)
