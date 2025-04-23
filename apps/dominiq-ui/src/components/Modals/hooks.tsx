import { useState, useEffect} from "react";
import axios from "axios";

// Definir el tipo para las industrias
interface Industry {
  ID_Industria: number;
  Nombre: string;
}

// Hook para obtener industrias
const useIndustries = () => {
  const [industries, setIndustries] = useState<Industry[]>([]);

  useEffect(() => {
    const fetchIndustries = async () => {
      try {
        const response = await axios.get<Industry[]>("http://localhost:5000/api/industries");
        setIndustries(response.data);
      } catch (error) {
        console.error("Error fetching industries:", error);
      }
    };

    fetchIndustries();
  }, []);

  return industries;
};

// Hook para actualizar Dominio
const useUpdateDomain = () => {
  const updateDomain = async (idDominio, newDomain) => {
    try {
      await axios.put(`http://localhost:5000/api/domains/${idDominio}`, { nombre: newDomain });
      return true; // Indica que la actualización fue exitosa
    } catch (error) {
      console.error("Error al actualizar dominio:", error);
      return false; // Indica que hubo un error
    }
  };

  return { updateDomain };
};

// Hook para actualizar Subdominio
const useUpdateSubdomain = () => {
  const updateSubdomain = async (idSubdomain, newSubdomain) => {
    try {
      await axios.put(`http://localhost:5000/api/subdomains/${idSubdomain}`, { subdomain: newSubdomain });
      return true; // Indica que la actualización fue exitosa
    } catch (error) {
      console.error("Error al actualizar subdominio:", error);
      return false; // Indica que hubo un error
    }
  };

  return { updateSubdomain };
};

// Hook para actualizar Responsable
const useUpdateResponsible = () => {
  const updateResponsible = async (idResponsible, responsible, email) => {
    try {
      await axios.put(`http://localhost:5000/api/responsibles/${idResponsible}`, { responsible, email });
      return true; // Indica que la actualización fue exitosa
    } catch (error) {
      console.error("Error al actualizar responsable:", error);
      return false; // Indica que hubo un error
    }
  };

  return { updateResponsible };
};

export { useIndustries, useUpdateDomain, useUpdateSubdomain, useUpdateResponsible };