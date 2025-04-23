// server/routes.js
import express from 'express';
import db from './db.js'; // Asegúrate de usar .js en la importación

const router = express.Router();

// Endpoint para obtener los dominios y subdominios de una industria
router.get('/domains/:industry', async (req, res) => {
  const { industry } = req.params;

  try {
      const [results] = await db.promise().query(`
          SELECT 
              i.Nombre AS industria,
              d.Nombre AS dominio,
              d.ID_Dominio AS id_dominio,
              s.Nombre AS subdominio,
              s.ID_Subdominio AS id_subdomain
          FROM Industria i
          JOIN Dominio d ON i.ID_Industria = d.ID_Industria
          JOIN Subdominio s ON d.ID_Dominio = s.ID_Dominio
          WHERE i.Nombre = ?
          ORDER BY i.Nombre, d.Nombre, s.Nombre
      `, [industry]);

      res.status(200).json(results);
  } catch (error) {
      console.error("Error en la consulta:", error); // Agrega este log
      res.status(500).json({ message: 'Error al obtener dominios y subdominios', error: error.message });
  }
});
  
// Endpoint para obtener todas las industrias
router.get('/industries', async (req, res) => {
    try {
      const [results] = await db.promise().query('SELECT * FROM Industria');
      res.status(200).json(results);
    } catch (error) {
      console.error(error);
      res.status(500).json({ message: 'Error al obtener industrias' });
    }
  });

router.get('/responsibles/:id_subdomain', async (req, res) => {
  const { id_subdomain } = req.params;

  try {
    const [results] = await db.promise().query(`
      SELECT Nombre AS responsible, Email AS email 
      FROM Responsable 
      WHERE ID_Subdominio = ?`, [id_subdomain]);

    res.status(200).json(results);
  } catch (error) {
    console.error("Error en la consulta:", error);
    res.status(500).json({ message: 'Error al obtener responsables', error: error.message });
  }
});

// Endpoint para obtener responsables por industria
router.get('/responsibles/industry/:industry', async (req, res) => {
  const { industry } = req.params;

  try {
    const [results] = await db.promise().query(`
      SELECT r.ID_Responsable AS id_responsable, r.Nombre AS responsible, r.Email AS email, s.ID_Subdominio AS id_subdomain
      FROM Responsable r
      JOIN Subdominio s ON r.ID_Subdominio = s.ID_Subdominio
      JOIN Dominio d ON s.ID_Dominio = d.ID_Dominio
      JOIN Industria i ON d.ID_Industria = i.ID_Industria
      WHERE i.Nombre = ?
    `, [industry]);

    console.log("Resultados de la consulta:", results); // Log para depuración
    res.status(200).json(results);
  } catch (error) {
    console.error("Error en la consulta:", error);
    res.status(500).json({ message: 'Error al obtener responsables', error: error.message });
  }
});

// Endpoint para insertar un nuevo dominio
router.post('/domains', async (req, res) => {
  const { nombre, id_industria } = req.body; // Extraer nombre e id_industria del cuerpo

  // Validación
  if (!nombre || !id_industria) {
    return res.status(400).json({ message: 'El nombre y el ID de la industria son requeridos para insertar un dominio.' });
  }

  try {
    // Inserción en la base de datos
    const [result] = await db.promise().query(`
      INSERT INTO Dominio (Nombre, ID_Industria)
      VALUES (?, ?)`, [nombre, id_industria]);

    res.status(201).json({ message: 'Dominio insertado correctamente.', id_dominio: result.insertId });
  } catch (error) {
    console.error("Error al insertar dominio:", error);
    res.status(500).json({ message: 'Error al insertar dominio', error: error.message });
  }
});

