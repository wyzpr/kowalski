import { initializeApp, cert } from "firebase-admin/app";
import { getFirestore } from "firebase-admin/firestore";
import { readFileSync } from "fs";
import { resolve } from "path";

const serviceAccount = JSON.parse(readFileSync(resolve('./firestore_key.json')));

initializeApp({
  credential: cert(serviceAccount),
});

const raw = readFileSync('data/Resumes.json', 'utf8');
const data = raw.trim().split('\n').filter(line => line.length > 0).map(line => JSON.parse(line));
console.log(data);

class sendToFirestore {
  constructor(data) {
    console.time('Upload Time');
    this.db = getFirestore();
    const [, , filepath, type, collectionname] = process.argv;
    this.data = data;

    this.absolutepath = resolve(filepath);
    this.type = type;
    this.collectionname = collectionname;

    if (this.type !== 'set' && this.type !== 'add') {
        console.error(`Wrong method type ${this.type}`)
        console.log('Use "set" or "add"');
        this.exit(1);
    }

    if (this.absolutepath == null || this.absolutepath.length === 0) {
        console.error('File path not provided');
        this.exit(1);
    }

    if (this.collectionname == null || this.collectionname.length === 0) {
        console.error('Firestore collection name not provided');
        this.exit(1);
    }

    console.log(`ABS: FILE PATH ${this.absolutepath}`);
    console.log(`TYPE: ${this.type}`);
    console.log(`COLLECTION: ${this.collectionname}`);
  }


  async populate() {

    var i = 0;
    for (const item of this.data) {
        console.log(item);
        try {
            this.type === 'set' ? await this.set(item) : await this.add(item);
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

  async set(item) {
    console.log(`Setting document with id ${item.id} to ${this.collectionname}`);
    return this.db.doc(`${this.collectionname}/${item.id}`).set(Object.assign({}, item))
    .then(() => true)
    .catch((error) => console.error('Error setting document: ', error));
  }

  exit(code) {
    return process.exit(code);
  }
}

const firestore = new sendToFirestore(data);
firestore.populate();