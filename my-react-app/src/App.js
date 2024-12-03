import React, { useEffect, useState } from "react";

function App() {
  const [leagueData, setLeagueData] = useState([]);
  const [gameTimings, setGameTimings] = useState([]);
  const [teamTimings, setTeamTimings] = useState({});
  const [teams, setTeams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [gameTimingColors, setGameTimingColors] = useState({}); // Global variable to track game timing colors

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

  // Function to select a color from the predefined set, cycling through the colors
  const getGameTimingColor = (timing) => {
    const colors = ["red", "aqua", "green", "orange", "purple"];
    
    // Check if the color for this timing is already assigned
    if (!gameTimingColors[timing]) {
      const color = colors[Object.keys(gameTimingColors).length % colors.length];  // Cycle through colors based on the number of unique timings
      setGameTimingColors((prevColors) => {
        const updatedColors = { ...prevColors, [timing]: color };
        console.log(updatedColors); // Log the updated color mapping
        return updatedColors;
      });
    }

    return gameTimingColors[timing] || "gray";  // Return the color for the game timing, default to "gray" if not found
  };

  return (
    <div style={{ display: "flex", flexDirection: "row", gap: "20px" }}>
      {/* TV Web Scraping Section */}
      <div style={{ flex: "0 0 40%", padding: "10px" }}>
        <h1>TV Web Scraping Service</h1>

        <h2>Game Timings</h2>
        <ul>
          {gameTimings.map((timing, index) => (
            <li
              key={index}
              style={{
                backgroundColor: getGameTimingColor(timing), // Use the optimized color selection
                padding: "5px",
                marginBottom: "5px",
              }}
            >
              {timing}
            </li>
          ))}
        </ul>

        <h2>Teams</h2>
        <ul>
          {Object.entries(teamTimings).map(([team, timing]) => (
            <li key={team}>
              {team}: {timing}
            </li>
          ))}
        </ul>

        <h2>Matchups</h2>
        <ul>
          {teams.map((team, index) => (
            <li key={index}>{team}</li>
          ))}
        </ul>
      </div>

      {/* Sleeper Data Section */}
      <div style={{ flex: "0 0 60%", padding: "10px" }}>
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
                        <strong>Game Timing: </strong> 
                        <span style={{ color: getGameTimingColor(gameTiming) }}>{gameTiming}</span>
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
