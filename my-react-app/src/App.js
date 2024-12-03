import React, { useEffect, useState } from "react";

function App() {
  const [leagueData, setLeagueData] = useState([]);
  const [gameTimings, setGameTimings] = useState([]);
  const [teamTimings, setTeamTimings] = useState({});
  const [teams, setTeams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const SLEEPER_URL = "https://sleeperrosterviewer.onrender.com/get_user_data?username=Branau";
  const BASE_URL = "https://tvwebscrapingwebservice.onrender.com";

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Fetch Sleeper Data
        const sleeperResponse = await fetch(SLEEPER_URL);
        if (!sleeperResponse.ok) throw new Error(`Error fetching Sleeper data: ${sleeperResponse.statusText}`);
        const sleeperData = await sleeperResponse.json();
        setLeagueData(sleeperData);

        // Fetch TV Web Scraping Data
        const startResponse = await fetch(`${BASE_URL}/start_backend`, { method: "POST" });
        if (!startResponse.ok) throw new Error(`Error starting backend: ${startResponse.statusText}`);
        const gameTimingsResponse = await fetch(`${BASE_URL}/get_game_timings`);
        if (!gameTimingsResponse.ok) throw new Error("Error fetching game timings");
        const gameTimingsData = await gameTimingsResponse.json();
        setGameTimings(gameTimingsData);

        const teamTimingsResponse = await fetch(`${BASE_URL}/get_team_timings`);
        if (!teamTimingsResponse.ok) throw new Error("Error fetching team timings");
        const teamTimingsData = await teamTimingsResponse.json();
        setTeamTimings(teamTimingsData);

        const teamsResponse = await fetch(`${BASE_URL}/get_teams`);
        if (!teamsResponse.ok) throw new Error("Error fetching teams");
        const teamsData = await teamsResponse.json();
        setTeams(teamsData);

        setLoading(false);
      } catch (err) {
        setError(err.message);
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) return <h1>Loading...</h1>;
  if (error) return <h1>Error: {error}</h1>;

  // Helper function to get game timing
  const getGameTimingForTeam = (team) => {
    const gameIndex = teamTimings[team];
    return gameTimings[gameIndex] || "N/A"; // Return "N/A" if no timing is found
  };

  return (
    <div style={{ display: "flex", flexDirection: "row", gap: "20px" }}>
            {/* TV Web Scraping Section */}
            <div style={{ flex: 1, padding: "10px" }}>
        <h1>TV Web Scraping Service</h1>

        <h2>Game Timings</h2>
        <ul>
          {gameTimings.map((timing, index) => (
            <li key={index}>{timing}</li>
          ))}
        </ul>

        <h2>Team Timings</h2>
        <ul>
          {Object.entries(teamTimings).map(([team, timing]) => (
            <li key={team}>
              {team}: {timing}
            </li>
          ))}
        </ul>

        <h2>Teams</h2>
        <ul>
          {teams.map((team, index) => (
            <li key={index}>{team}</li>
          ))}
        </ul>
      </div>
      {/* Sleeper Data Section */}
      <div style={{ flex: 1, borderRight: "1px solid gray", padding: "10px" }}>
        <h1>Sleeper League Viewer</h1>
        {leagueData.map((league) => (
          <div key={league["League ID"]}>
            <h2>{league["League Name"]}</h2>
            <ul>
              {league.Starters.map((player, index) => {
                const gameTiming = getGameTimingForTeam(player.Team);
                return (
                  <li key={index}>
                    {player.Name || "N/A"} - {player.Position} - {player.Team}{" "}
                    {gameTiming !== "N/A" && (
                      <>
                        <strong>Game Timing:</strong> {gameTiming}
                      </>
                    )}
                  </li>
                );
              })}
            </ul>
          </div>
        ))}
      </div>


    </div>
  );
}

export default App;
