import { initializeApp, cert } from "firebase-admin/app";
import { getFirestore } from "firebase-admin/firestore";
import { createReadStream } from "fs";
import { readFileSync } from "fs";
import { resolve } from "path";
import { createInterface } from "readline";

const serviceAccount = JSON.parse(readFileSync(resolve('./project_tools/firestore_key.json')));

initializeApp({
  credential: cert(serviceAccount),
});

async function readJsonLines() {
  const data = [];
  const fileStream = createReadStream('data/skills/job_skills.json');
  const rl = createInterface({
    input: fileStream,
    crlfDelay: Infinity
  });

  for await (const line of rl) {
    if (line.trim()) {
      data.push(JSON.parse(line));
    }
  }
  return data;
}

class sendToFirestore {
  constructor(data, collectionname) {
    console.time('Upload Time');
    this.db = getFirestore();
    this.data = data;
    this.collectionname = collectionname;

    if (this.collectionname == null || this.collectionname.length === 0) {
        console.error('Firestore collection name not provided');
        this.exit(1);
    }

    console.log(`COLLECTION: ${this.collectionname}`);
  }


  async populate() {

    var i = 0;
    for (const item of this.data) {
        console.log(item);
        try {
            await this.add(item);
        } catch (error) {
            console.error('Error adding document: ', error);
            this.exit(1);
        }

        if (this.data.length - 1 === i) {
            console.log(`**************************\n****SUCCESS UPLOAD*****\n**************************`);
            console.timeEnd("Time taken");
            this.exit(0);
        }

        i++;
    }
  }


  async add(item) {
    console.log(`Adding document to ${this.collectionname}`);
    return this.db.collection(this.collectionname).add(Object.assign({}, item))
    .then(() => true)
    .catch((error) => console.error('Error adding document: ', error));
  }

  exit(code) {
    return process.exit(code);
  }
}

// Read the data and start the upload
readJsonLines().then(data => {
  const firestore = new sendToFirestore(data, 'JobSkills');
  firestore.populate();
}).catch(error => {
  console.error('Error reading file:', error);
  process.exit(1);
});