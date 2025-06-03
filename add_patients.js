// add_patients.js
import { initializeApp } from "firebase/app";
import { getFirestore, collection, addDoc, serverTimestamp } from "firebase/firestore";

// Your Firebase config (same as in your HTML)
const firebaseConfig = {
  apiKey: "AIzaSyDtAmUF5c_VY3eUXZQEyKN8oxM_zmj9mOs",
  authDomain: "patient-dashboard-500d2.firebaseapp.com",
  projectId: "patient-dashboard-500d2",
  storageBucket: "patient-dashboard-500d2.appspot.com",
  messagingSenderId: "178852814723",
  appId: "1:178852814723:web:b92ae5e5009a1a7e66e0b6"
};

const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

async function addSamplePatients() {
  const patients = [
    { name: "John Doe", id: "P001", createdAt: serverTimestamp() },
    { name: "Jane Smith", id: "P002", createdAt: serverTimestamp() }
  ];

  for (const patient of patients) {
    await addDoc(collection(db, "patients"), patient);
    console.log(`Added patient: ${patient.name}`);
  }
}

addSamplePatients().then(() => {
  console.log("Sample patients added!");
  process.exit(0);
}).catch((err) => {
  console.error("Error adding patients:", err);
  process.exit(1);
}); 