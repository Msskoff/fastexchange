document.getElementById('transactionForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const montant = parseFloat(document.getElementById('montant').value);
    const frais = parseFloat(document.getElementById('frais').value);

    fetch('http://localhost:5000/add_transaction_niger', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            montant: montant,
            frais: frais,
            type_transfert: "Envoi"
        })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        document.getElementById('transactionForm').reset();
    })
    .catch(error => console.error('Erreur:', error));
});