```md
# Components Final Project

A simple Flask web application that lets users search for books using the Open Library Search API and view matching results in a clean table.

## Overview

This project is a starter/final project template for building a small API-driven web application with Python, Flask, and WTForms. It demonstrates:

- a form-based search interface
- fetching live data from an external API
- filtering and sorting results
- rendering results in an HTML table
- basic Bootstrap styling for a responsive UI

## Features

- Search by title, author, or topic terms
- Limit the number of results
- Filter by minimum publication year
- Sort by newest, title, or most editions
- Optionally show only books with cover images
- Displays summary statistics for the returned results

## Tech Stack

- Python 3
- Flask
- Flask-WTF
- WTForms
- Requests
- Bootstrap 5 (via CDN)
- Open Library Search API

## Project Structure

```text
componentsFinalProject/
├── app.py                  # Flask app and logic
├── requirements.txt        # Python dependencies
├── templates/
│   ├── base.html           # Shared page layout
│   ├── index.html          # Search form page
│   └── results.html        # Search results page
└── README.md               # Project documentation
```

## Setup

1. Clone the repository:

```bash
git clone https://github.com/studentgreg/componentsFinalProject.git
cd componentsFinalProject
```

2. Create and activate a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate   # On macOS/Linux
venv\Scripts\activate      # On Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the App

```bash
python app.py
```

Then open the app in your browser at:

```text
http://127.0.0.1:5000
```

## How It Works

The app uses a Flask form to collect user input, sends the request parameters to the Open Library Search API, and processes the JSON response.

The `process_data()` function:

- extracts relevant book fields like title, author, year, edition count, and cover image
- applies filters based on user selections
- sorts results according to the chosen option
- limits the number of results shown
- calculates summary stats for display

## Form Fields

The search form includes:

- search term
- maximum number of results
- minimum publication year (optional)
- sorting method
- cover-only toggle

## Notes

This project currently uses the Open Library Search API, which is free and does not require an API key for basic searches. The app is structured as a starter template and can be adapted to other APIs or custom data sources.

## License

This project does not currently include a license file.
``