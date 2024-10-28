from flask import Flask, render_template, jsonify, request, session
import requests
import random
import string


app = Flask(__name__)
app.secret_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(12))


# Fetch all quotes
quotes = requests.get("https://dummyjson.com/quotes").json()["quotes"]


@app.route('/')
def index():
    # load initially a random quote
    session["name"] = session.get("name", "Guest")
    quote = random.choice(quotes)
    return render_template(template_name_or_list="index.html", quote=quote, name=session["name"])


@app.route(rule='/login', methods=['POST'])
def login():
    # just set the user's name, we won't authenticate yet
    name = request.json.get("name", "Guest")
    session["name"] = name
    return jsonify({"name": name})


@app.route('/next')
def next_quote():
    """
    :return:

    tricky: the quotes are numbered 1..., the index starts with 0
            meaning the next_id=2 is actually the 3rd quote
    """
    current_id = request.args.get("id", default=0, type=int)
    next_id = current_id % len(quotes)
    print(current_id, next_id, quotes)
    return jsonify(quotes[next_id])


@app.route('/random')
def random_quote():
    # getanother random quote
    quote = random.choice(quotes)
    return jsonify(quote)


if __name__ == '__main__':
    app.run(debug=True)
