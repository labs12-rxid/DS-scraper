from flask import Flask, request, render_template, jsonify
import atexit
from drugscom import drugscom
import json
from config import chromedriver_path, max_output_drugs

# print a nice greeting.
def say_hello(username = "World"):
    return '<p>Hello %s !</p>\n' % chromedriver_path
# some bits of text for the page.
header_text = '''
    <html>\n<head> <title>EB Flask Test</title> </head>\n<body>'''
instructions = '''
    <p><em>Hint</em>: This is a RESTful web service! Append a username
    to the URL (for example: <code>/Thelonious</code>) to say hello to
    someone specific.</p>\n'''
home_link = '<p><a href="/">Back</a></p>\n'
footer_text = '</body>\n</html>'

# EB looks for an 'application' callable by default.
application = Flask(__name__)


drugs_com = drugscom()

def close_drugs_com():
    print('started closing')
    if drugs_com != None:
        print('closing drugs_com')
        drugs_com.close()

atexit.register(close_drugs_com)

def get_drugscom(query_string):
    out_put = ''
    try:
        out_put = drugs_com.get_data(query_string)
    except Exception as e:
        out_put = f'error: {e}'
    finally:
        if drugs_com is not None: 
            drugs_com.reset()
    return out_put

@application.route('/identify', methods=['GET', 'POST'])
def identify():
    if request.method == 'POST':
        post_params = request.get_json(force=True)
        results = get_drugscom(post_params)
        return results
    else:
        return jsonify("GET request to /identify :")        


# add a rule for the index page.
application.add_url_rule('/', 'index', (lambda: header_text +
    say_hello() + instructions + footer_text))   

# add a rule when the page is accessed with a name appended to the site
# URL.
application.add_url_rule('/user/<username>', 'hello', (lambda username:
    header_text + say_hello(username) + home_link + footer_text))

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()
    