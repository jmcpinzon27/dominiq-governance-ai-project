export interface SidebarItem {
    label: string; // Texto que se mostrará en el sidebar
    route: string; // Ruta de navegación
  }
  
  export const sidebarItems: SidebarItem[] = [
    { label: "Home", route: "/" },
    { label: "DominiQ", route: "/dominiQ" },
  ];
  