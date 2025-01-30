async function getGames() {
    try {
        const response = await axios.get('http://127.0.0.1:5000/games');

        // Check if games data is returned
        if (!response.data || !response.data.games || response.data.games.length === 0) {
            alert('No games available');
            return; // If no games, exit function
        }

        const gamesList = document.getElementById('games-list');
        gamesList.innerHTML = ''; // Clear existing list

        response.data.games.forEach(game => {
            gamesList.innerHTML += `
                <div class="game-card">
                    <h3>${game.name}</h3>
                    <p>Creator: ${game.creator}</p>
                    <p>Year Released: ${game.year_released}</p>
                    <p>Genre: ${game.genre}</p>
                </div>
            `;
        });
    } catch (error) {
        console.error('Error fetching games:', error);
        alert('Failed to load games');
    }
}

async function addGame() {
    const name = document.getElementById('game-name').value;
    const creator = document.getElementById('game-creator').value;
    const yearReleased = document.getElementById('game-year-released').value;
    const genre = document.getElementById('game-genre').value;

    // Check if all fields are filled
    if (!name || !creator || !yearReleased || !genre) {
        alert('Please fill in all fields!');
        return; // Stop the function if any field is empty
    }

    try {
        await axios.post('http://127.0.0.1:5000/games', {
            name: name,
            creator: creator,
            year_released: yearReleased,
            genre: genre
        });

        // Clear form fields
        document.getElementById('game-name').value = '';
        document.getElementById('game-creator').value = '';
        document.getElementById('game-year-released').value = '';
        document.getElementById('game-genre').value = '';

        // Refresh the games list
        getGames();

        alert('Game added successfully!');
    } catch (error) {
        console.error('Error adding game:', error);
        alert('Failed to add game');
    }
}


// Load all games when page loads
document.addEventListener('DOMContentLoaded', getGames);
