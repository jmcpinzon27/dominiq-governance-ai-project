import React from "react";
import Logo from "./Logo";
import { useProject } from "../context/ProjectContext" // Importa el hook del contexto

const Header: React.FC = () => {
  const { currentProjectName } = useProject(); // Obtiene el nombre del proyecto actual

  return (
    <header className="w-full h-[10dvh] flex items-center justify-between px-4 border-b-4 text-white relative bg-gray-800">
      <Logo />
      {currentProjectName && (
        <h1 className="text-lg font-semibold">{currentProjectName}</h1> // Muestra el nombre del proyecto actual
      )}
    </header>
  );
};

export default Header;