import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)

CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

teamTimings = {}
gameTimings = []
teams = []

def run_backend_script():
    global gameTimings, teams, teamTimings
    # Clear the data arrays before processing
    gameTimings = []
    teams = []
    teamTimings = {}    
    session = requests.Session()

    startUrl = 'https://www.ontvtonight.com/user/login'
    loginUrl = 'https://www.ontvtonight.com/user/dologin'

    login_page = session.get(startUrl, timeout=10)
    soup = BeautifulSoup(login_page.text, 'html.parser')

    csrf_token = soup.find('meta', {'name': 'csrf-token'})['content']
    print(csrf_token)

    payload = {
        '_token': csrf_token,
        'email': 'prv.thoppe@gmail.com',
        'password': 'hyguys..'
    }

    r = session.post(loginUrl, data=payload)

    #print(r.text)

    nextUrl = 'https://www.ontvtonight.com/user/home'

    nextResponse = session.get(nextUrl)
    soup = BeautifulSoup(nextResponse.content, "html.parser")

    #print(soup)

    tables = soup.find_all('table', class_='table table-hover')
    image_url = "https://d2po7v53a8yrck.cloudfront.net/img/sport-highlight-2.png?v=920241125"


    
    matching_thin_elements = []

    #print(tables)

    # Loop through tables and find all "thin" class elements
    for index, table in enumerate(tables):
        #print(f"Table {index + 1}:")
        
        # Find all elements with class "thin" inside the table
        thin_elements = table.find_all(class_='thin')
        
        if thin_elements:
            for thin_index, thin_element in enumerate(thin_elements):
                # Look for the <img> tag inside the thin element
                
                
                
                img_tag = thin_element.find('img')
                #print(img_tag)
                if img_tag and img_tag.get('src') != None:
                    #print(thin_element)
                    # Add matching thin element to the array
                    matching_thin_elements.append(thin_element)

    #print(matching_thin_elements)
    urls = []
    
    for thin_element in matching_thin_elements:
        # Look for the <a> tag and extract the href attribute
        a_tag = thin_element.find('a')
        if a_tag and a_tag.get('href'):
            urls.append(a_tag['href'])
    
    gameInfo = []

    teamInfo = []

    for url in urls:
        print(f"Processing URL: {url}")
        
        try:
            # Fetch the page content
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # Raise an error for HTTP issues
            
            # Parse the HTML content
            soup = BeautifulSoup(response.content, "html.parser")
            
            # Find all elements with class "tab-pane"
            tab_panes = soup.find_all(class_="tab-pane")
            
            # Add the first instance to gameInfo and the second to teamInfo, if they exist
            if len(tab_panes) > 0:
                gameInfo.append(tab_panes[0])
            if len(tab_panes) > 1:
                teamInfo.append(tab_panes[1])
        except requests.RequestException as e:
            print(f"Error fetching URL {url}: {e}")

    # Print the results
    print(f"\nTotal gameInfo entries: {len(gameInfo)}")
    print(f"Total teamInfo entries: {len(teamInfo)}")


    
    for index, team in enumerate(teamInfo, start=1):
        #print(f"\nProcessing teamInfo entry {index}:")
        strong_elements = team.find_all('strong')
        for strong in strong_elements:
            strong_text = strong.get_text(strip=True)
            teams.append(strong_text)
            #print(f"  Found <strong> text: {teams}")


    for index, team in enumerate(gameInfo, start=1):
        h5_elements = team.find_all('h5')
        for h5 in h5_elements:
                # Extract the full text and clean it up
                timing = h5.get_text(" ", strip=True)  # Replace newlines with spaces

                # Extract the channel number
                channel_number = ""
                if "(" in timing and ")" in timing:
                    start = timing.rfind("(") + 1
                    end = timing.rfind(")")
                    channel_number = timing[start:end].strip()
                
                # Combine timing, date, and channel number into a single string
                timing_with_channel = f"{timing.split('on')[0].strip()} ({channel_number})" if channel_number else timing.split('on')[0].strip()
                timing_with_channel = ' '.join(timing_with_channel.split())
                # Add to gameTimings array
                gameTimings.append(timing_with_channel)



    i = 0
    while i < len(teams):
        splitter = teams[i].split(" at ")
        for t in splitter:
            teamTimings[t] = i
        i += 1
    print(teams)




def initialize_data():
    run_backend_script()


@app.route('/get_teams', methods=['GET'])
def get_teams():
    return jsonify(teams)

@app.route('/get_game_timings', methods=['GET'])
def get_game_timings():
    return jsonify(gameTimings)

@app.route('/get_team_timings', methods=['GET'])
def get_team_timings():
    return jsonify(teamTimings)



@app.route('/test', methods=['GET'])
def test():
    print("Test endpoint hit!")
    return jsonify({"status": "working"})

@app.route('/start_backend', methods=['POST'])
def start_backend():
    
    try:
        
        # Run the backend script
        run_backend_script()
        return jsonify({"status": "success", "message": "Backend script started successfully"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Start the Flask app
if __name__ == '__main__':
    initialize_data()
    app.run(debug=True)