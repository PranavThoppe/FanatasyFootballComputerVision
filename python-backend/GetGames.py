from flask import Flask, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)

# Initialize storage variables for the fetched data
teamTimings = {}
gameTimings = []
teams = []

def run_backend_script():
    global gameTimings, teams, teamTimings
    gameTimings = []  # Clear old data
    teams = []
    teamTimings = {}

    session = requests.Session()
    startUrl = 'https://www.ontvtonight.com/user/login'
    loginUrl = 'https://www.ontvtonight.com/user/dologin'

    login_page = session.get(startUrl)
    soup = BeautifulSoup(login_page.text, 'html.parser')
    csrf_token = soup.find('meta', {'name': 'csrf-token'})['content']

    payload = {
        '_token': csrf_token,
        'email': '######', # Use own Email and Password
        'password': '######'
    }
    session.post(loginUrl, data=payload)

    nextUrl = 'https://www.ontvtonight.com/user/home'
    nextResponse = session.get(nextUrl)
    soup = BeautifulSoup(nextResponse.content, "html.parser")
    
    tables = soup.find_all('table', class_='table table-hover')
    matching_thin_elements = []
    
    for table in tables:
        thin_elements = table.find_all(class_='thin')
        for thin_element in thin_elements:
            img_tag = thin_element.find('img')
            if img_tag and img_tag.get('src'):
                matching_thin_elements.append(thin_element)
    
    urls = [thin_element.find('a')['href'] for thin_element in matching_thin_elements if thin_element.find('a')]
    
    gameInfo = []
    teamInfo = []
    for url in urls:
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            tab_panes = soup.find_all(class_="tab-pane")
            if len(tab_panes) > 0:
                gameInfo.append(tab_panes[0])
            if len(tab_panes) > 1:
                teamInfo.append(tab_panes[1])
        except requests.RequestException as e:
            print(f"Error fetching URL {url}: {e}")

    for team in teamInfo:
        strong_elements = team.find_all('strong')
        for strong in strong_elements:
            teams.append(strong.get_text(strip=True))

    for game in gameInfo:
        h5_elements = game.find_all('h5')
        for h5 in h5_elements:
            timing = h5.get_text(" ", strip=True)
            channel_number = ""
            if "(" in timing and ")" in timing:
                start = timing.rfind("(") + 1
                end = timing.rfind(")")
                channel_number = timing[start:end].strip()
            timing_with_channel = f"{timing.split('on')[0].strip()} ({channel_number})" if channel_number else timing.split('on')[0].strip()
            gameTimings.append(' '.join(timing_with_channel.split()))

    i = 0
    while i < len(teams):
        splitter = teams[i].split(" at ")
        for t in splitter:
            teamTimings[t] = i
        i += 1



@app.route('/get_teams', methods=['GET'])
def get_teams():
    return jsonify(teams)

@app.route('/get_game_timings', methods=['GET'])
def get_game_timings():
    return jsonify(gameTimings)

@app.route('/get_team_timings', methods=['GET'])
def get_team_timings():
    return jsonify(teamTimings)

@app.route('/start_backend', methods=['POST'])
def start_backend():
    try:
        run_backend_script()  # Run the backend script to pull and store data
        return jsonify({"status": "success", "message": "Backend script started successfully"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
    
