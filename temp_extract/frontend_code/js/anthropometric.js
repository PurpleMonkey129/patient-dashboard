// SheetJS library (xlsx) must be loaded in the HTML before this script

let allEntries = [];
const columns = [
  { header: "Patient ID", key: "patientId" },
  { header: "Patient Name", key: "patientName" },
  { header: "Weight (kg)", key: "weight" },
  { header: "Height (cm)", key: "height" },
  { header: "BMI", key: "bmi" }
];

// Load entries from localStorage on page load
function loadEntries() {
    const saved = localStorage.getItem('anthropometricEntries');
    allEntries = saved ? JSON.parse(saved) : [];
}
function saveEntries() {
    localStorage.setItem('anthropometricEntries', JSON.stringify(allEntries));
}

// Patient info and BMI calculation
window.onload = function() {
    loadEntries();
    const storedPatient = sessionStorage.getItem('selectedPatient');
    if (storedPatient) {
        const patient = JSON.parse(storedPatient);
        document.getElementById('patientId').value = patient.id;
        document.getElementById('patientName').value = patient.name;
        document.getElementById('selectedPatientInfo').textContent = 
            `Patient: ${patient.name} (ID: ${patient.id})`;
    } else {
        alert('No patient selected. Please select a patient from the dashboard.');
        window.location.href = 'index.html';
    }
}

function calculateBMI() {
    const weight = parseFloat(document.getElementById('weight').value) || 0;
    const height = parseFloat(document.getElementById('height').value) || 0;
    if (weight > 0 && height > 0) {
        const bmi = (weight * 10000) / (height * height);
        document.getElementById('bmi').value = bmi.toFixed(2);
    } else {
        document.getElementById('bmi').value = '';
    }
}

['weight', 'height'].forEach(id => {
    document.getElementById(id).addEventListener('input', calculateBMI);
});

document.getElementById('anthropometricForm').addEventListener('submit', function(e) {
    e.preventDefault();
    calculateBMI();
    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData.entries());
    allEntries.push(data);
    saveEntries();
    alert("Entry added! Click 'Download All' to get the Excel file.");
    e.target.reset();
    // Restore patient info if needed
    const storedPatient = sessionStorage.getItem('selectedPatient');
    if (storedPatient) {
        const patient = JSON.parse(storedPatient);
        document.getElementById('patientId').value = patient.id;
        document.getElementById('patientName').value = patient.name;
    }
});

document.getElementById('downloadExcel').addEventListener('click', function() {
    if (allEntries.length === 0) {
        alert("No entries to download!");
        return;
    }
    // Create worksheet with custom headers
    const ws = XLSX.utils.json_to_sheet(allEntries, { header: columns.map(col => col.key) });
    // Set custom header names
    columns.forEach((col, idx) => {
        const cell = XLSX.utils.encode_cell({ r: 0, c: idx });
        ws[cell].v = col.header;
    });
    // Create workbook and download
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, "Anthropometric Data");
    XLSX.writeFile(wb, "anthropometric_data.xlsx");
});

// Optional: Add a button to clear all stored data
const clearBtn = document.createElement('button');
clearBtn.textContent = 'Clear All Data';
clearBtn.type = 'button';
clearBtn.className = 'submit-button';
clearBtn.style.backgroundColor = '#e74c3c';
clearBtn.style.marginTop = '10px';
clearBtn.onclick = function() {
    if (confirm('Are you sure you want to clear all saved data?')) {
        allEntries = [];
        saveEntries();
        alert('All data cleared.');
    }
};
document.querySelector('.container').appendChild(clearBtn); 