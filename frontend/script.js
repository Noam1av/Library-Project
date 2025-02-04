async function getGames() {
    try {
        const response = await axios.get('http://127.0.0.1:5000/games', {
            withCredentials: true  // לשלוח את העוגיה עם הבקשה
        });
        const gamesList = document.getElementById('games-list');
        gamesList.innerHTML = ''; // Clear existing list

        response.data.games.forEach(game => {
            gamesList.innerHTML += `
                <div class="game-card">
                    <h3>${game.title}</h3>
                    <p>Genre: ${game.genre}</p>
                    <p>Price: ${game.price}</p>
                    <p>Quantity: ${game.quantity}</p>
                </div>
            `;
        });
    } catch (error) {
        console.error('Error fetching games:', error);
        alert('Failed to load games');
    }
}

async function addGame() {
    const title = document.getElementById('game-title').value;
    const genre = document.getElementById('game-genre').value;
    const price = document.getElementById('game-price').value;
    const quantity = document.getElementById('game-quantity').value;

    try {
        await axios.post('http://127.0.0.1:5000/games', {
            title: title,
            genre: genre,
            price: price,
            quantity: quantity
        }, {
            withCredentials: true  // לשלוח את העוגיה עם הבקשה
        });

        // Clear form fields
        document.getElementById('game-title').value = '';
        document.getElementById('game-genre').value = '';
        document.getElementById('game-price').value = '';
        document.getElementById('game-quantity').value = '';

        // Refresh the games list
        getGames();

        alert('Game added successfully!');
    } catch (error) {
        console.error('Error adding game:', error);
        alert('Failed to add game');
    }
}

async function login() {
    const username = document.getElementById('username').value;
    const passwordInput = document.getElementById('password').value;

    axios.post('http://127.0.0.1:5000/login', {
        username: username,
        password: passwordInput
    }, {
        headers: {
            "Content-Type": "application/json"
        }
    })
    .then(response => {
        localStorage.setItem('isLoggedIn', 'true');
        alert(response.data.message);
        document.getElementById("auth-section").classList.add("hidden");
        document.getElementById("main-section").classList.remove("hidden");
        getGames();
    })
    .catch(error => {
        alert(error.response.data.error);
    })
}

async function logout() {
    axios.post('http://127.0.0.1:5000/logout', {}, {
        withCredentials: true
    }).then(response => {
        alert(response.data.message);
        document.getElementById("auth-section").classList.remove("hidden");
        document.getElementById("main-section").classList.add("hidden");
        localStorage.removeItem('isLoggedIn');
    }).catch(error => {
        alert('Error logging out');
    });
}

function checkIfLoggedIn() {
    const isLoggedIn = localStorage.getItem('isLoggedIn');
    if (isLoggedIn === 'true') {
        document.getElementById("auth-section").classList.add("hidden");
        document.getElementById("main-section").classList.remove("hidden");
        getGames();
    } else {
        document.getElementById("auth-section").classList.remove("hidden");
        document.getElementById("main-section").classList.add("hidden");
    }
}

window.onload = checkIfLoggedIn;