// Endpoint para actualizar responsables
router.post('/responsibles', async (req, res) => {
  const { id_subdomain, responsible, email } = req.body;

  // Verifica que se proporcionen los campos requeridos
  if (!id_subdomain || !responsible) {
    return res.status(400).json({ error: 'ID_Subdominio y responsable son requeridos.' });
  }

  try {
    // Insertar o actualizar el responsable
    const [responsableResult] = await db.promise().query('SELECT * FROM Responsable WHERE ID_Subdominio = ? AND Nombre = ?', [id_subdomain, responsible]);
    if (responsableResult.length > 0) {
      // Si el responsable ya existe, puedes actualizarlo si es necesario
      await db.promise().query('UPDATE Responsable SET Email = ? WHERE ID_Responsable = ?', [email, responsableResult[0].ID_Responsable]);
      return res.status(200).json({ message: 'Responsable actualizado correctamente.' });
    } else {
      // Si no existe, insertarlo
      const [insertResult] = await db.promise().query('INSERT INTO Responsable (Nombre, Email, ID_Subdominio) VALUES (?, ?, ?)', [responsible, email, id_subdomain]);
      console.log('Resultado de la inserción:', insertResult); // Log para depuración
      return res.status(201).json({ message: 'Responsable insertado correctamente.', id_responsable: insertResult.insertId });
    }
  } catch (error) {
    console.error('Error inserting or updating responsible:', error);
    res.status(500).json({ 
      message: 'Error inserting or updating responsible', 
      error: error.message,
      stack: error.stack // Esto puede ayudar a depurar
    });
  }
});

// Endpoint para insertar un nuevo subdominio
router.post('/subdomains', async (req, res) => {
  const { nombre, id_dominio } = req.body;

  // Validaciones simples
  if (!nombre || !id_dominio) {
    return res.status(400).json({ message: 'El nombre del subdominio y el ID del dominio son requeridos.' });
  }

  try {
    // Inserción en la base de datos
    const result = await db.promise().query(`
      INSERT INTO Subdominio (Nombre, ID_Dominio)
      VALUES (?, ?)`, [nombre, id_dominio]);

    res.status(201).json({ message: 'Subdominio insertado correctamente.', id_subdomain: result[0].insertId });
  } catch (error) {
    console.error("Error al insertar subdominio:", error);
    res.status(500).json({ message: 'Error al insertar subdominio', error: error.message });
  }
});

// Endpoint para actualizar responsables
router.put('/responsibles/:id', async (req, res) => {
  const { id } = req.params; // ID del responsable a actualizar
  const { responsible, email, id_subdomain } = req.body; // Datos a actualizar

  // Verifica que se proporcionen los campos requeridos
  if (!responsible || !email || !id_subdomain) {
    return res.status(400).json({ error: 'Responsable, email y ID_Subdominio son requeridos.' });
  }

  try {
    // Actualiza el responsable en la base de datos
    const [result] = await db.promise().query('UPDATE Responsable SET Nombre = ?, Email = ?, ID_Subdominio = ? WHERE ID_Responsable = ?', [responsible, email, id_subdomain, id]);

    if (result.affectedRows === 0) {
      return res.status(404).json({ message: 'Responsable no encontrado' });
    }

    res.status(200).json({ message: 'Responsable actualizado correctamente' });
  } catch (error) {
    console.error('Error al actualizar responsable:', error);
    res.status(500).json({ message: 'Error al actualizar responsable', error: error.message });
  }
});

// Endpoint para insertar un nuevo dominio
router.put('/domains/:id_dominio', async (req, res) => {
  const { id_dominio } = req.params; // ID del dominio a actualizar
  const { nombre } = req.body; // Nuevo valor para Nombre

  try {
    // Verificar que el nombre no esté vacío
    if (!nombre) {
      return res.status(400).json({ message: 'El nombre es requerido para actualizar' });
    }

    // Ejecutar la consulta para actualizar el nombre
    const [result] = await db.promise().query(`
      UPDATE Dominio
      SET Nombre = ?
      WHERE ID_Dominio = ?
    `, [nombre, id_dominio]);

    if (result.affectedRows === 0) {
      return res.status(404).json({ message: 'Dominio no encontrado' });
    }

    res.status(200).json({ message: 'Dominio actualizado correctamente' });
  } catch (error) {
    console.error("Error al actualizar dominio:", error);
    res.status(500).json({ message: 'Error al actualizar dominio', error: error.message });
  }
});

