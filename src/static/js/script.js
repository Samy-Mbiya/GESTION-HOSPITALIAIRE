
document.addEventListener('DOMContentLoaded', function() {
    const addRowBtn = document.getElementById('add-row');
    const formsetTable = document.querySelector('#formset-table tbody');
    const totalForms = document.getElementById('id_description_set-TOTAL_FORMS');

    // ➕ Ajouter une nouvelle ligne
    addRowBtn.addEventListener('click', () => {
        const formCount = parseInt(totalForms.value);
        const newForm = formsetTable.querySelector('.formset-row').cloneNode(true);

        // Remplacer les index des champs
        newForm.innerHTML = newForm.innerHTML.replaceAll(`description_set-0`, `description_set-${formCount}`);

        // Vider les valeurs
        newForm.querySelectorAll('input').forEach(input => input.value = '');

        formsetTable.appendChild(newForm);
        totalForms.value = formCount + 1;
    });

    // ❌ Supprimer une ligne
    formsetTable.addEventListener('click', e => {
        if (e.target.classList.contains('remove-row')) {
            e.target.closest('tr').remove();
        }
    });

    // 💰 Calcul du total à la volée
    formsetTable.addEventListener('input', e => {
        const row = e.target.closest('tr');
        const qt = parseFloat(row.querySelector('[name$="qt"]').value) || 0;
        const prix = parseFloat(row.querySelector('[name$="prix"]').value) || 0;
        const total = qt * prix;
        row.querySelector('.row-total').textContent = total.toFixed(2);
    });

    // 📨 Envoi AJAX
    const factureForm = document.getElementById('factureForm');
    factureForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(factureForm);

        fetch("", {
            method: "POST",
            body: formData,
            headers: {
                "X-Requested-With": "XMLHttpRequest",
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById('total-display').style.display = 'block';
                document.getElementById('total-value').textContent = data.total.toFixed(2);
                document.getElementById('reste-value').textContent = data.reste.toFixed(2);
                alert('✅ Facture enregistrée avec succès !');
            } else {
                alert('Erreur: ' + JSON.stringify(data.errors));
            }
        })
        .catch(err => console.error(err));
    });
});
