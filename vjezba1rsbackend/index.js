
import express from "express";
import cors from "cors";

const app = express();

const PORT = process.env.PORT || 3000;

app.use(cors({
  origin: [
    "http://localhost:5173",
    process.env.FRONTEND_URL
  ].filter(Boolean)
}));

app.use(express.json());

app.get("/api/test", (req, res) => {
  res.json({
    message: "Hello from Express backend!"
  });
});

app.listen(PORT, "0.0.0.0", () => {
  console.log(`Server running on port ${PORT}`);
});
