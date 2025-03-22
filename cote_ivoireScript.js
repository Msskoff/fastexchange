// Fonction pour mettre à jour le tableau
function updateDashboard() {
    fetch('http://localhost:5000/get_history_cote_ivoire')
        .then(response => response.json())
        .then(data => {
            const historyTable = document.getElementById('historyTable').getElementsByTagName('tbody')[0];
            historyTable.innerHTML = '';

            data.forEach(transaction => {
                const row = historyTable.insertRow();
                row.insertCell().textContent = transaction.date;
                row.insertCell().textContent = transaction.montant;
                row.insertCell().textContent = transaction.frais;
                row.insertCell().textContent = transaction.benefice;
                row.insertCell().textContent = transaction.type_transfert;

                // Boutons d'actions
                const actionsCell = row.insertCell();
                const updateButton = document.createElement('button');
                updateButton.textContent = 'Modifier';
                updateButton.className = 'btn btn-warning btn-sm me-2';
                updateButton.onclick = () => updateTransaction(transaction.id);
                actionsCell.appendChild(updateButton);

                const deleteButton = document.createElement('button');
                deleteButton.textContent = 'Supprimer';
                deleteButton.className = 'btn btn-danger btn-sm';
                deleteButton.onclick = () => deleteTransaction(transaction.id);
                actionsCell.appendChild(deleteButton);
            });
        })
        .catch(error => console.error('Erreur:', error));
}

// Fonction pour modifier une transaction
function updateTransaction(id) {
    const newMontant = prompt("Entrez le nouveau montant:");
    const newFrais = prompt("Entrez les nouveaux frais:");
    const newTypeTransfert = prompt("Entrez le nouveau type de transfert (Envoi ou Retrait):");

    if (newMontant && newFrais && newTypeTransfert) {
        fetch(`http://localhost:5000/update_transaction_cote_ivoire/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                montant: parseFloat(newMontant),
                frais: parseFloat(newFrais),
                type_transfert: newTypeTransfert
            })
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            updateDashboard();
        })
        .catch(error => console.error('Erreur:', error));
    }
}

// Fonction pour supprimer une transaction
function deleteTransaction(id) {
    if (confirm("Êtes-vous sûr de vouloir supprimer cette transaction ?")) {
        fetch(`http://localhost:5000/delete_transaction_cote_ivoire/${id}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            updateDashboard();
        })
        .catch(error => console.error('Erreur:', error));
    }
}

// Charger les données initiales
document.addEventListener('DOMContentLoaded', updateDashboard);