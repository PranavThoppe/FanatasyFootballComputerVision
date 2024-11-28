from flask import Flask, jsonify, request
import requests

# Flask app setup
app = Flask(__name__)

# NFL Teams dictionary to map acronyms to full names
nfl_teams = {
    "ARI": "Arizona Cardinals",
    "ATL": "Atlanta Falcons",
    "BAL": "Baltimore Ravens",
    "BUF": "Buffalo Bills",
    "CAR": "Carolina Panthers",
    "CHI": "Chicago Bears",
    "CIN": "Cincinnati Bengals",
    "CLE": "Cleveland Browns",
    "DAL": "Dallas Cowboys",
    "DEN": "Denver Broncos",
    "DET": "Detroit Lions",
    "GB": "Green Bay Packers",
    "HOU": "Houston Texans",
    "IND": "Indianapolis Colts",
    "JAX": "Jacksonville Jaguars",
    "KC": "Kansas City Chiefs",
    "LV": "Las Vegas Raiders",
    "LAC": "Los Angeles Chargers",
    "LAR": "Los Angeles Rams",
    "MIA": "Miami Dolphins",
    "MIN": "Minnesota Vikings",
    "NE": "New England Patriots",
    "NO": "New Orleans Saints",
    "NYG": "New York Giants",
    "NYJ": "New York Jets",
    "PHI": "Philadelphia Eagles",
    "PIT": "Pittsburgh Steelers",
    "SF": "San Francisco 49ers",
    "SEA": "Seattle Seahawks",
    "TB": "Tampa Bay Buccaneers",
    "TEN": "Tennessee Titans",
    "WAS": "Washington Commanders"
}

# Function to fetch user information
def get_user_info(username):
    url = f"https://api.sleeper.app/v1/user/{username}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Error fetching user data: {e}"}

# Function to fetch user leagues
def get_user_leagues(user_id, sport, season):
    url = f"https://api.sleeper.app/v1/user/{user_id}/leagues/{sport}/{season}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Error fetching league data: {e}"}

# Function to fetch league rosters
def get_league_rosters(league_id):
    url = f"https://api.sleeper.app/v1/league/{league_id}/rosters"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Error fetching rosters for league {league_id}: {e}"}

# Function to fetch player map
def get_player_map():
    url = "https://api.sleeper.app/v1/players/nfl"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Error fetching player map: {e}"}

# Helper function to format starter details
def format_starters(starters, player_map):
    starter_details = []
    for player_id in starters:
        player_info = player_map.get(player_id, {"full_name": "Unknown Player", "position": "Unknown", "team": "Unknown"})
        team_acronym = player_info.get("team", "Unknown")
        full_team_name = nfl_teams.get(team_acronym, "Unknown Team")
        starter_details.append({
            "Player ID": player_id,
            "Name": player_info.get("full_name"),
            "Position": player_info.get("position"),
            "Team": full_team_name
        })
    return starter_details

@app.route('/get_user_data', methods=['GET'])
def get_user_data():
    username = request.args.get('username')  # Get username from query parameter
    if not username:
        return jsonify({"error": "Missing username parameter"}), 400

    user_data = get_user_info(username)
    if "error" in user_data:
        return jsonify(user_data), 500

    user_id = user_data.get("user_id")
    sport = "nfl"
    season = "2024"

    player_map = get_player_map()
    if "error" in player_map:
        return jsonify(player_map), 500

    leagues_data = get_user_leagues(user_id, sport, season)
    if "error" in leagues_data:
        return jsonify(leagues_data), 500

    results = []
    for league in leagues_data:
        league_id = league.get('league_id')
        rosters_data = get_league_rosters(league_id)
        if "error" in rosters_data:
            return jsonify(rosters_data), 500

        for roster in rosters_data:
            if roster.get('owner_id') == user_id:
                starters = roster.get("starters", [])
                starters_info = format_starters(starters, player_map)
                results.append({
                    "League Name": league.get('name'),
                    "League ID": league_id,
                    "Starters": starters_info
                })
                break  # Stop after finding the user's roster in this league

    return jsonify(results)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
