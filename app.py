from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import wikipediaapi

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///search_history.db'
db = SQLAlchemy(app)

class SearchHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    query = db.Column(db.String(255), nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query')

    # Save the query to the database
    with app.app_context():
        db.create_all()
        search_entry = SearchHistory(query=query)
        db.session.add(search_entry)
        db.session.commit()

    # Specify a user agent when making requests
    headers = {'User-Agent': 'your-app-name/1.0'}
    wiki_wiki = wikipediaapi.Wikipedia('en', headers=headers)

    page_py = wiki_wiki.page(query)

    if not page_py.exists():
        # Handle the case where the page doesn't exist
        result = f"No information found for '{query}'. Please check your spelling and try again."
    else:
        result = page_py.summary[:500]  # Displaying the first 500 characters of the summary

    return render_template('result.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)






