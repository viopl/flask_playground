function getNextQuote() {
    const currentId = document.getElementById("quote-id").textContent;
    fetch(`/next?id=${currentId}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById("quote").textContent = data.quote;
            document.getElementById("author").textContent = `- ${data.author}`;
            document.getElementById("quote-id").textContent = data.id;
        });
}

function getRandomQuote() {
    fetch("/random")
        .then(response => response.json())
        .then(data => {
            document.getElementById("quote").textContent = data.quote;
            document.getElementById("author").textContent = `- ${data.author}`;
            document.getElementById("quote-id").textContent = data.id;
        });
}

function login() {
    const name = prompt("Enter your name:");
    fetch("/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: name })
    })
    .then(response => response.json())
    .then(data => {
        document.title = `Quotes - Welcome ${data.name}`;
        document.querySelector("h1").textContent = `Welcome, ${data.name}!`;
    });
}