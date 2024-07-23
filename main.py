from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def scrape_webpage(url):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

        title = soup.title.text.strip() if soup.title else 'Başlık bulunamadı'
        h1 = soup.find("h1").text.strip() if soup.find("h1") else 'H1 bulunamadı'
        
        meta_description_tag = soup.find("meta", attrs={"name": "description"})
        meta_description = (
            meta_description_tag["content"].strip() if meta_description_tag and "content" in meta_description_tag.attrs else 'Meta açıklaması bulunamadı'
        )

        return {"title": title, "meta_description": meta_description, "h1": h1}
    else:
        print("Failed to scrape web page")
        return {"Error": "Failed to scrape web page"}

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        result = scrape_webpage(url)
        return jsonify(result)
    else:
        return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
