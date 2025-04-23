import { ProductProps } from "./Product/Product";
import image from "../../assets/img/gen-ia-product-hub-ux/13.png";
import imageTwo from "../../assets/img/gen-ia-product-hub-ux/14.png";
import imageThree from "../../assets/img/gen-ia-product-hub-ux/15.png";

const productData: ProductProps[] = [
  {
    productName: "DOMINIQ",
    productMiddleName: "",
    productImage: image,
    productOwner: "Alicia Martinez",
    description:
      "Agente de IA que apoya en la definición end-to-end de modelos de gobierno de datos",
    isExpanded: false,
    onExpand: () => {},
    route: "dominiQ",
  },
  {
    productName: "TORRE DE CONTROL",
    productMiddleName: "DE COSTOS DE PRODUCCION",
    productImage: imageTwo,
    productOwner: "Alicia Martinez",
    description:
      "Lorem ipsum, placeholder or dummy text used in typesetting and graphic design for previewing layouts.",
    isExpanded: false,
    onExpand: () => {},
    route: "dominiQ",
  },
  {
    productName: "OPTIMIZADOR",
    productMiddleName: "OFERTA Y DEMANDA",
    productImage: imageThree,
    productOwner: "Alicia Martinez",
    description:
      "Lorem ipsum, placeholder or dummy text used in typesetting and graphic design for previewing layouts.",
    isExpanded: false,
    onExpand: () => {},
    route: "dominiQ",
  },
  
];

export default productData;
