const express = require("express");
const mongoose = require("mongoose");
const cors = require("cors");

const app = express();

app.use(cors());
app.use(express.json());


// MongoDB Atlas connection
mongoose.connect(
"mongodb+srv://cloudshield1234:CloudShield@cluster0.knbcq78.mongodb.net/?appName=Cluster0"
)
.then(()=>{
    console.log("MongoDB Connected");
})
.catch((error)=>{
    console.log(error);
});


// Test route
app.get("/",(req,res)=>{
    res.send("CloudShield Backend Running");
});


// Receive traffic data
app.post("/analyze",(req,res)=>{

    console.log("Received Data:");
    console.log(req.body);

    res.json({
        message:"Traffic received",
        data:req.body
    });

});


app.listen(5000,()=>{
    console.log("Server running on port 5000");
});