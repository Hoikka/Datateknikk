
from flask import Flask, render_template


app = Flask(__name__)
@app.route('/')

def hello():
    hello = "Hello Flask!"
    return render_template('template.html', hello=hello)

if __name__ == "__main__":
    app.run(debug=True)
