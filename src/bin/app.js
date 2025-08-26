import express from "express";
import axios from "axios";
import cors from "cors";

const app = express()
const port = process.env.PORT || 3000

app.get('/', (req, res) => {
  res.send('Hello World!')
})

app.listen(port, (err) => {
    if (err) {
        return console.log('Error starting server', err)
    }
  console.log(`Example app listening on port ${port}`)
})