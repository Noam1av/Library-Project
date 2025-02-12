async function getCustomers() {
    try {
        const response = await axios.get('http://127.0.0.1:5000/customers');
        const customersList = document.getElementById('customers-list');
        customersList.innerHTML = '';

        response.data.customers.forEach(customer => {
            const customerCard = document.createElement('div');
            customerCard.classList.add('customer-card');
            customerCard.innerHTML = `
                <h3>${customer.name}</h3>
                <p>Email: ${customer.email}</p>
                <p>Phone: ${customer.phone}</p>
                <button onclick="editCustomer(${customer.id})">Edit</button>
                <button onclick="deleteCustomer(${customer.id})">Delete</button>
            `;
            customersList.appendChild(customerCard);
        });
    } catch (error) {
        console.error('Error fetching customers:', error);
        alert('Failed to load customers.');
    }
}

async function addCustomer() {
    const name = document.getElementById('customer-name').value;
    const email = document.getElementById('customer-email').value;
    const phone = document.getElementById('customer-phone').value;

    try {
        await axios.post('http://127.0.0.1:5000/customers', {
            name: name,
            email: email,
            phone: phone
        });

        document.getElementById('customer-name').value = '';
        document.getElementById('customer-email').value = '';
        document.getElementById('customer-phone').value = '';
        getCustomers();
        alert('Customer added successfully!');
    } catch (error) {
        console.error('Error adding customer:', error);
        alert('Failed to add customer.');
    }
}

async function editCustomer(customerId) {
    const newName = prompt("Enter the new name:");
    const newEmail = prompt("Enter the new email:");
    const newPhone = prompt("Enter the new phone:");

    const data = {};

    if (newName) {
        data.name = newName;
    }
    if (newEmail) {
        data.email = newEmail;
    }
    if (newPhone) {
        data.phone = newPhone;
    }

    if (Object.keys(data).length === 0) {
        alert("Please fill in at least one field.");
        return;
    }

    try {
        await axios.put(`http://127.0.0.1:5000/customers/${customerId}`, data);
        alert("Customer updated successfully!");
        getCustomers();
    } catch (error) {
        console.error('Error editing customer:', error);
        alert("Failed to edit the customer.");
    }
}

async function deleteCustomer(customerId) {
    const confirmDelete = confirm("Are you sure you want to delete this customer?");
    if (!confirmDelete) {
        return;
    }

    try {
        await axios.delete(`http://127.0.0.1:5000/customers/${customerId}`);
        alert("Customer deleted successfully!");
        getCustomers();
    } catch (error) {
        console.error('Error deleting customer:', error);
        alert("Failed to delete the customer.");
    }
}
getCustomers();

async function getGames() {
    try {
        const response = await axios.get('http://127.0.0.1:5000/games');
        const gamesList = document.getElementById('games-list');
        gamesList.innerHTML = '';

        response.data.games.forEach(game => {
            const gameCard = document.createElement('div');
            gameCard.classList.add('game-card');
            gameCard.innerHTML = `
                <h3>${game.title}</h3>
                <p>Genre: ${game.genre}</p>
                <p>Price: ${game.price}</p>
                <p>Quantity: ${game.quantity}</p>
                <p>Status: ${game.loan_status ? 'Loaned' : 'Available'}</p>
                <button onclick="loanGame(${game.id})">Loan</button>
                <button onclick="editGame(${game.id})">Edit</button>
                <button onclick="deleteGame(${game.id})">Delete</button>
            `;
            gamesList.appendChild(gameCard);
        });
    } catch (error) {
        console.error('Error fetching games:', error);
        alert('Failed to load games.');
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
        });

        document.getElementById('game-title').value = '';
        document.getElementById('game-genre').value = '';
        document.getElementById('game-price').value = '';
        document.getElementById('game-quantity').value = '';
        getGames();
        alert('Game added successfully!');
    } catch (error) {
        console.error('Error adding game:', error);
        alert('Failed to add game.');
    }
}

async function loanGame(gameId) {
    const customerId = prompt("Enter the customer ID for the loan:");
    if (!customerId) {
        alert("Please enter a valid customer ID.");
        return;
    }

    try {
        await axios.post('http://127.0.0.1:5000/loan', {
            game_id: gameId,
            customer_id: customerId
        });
        alert("Game loaned successfully!");
        getGames();
    } catch (error) {
        console.error('Error loaning game:', error);
        alert("Failed to loan the game.");
    }
}

async function editGame(gameId) {
    const newTitle = prompt("Enter the new title:");
    const newGenre = prompt("Enter the new genre:");
    const newPrice = prompt("Enter the new price:");
    const newQuantity = prompt("Enter the new quantity:");

    const data = {};

    if (newTitle) {
        data.title = newTitle;
    }
    if (newGenre) {
        data.genre = newGenre;
    }
    if (newPrice) {
        data.price = newPrice;
    }
    if (newQuantity) {
        data.quantity = newQuantity;
    }

    if (Object.keys(data).length === 0) {
        alert("Please fill in at least one field.");
        return;
    }

    try {
        await axios.put('http://127.0.0.1:5000/games/' + gameId, data);
        alert("Game updated successfully!");
        getGames();
    } catch (error) {
        console.error('Error editing game:', error);
        alert("Failed to edit the game.");
    }
}


async function deleteGame(gameId) {
    const confirmDelete = confirm("Are you sure you want to delete this game?");
    if (!confirmDelete) {
        return;
    }

    try {
        await axios.delete('http://127.0.0.1:5000/games/' + gameId);
        alert("Game deleted successfully!");
        getGames();
    } catch (error) {
        console.error('Error deleting game:', error);
        alert("Failed to delete the game.");
    }
}

async function login() {
    const emailInput = document.getElementById('email').value;
    const passwordInput = document.getElementById('password').value;

    axios.post('http://127.0.0.1:5000/login', {
        email: emailInput,
        password: passwordInput
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
    });
}

async function logout() {
    localStorage.removeItem('isLoggedIn');
    document.getElementById("auth-section").classList.remove("hidden");
    document.getElementById("main-section").classList.add("hidden");
    alert("Logged out successfully.");
}

function checkIfLoggedIn() {
    const isLoggedIn = localStorage.getItem('isLoggedIn');
    if (isLoggedIn == 'true') {
        document.getElementById("auth-section").classList.add("hidden");
        document.getElementById("main-section").classList.remove("hidden");
        getGames();
    } else {
        document.getElementById("auth-section").classList.remove("hidden");
        document.getElementById("main-section").classList.add("hidden");
    }
}

window.onload = checkIfLoggedIn;
