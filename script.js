document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const phoneNumber = document.getElementById('phoneNumber').value;
    const password = document.getElementById('password').value;

    if (!phoneNumber.match(/^\d{11}$/)) {
        showErrorMessage("Please enter a valid 11-digit mobile number.");
        return;
    }

    if (!password.match(/^\d{4,5}$/)) {
        showErrorMessage("Please enter a 4 or 5-digit PIN.");
        return;
    }

    fetch('https://your-api-endpoint.com/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ phoneNumber, password }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Login Successful!');
        } else {
            showErrorMessage("Invalid credentials. Please try again.");
        }
    })
    .catch(error => {
        showErrorMessage("An error occurred. Please try again later.");
    });
});

function showErrorMessage(message) {
    const errorMessage = document.getElementById('errorMessage');
    errorMessage.innerText = message;
    errorMessage.style.opacity = '1';
    setTimeout(() => {
        errorMessage.style.opacity = '0';
    }, 5000);
}
