import FormatListNumberedRtlIcon from '@mui/icons-material/FormatListNumberedRtl';
import IndustryIcon from '@mui/icons-material/Business'; // Ejemplo de otro icono
import AccountTreeIcon from '@mui/icons-material/AccountTree';
import WbTwilightIcon from '@mui/icons-material/WbTwilight';

export interface StepperSidebarItem {
  label: string;
  isActive: boolean;
  icon: React.ElementType; // Cambia a ElementType
  route?: string; // Ruta opcional para la navegación
}

export const stepperSidebarItem: StepperSidebarItem[] = [
  {
    label: "Modelo de Madurez",
    isActive: false,
    icon: WbTwilightIcon, // Sin JSX aquí
    route: "/modelo-madurez-form", // Ruta para la navegación
  },
  {
    label: "Modelo de Industria",
    isActive: false,
    icon: IndustryIcon, // Sin JSX aquí
  },
  {
    label: "Conceptualizacion Dominios",
    isActive: false,
    icon: AccountTreeIcon, // Sin JSX aquí
  },
  {
    label: "Priorizacion",
    isActive: false,
    icon: FormatListNumberedRtlIcon, // Sin JSX aquí
  },
];