router.put('/subdomains/:id_subdomain', async (req, res) => {
  const { id_subdomain } = req.params;
  const { subdomain } = req.body; // Este es el nuevo nombre que se está enviando

  try {
    // Verificar que el subdominio no esté vacío
    if (!subdomain) {
      return res.status(400).json({ message: 'El subdominio es requerido' });
    }

    // Actualiza la columna 'Nombre' en lugar de 'Subdominio'
    const [result] = await db.promise().query(`
      UPDATE Subdominio
      SET Nombre = ?
      WHERE ID_Subdominio = ?
    `, [subdomain, id_subdomain]);

    if (result.affectedRows === 0) {
      return res.status(404).json({ message: 'Subdominio no encontrado' });
    }

    res.status(200).json({ message: 'Subdominio actualizado correctamente' });
  } catch (error) {
    console.error("Error al actualizar subdominio:", error);
    res.status(500).json({ message: 'Error al actualizar subdominio', error: error.message });
  }
});

// Endpoint para eliminar responsable, subdominio y dominio
router.delete('/delete', async (req, res) => {
  const { idDominio, idSubdominio, idResponsable } = req.body;

  try {
    // Paso 1: Verificar cuántos responsables hay para el subdominio
    const [responsablesCount] = await db.promise().query('SELECT COUNT(*) AS count FROM Responsable WHERE ID_Subdominio = ?', [idSubdominio]);
    const countResponsables = responsablesCount[0].count;

    // Si no hay responsables, eliminamos el subdominio y el dominio si es el único
    if (countResponsables === 0) {
      await db.promise().query('DELETE FROM Subdominio WHERE ID_Subdominio = ?', [idSubdominio]);
      const [subdominiosCount] = await db.promise().query('SELECT COUNT(*) AS count FROM Subdominio WHERE ID_Dominio = ?', [idDominio]);
      const countSubdominios = subdominiosCount[0].count;

      // Si el dominio tiene solo un subdominio, lo eliminamos también
      if (countSubdominios === 0) {
        await db.promise().query('DELETE FROM Dominio WHERE ID_Dominio = ?', [idDominio]);
      }

      return res.status(200).json({ message: 'Subdominio eliminado correctamente.' });
    }

    if (countResponsables > 1) {
      // Si hay más de un responsable, solo se elimina el responsable
      await db.promise().query('DELETE FROM Responsable WHERE ID_Responsable = ?', [idResponsable]);
      return res.status(200).json({ message: 'Responsable eliminado correctamente.' });
    }

    // Paso 2: Si el subdominio tiene solo un responsable, se elimina el responsable y el subdominio
    if (countResponsables === 1) {
      await db.promise().query('DELETE FROM Responsable WHERE ID_Responsable = ?', [idResponsable]);
      await db.promise().query('DELETE FROM Subdominio WHERE ID_Subdominio = ?', [idSubdominio]);

      const [subdominiosCount] = await db.promise().query('SELECT COUNT(*) AS count FROM Subdominio WHERE ID_Dominio = ?', [idDominio]);
      const countSubdominios = subdominiosCount[0].count;

      // Si el dominio tiene solo un subdominio, también se elimina
      if (countSubdominios === 0) {
        await db.promise().query('DELETE FROM Dominio WHERE ID_Dominio = ?', [idDominio]);
      }

      return res.status(200).json({ message: 'Responsable y subdominio eliminados correctamente.' });
    }

    // Si llegamos aquí, significa que no se puede realizar ninguna acción
    return res.status(400).json({ message: 'No se puede eliminar el subdominio ya que tiene responsables.' });
    
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Error al eliminar datos' });
  }
});

export default router; // Asegúrate de exportar el router