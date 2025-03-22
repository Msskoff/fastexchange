document.getElementById('transactionForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const montant = parseFloat(document.getElementById('montant').value);

    fetch('http://localhost:5000/add_transaction_togo', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            montant: montant,
            frais: 0,
            type_transfert: "Retrait"
        })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        document.getElementById('transactionForm').reset();
    })
    .catch(error => console.error('Erreur:', error));
});