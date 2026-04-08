const ws = new WebSocket("ws://localhost:8000/ws");

ws.onmessage = (event) => {
    const msg = JSON.parse(event.data);
    if (msg.type === "update") {
        renderTable(msg.data);
    }
};

function renderTable(data) {
    const tbody = document.querySelector("#results tbody");
    tbody.innerHTML = "";

    data.forEach(row => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${row.pair}</td>
            <td>${row.buy_exchange}</td>
            <td>${row.buy_price}</td>
            <td>${row.sell_exchange}</td>
            <td>${row.sell_price}</td>
            <td>${row.spread}</td>
        `;
        tbody.appendChild(tr);
    });
}

function applySettings() {
    const minSpread = document.getElementById("minSpread").value;
    const sortField = document.getElementById("sortField").value;
    const sortDesc = document.getElementById("sortDesc").value === "true";

    fetch("/api/settings/min_spread", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(minSpread)
    });

    fetch(`/api/settings/sort?field=${sortField}&desc=${sortDesc}`, {
        method: "POST"
    });
}

