"""
Final Project Starter Template - Flask + API + Data Integration
================================================================

Guys, this example is simple, I didn't want to force you guys to apply for API keys,
it uses the Open Library Search API (free, no API key, returns JSON):
    https://openlibrary.org/dev/docs/api/search

HOW TO ADAPT IT TO YOUR OWN PROJECT FOR THIS CLASS:
-----------------------------------
1. Pick your API and change API_URL below.
2. Change the fields in SearchForm (keep at least THREE).
3. Change build_params() so the form values become your API's parameters.
4. Change process_data() to parse/filter/transform YOUR API's JSON (or XML).
5. Change the table columns in templates/results.html.
Again, you do not need to follow this template, you can use any API you want and you can structure it differently.
Run it:
    pip install -r requirements.txt
    python app.py
Then open http://127.0.0.1:5000
"""

import requests
from flask import Flask, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Optional


# Very likely you will need the same set of imports as above
app = Flask(__name__)
app.config["SECRET_KEY"] = "change-this-secret-key"  # needed by Flask-WTF for CSRF protection

# TODO (Step 1): change to your API's endpoint
API_URL = "https://openlibrary.org/search.json"


# ---------------------------------------------------------------------------
# 1) THE FORM  (requirement: at least three fields)
# ---------------------------------------------------------------------------
class SearchForm(FlaskForm):
    # TODO (Step 2): replace these with fields that make sense for your API
    query = StringField("Search term (title, author, topic)", validators=[DataRequired()])
    max_results = IntegerField("How many results?", default=10,
                               validators=[DataRequired(), NumberRange(min=1, max=50)])
    min_year = IntegerField("Published after year (optional)", validators=[Optional()])
    sort_by = SelectField("Sort by", choices=[("year", "Newest first"),
                                              ("title", "Title A-Z"),
                                              ("editions", "Most editions")])
    only_with_cover = BooleanField("Only show books with a cover image")
    submit = SubmitField("Search")


# ---------------------------------------------------------------------------
# 2) FETCH DATA FROM THE API  (requirement: use `requests` + the user's input)
# ---------------------------------------------------------------------------
def build_params(form):
    """Turn the form values into API query parameters."""
    # TODO (Step 3): adapt to your API's documentation
    return {"q": form.query.data, "limit": 100}


def fetch_data(params):
    """Call the API and return the parsed JSON (a Python dict)."""
    response = requests.get(API_URL, params=params, timeout=10)
    response.raise_for_status()   # raises an error for 4xx/5xx responses
    return response.json()        # for XML use: xml.etree.ElementTree.fromstring(response.text)


# ---------------------------------------------------------------------------
# 3) PROCESS / TRANSFORM THE DATA  (requirement: filter, transform, format)
# ---------------------------------------------------------------------------
def process_data(raw, form):
    """Pick the fields we care about, filter, sort, and limit the results."""
    # TODO (Step 4): adapt to the structure of your API's JSON
    books = []
    for doc in raw.get("docs", []):
        books.append({
            "title": doc.get("title", "Unknown title"),
            "author": ", ".join(doc.get("author_name", ["Unknown author"])),
            "year": doc.get("first_publish_year"),
            "editions": doc.get("edition_count", 0),
            "cover": (f"https://covers.openlibrary.org/b/id/{doc['cover_i']}-S.jpg"
                      if doc.get("cover_i") else None),
        })

    # Filtering based on user input
    if form.min_year.data:
        books = [b for b in books if b["year"] and b["year"] >= form.min_year.data]
    if form.only_with_cover.data:
        books = [b for b in books if b["cover"]]

    # Sorting based on user input
    if form.sort_by.data == "year":
        books.sort(key=lambda b: b["year"] or 0, reverse=True)
    elif form.sort_by.data == "title":
        books.sort(key=lambda b: b["title"].lower())
    else:
        books.sort(key=lambda b: b["editions"], reverse=True)

    # Limit to the number the user asked for
    books = books[: form.max_results.data]

    # A simple aggregation to show on the results page
    years = [b["year"] for b in books if b["year"]]
    summary = {
        "count": len(books),
        "oldest": min(years) if years else "N/A",
        "newest": max(years) if years else "N/A",
    }
    return books, summary


# ---------------------------------------------------------------------------
# 4) ROUTES
# ---------------------------------------------------------------------------
@app.route("/", methods=["GET"])
def index():
    """Show the empty form."""
    return render_template("index.html", form=SearchForm())


@app.route("/results", methods=["POST"])
def results():
    """Handle the form submission (POST), call the API, show the results."""
    form = SearchForm()
    if not form.validate_on_submit():
        # Validation failed: show the form again with error messages
        return render_template("index.html", form=form)

    try:
        raw = fetch_data(build_params(form))
    except requests.exceptions.RequestException as e:
        flash(f"Could not reach the API: {e}")
        return redirect(url_for("index"))

    items, summary = process_data(raw, form)
    if not items:
        flash("No results matched your search. Try different options.")
        return redirect(url_for("index"))

    return render_template("results.html", items=items, summary=summary, form=form)


if __name__ == "__main__":
    app.run(debug=True)
