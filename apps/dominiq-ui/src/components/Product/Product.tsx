import React from "react";
import { useNavigate } from "react-router-dom";
import AccountCircleOutlinedIcon from '@mui/icons-material/AccountCircleOutlined';

interface ProductProps {
  productName: string;
  description: string;
  productImage: string;
  productOwner: string;
  clients: number;
  lastInteraction: string;
  route: string;
}

const Product: React.FC<ProductProps> = ({
  productName,
  description,
  productImage,
  productOwner,
  clients,
  lastInteraction,
  route,
}) => {
  const navigate = useNavigate();

  const handleNavigate = () => {
    navigate(`/${route}`);
  };

  return (
    <div
      className="max-w-sm max-h-full h-[450px] bg-white rounded-lg shadow-lg overflow-visible relative my-6 cursor-pointer" // Added cursor-pointer class
      onClick={handleNavigate} // Added onClick event
    >
      <div className="h-[100px] absolute -top-5 w-full bg-blue-900 rounded-tl-lg rounded-tr-lg "></div>
      <img
        src={productImage}
        alt={productName}
        className="w-32 h-32 rounded-full border-4 border-white absolute -top-16 left-1/2 transform -translate-x-1/2 z-10 bg-gray-100 shadow-lg"
      />
      {/* Styles for a future image for bg */}
      <div className="pt-20 p-4 w-[280px]">
        <h2 className="text-xl pt-3 font-bold text-center max-h-14">{productName}</h2>
        <p className="border-t text-gray-700 text-center mb-4 max-h-16">{description}</p>
      </div>
      <div className="border-gray-400 pt-2 bg-gray-100 p-4 flex flex-col">
        <p className="text-gray-600 flex justify-between">Clients:<strong className="flex flex-end">{clients}</strong></p>
        <p className="text-gray-600 flex justify-between">Product Owner: <strong>{productOwner}</strong></p>
      </div>
      <p className="text-gray-500 mt-2 text-sm text-center ">{<AccountCircleOutlinedIcon />}Last interaction: {lastInteraction}</p>
    </div>
  );
};

export default Product;