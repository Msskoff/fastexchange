// Configuration du graphique global
const globalCtx = document.getElementById('globalChart').getContext('2d');
const globalChart = new Chart(globalCtx, {
    type: 'bar',
    data: {
        labels: ['Togo', 'Côte d\'Ivoire', 'Niger'],
        datasets: [{
            label: 'Bénéfice Total par Pays',
            data: [0, 0, 0], // Initialisation des données
            backgroundColor: [
                'rgba(75, 192, 192, 0.2)',
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)'
            ],
            borderColor: [
                'rgba(75, 192, 192, 1)',
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: {
                position: 'top',
            },
            title: {
                display: true,
                text: 'Bénéfice Total par Pays'
            }
        },
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

// Fonction pour mettre à jour le tableau global
function updateGlobalDashboard() {
    fetch('http://localhost:5000/get_all_transactions')
        .then(response => response.json())
        .then(data => {
            const globalTable = document.getElementById('globalTable').getElementsByTagName('tbody')[0];
            globalTable.innerHTML = '';

            const beneficeParPays = {
                "Togo": 0,
                "Côte d'Ivoire": 0,
                "Niger": 0
            };

            data.forEach(transaction => {
                const row = globalTable.insertRow();
                row.insertCell().textContent = transaction.pays;
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
                updateButton.onclick = () => updateTransaction(transaction.pays, transaction.id);
                actionsCell.appendChild(updateButton);

                const deleteButton = document.createElement('button');
                deleteButton.textContent = 'Supprimer';
                deleteButton.className = 'btn btn-danger btn-sm';
                deleteButton.onclick = () => deleteTransaction(transaction.pays, transaction.id);
                actionsCell.appendChild(deleteButton);

                // Calculer le bénéfice total par pays
                beneficeParPays[transaction.pays] += transaction.benefice;
            });

            // Mettre à jour le graphique global
            globalChart.data.datasets[0].data = [
                beneficeParPays["Togo"],
                beneficeParPays["Côte d'Ivoire"],
                beneficeParPays["Niger"]
            ];
            globalChart.update();
        })
        .catch(error => console.error('Erreur:', error));
}

// Fonction pour modifier une transaction
function updateTransaction(pays, id) {
    const newMontant = prompt("Entrez le nouveau montant:");
    const newFrais = prompt("Entrez les nouveaux frais:");
    const newTypeTransfert = prompt("Entrez le nouveau type de transfert (Envoi ou Retrait):");

    if (newMontant && newFrais && newTypeTransfert) {
        let endpoint = '';
        if (pays === "Togo") {
            endpoint = `/update_transaction_togo/${id}`;
        } else if (pays === "Côte d'Ivoire") {
            endpoint = `/update_transaction_cote_ivoire/${id}`;
        } else if (pays === "Niger") {
            endpoint = `/update_transaction_niger/${id}`;
        }

        fetch(`http://localhost:5000${endpoint}`, {
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
            updateGlobalDashboard();
        })
        .catch(error => console.error('Erreur:', error));
    }
}

// Fonction pour supprimer une transaction
function deleteTransaction(pays, id) {
    if (confirm("Êtes-vous sûr de vouloir supprimer cette transaction ?")) {
        let endpoint = '';
        if (pays === "Togo") {
            endpoint = `/delete_transaction_togo/${id}`;
        } else if (pays === "Côte d'Ivoire") {
            endpoint = `/delete_transaction_cote_ivoire/${id}`;
        } else if (pays === "Niger") {
            endpoint = `/delete_transaction_niger/${id}`;
        }

        fetch(`http://localhost:5000${endpoint}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            updateGlobalDashboard();
        })
        .catch(error => console.error('Erreur:', error));
    }
}

// Charger les données initiales
document.addEventListener('DOMContentLoaded', updateGlobalDashboard);