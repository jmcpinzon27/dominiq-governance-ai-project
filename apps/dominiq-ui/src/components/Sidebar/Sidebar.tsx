import React from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { sidebarItems } from "./sidebarItems";

interface SidebarProps {
  isVisible: boolean;
  toggleMenu: () => void;
}

const Sidebar: React.FC<SidebarProps> = ({ isVisible, toggleMenu }) => {
  const navigate = useNavigate();
  const location = useLocation(); // Para obtener la ruta actual

  return (
    <aside
      className={`fixed top-0 left-0 w-[250px] h-screen bg-black/80 backdrop-blur-md text-white flex flex-col p-4 transition-transform duration-300 ease-in-out z-40 ${
        isVisible ? "translate-x-0" : "-translate-x-full"
      }`}
    >
      <div className="flex justify-center items-center w-full h-[70px] mb-4">
        <input
          type="text"
          className="w-full h-[30px] rounded-lg pl-3 text-lg border-none focus:outline-none"
          placeholder="Search"
        />
      </div>
      <ul className="flex flex-col list-none p-0 m-0">
        {sidebarItems.map((item, index) => (
          <li key={index} className="mb-4">
            <button
              onClick={() => {
                toggleMenu(); // Cierra el menú al navegar
                navigate(item.route);
              }}
              className={`text-lg font-medium cursor-pointer ${
                location.pathname === item.route
                  ? "text-green-500"
                  : "text-white hover:text-green-500"
              }`}
            >
              {item.label}
            </button>
          </li>
        ))}
      </ul>
      <div className="mt-auto">
        {/* Contenido adicional para el perfil de usuario */}
      </div>
    </aside>
  );
};

export default Sidebar;
