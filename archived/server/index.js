// server/index.js
import express from 'express';
import bodyParser from 'body-parser';
import cors from 'cors';
import routes from './routes.js'; // Asegúrate de usar .js en la importación

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors());
app.use(bodyParser.json());

// Rutas
app.use('/api', routes);

// Iniciar el servidor
app.listen(PORT, () => {
  console.log(`Servidor escuchando en http://localhost:${PORT}`);
});