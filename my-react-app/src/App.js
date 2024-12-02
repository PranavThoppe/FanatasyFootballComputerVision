import React, { useEffect, useState } from "react";

function App() {
  const [gameTimings, setGameTimings] = useState([]);
  const [teamTimings, setTeamTimings] = useState({});
  const [teams, setTeams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const BASE_URL = "https://tvwebscrapingwebservice.onrender.com";

  useEffect(() => {
    const fetchBackendData = async () => {
      try {
        // Step 1: Start the backend script
        const startResponse = await fetch(`${BASE_URL}/start_backend`, {
          method: "POST",
        });

        if (!startResponse.ok) {
          throw new Error(`Error starting backend: ${startResponse.statusText}`);
        }

        const startData = await startResponse.json();
        if (startData.status !== "success") {
          throw new Error(`Backend error: ${startData.message}`);
        }

        // Step 2: Fetch game timings
        const gameTimingsResponse = await fetch(`${BASE_URL}/get_game_timings`);
        if (!gameTimingsResponse.ok) {
          throw new Error("Error fetching game timings");
        }
        const gameTimingsData = await gameTimingsResponse.json();

        // Step 3: Fetch team timings
        const teamTimingsResponse = await fetch(`${BASE_URL}/get_team_timings`);
        if (!teamTimingsResponse.ok) {
          throw new Error("Error fetching team timings");
        }
        const teamTimingsData = await teamTimingsResponse.json();

        // Step 4: Fetch teams
        const teamsResponse = await fetch(`${BASE_URL}/get_teams`);
        if (!teamsResponse.ok) {
          throw new Error("Error fetching teams");
        }
        const teamsData = await teamsResponse.json();

        // Update the state with the fetched data
        setGameTimings(gameTimingsData);
        setTeamTimings(teamTimingsData);
        setTeams(teamsData);
        setLoading(false); // Data fetching is complete
      } catch (err) {
        setError(err.message); // Handle errors
        setLoading(false);
      }
    };

    fetchBackendData();
  }, []); // Run only once when the component mounts

  // Conditional rendering based on state
  if (loading) {
    return <h1>Loading...</h1>;
  }

  if (error) {
    return <h1>Error: {error}</h1>;
  }

  return (
    <div>
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
  );
}

export default App;
