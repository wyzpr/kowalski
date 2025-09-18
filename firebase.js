// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getFirestore } from "firebase/firestore";

// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyAWWUPMxcSgziUgplObzjAuWq6TgLtp8E4",
  authDomain: "kowalski-7e408.firebaseapp.com",
  projectId: "kowalski-7e408",
  storageBucket: "kowalski-7e408.firebasestorage.app",
  messagingSenderId: "270407210059",
  appId: "1:270407210059:web:3607fdd063da04e405e9ce",
  measurementId: "G-9RJWWSPVQR"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

export { db };