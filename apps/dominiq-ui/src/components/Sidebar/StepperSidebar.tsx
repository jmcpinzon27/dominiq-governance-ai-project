import React from "react";
import { stepperSidebarItem } from "./stepperSidebarItems";
import { useNavigate, useLocation } from "react-router-dom";

const StepperSidebar: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation(); // Obtener la ubicación actual

  // Determinar qué elemento debe estar activo
  const updatedSidebarItems = stepperSidebarItem.map(item => ({
    ...item,
    isActive: item.route === location.pathname, // Activa el elemento si la ruta coincide
  }));

  return (
    <div className="w-[250px] bg-gray-900 text-white flex flex-col">
      <div className="p-4 text-xl font-semibold">DominiQ</div>
      <ul className="flex flex-col gap-4 p-4">
        {updatedSidebarItems.map((item, index) => (
          <li
            key={index}
            className={`cursor-pointer p-2 rounded-md ${item.isActive ? "bg-gray-700" : "bg-gray-900 hover:bg-blue-600"
              }`}
            onClick={() => navigate(item.route || "")}
          >
            <div className="flex items-center text-sm">
              {React.createElement(item.icon)}
              <span className="ml-2">{item.label}</span>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default StepperSidebar;