import { db } from "../firebase.js";
import { doc, getDoc, collection, query, where } from "firebase/firestore";

async function fetchResumeData() {
  try {
    const docRef = doc(db, "LabeledResumes", "0ITa6LNHAqIkk39M1HN2");
    const docSnap = await getDoc(docRef);

    if (docSnap.exists()) {
      console.log("Document data:", docSnap.data());
    } else {
      console.log("No such document!");
    }
  } catch (error) {
    console.error("Error fetching document:", error);
  }
}

// Execute the function
fetchResumeData().then(() => process.exit(0));

// Create a reference to the collection
const resumesRef = collection(db, "LabeledResumes");

// Create a query against the collection.
const q = query(resumesRef, where("state", "==", "CA"));