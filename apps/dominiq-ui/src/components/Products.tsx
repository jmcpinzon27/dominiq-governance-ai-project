import React, { useState } from "react";
import Product from "./Product/Product";
import productData from "./Product/productData";

const Products: React.FC = () => {
  const [expandedProduct, setExpandedProduct] = useState<string | null>(null);

  const handleExpand = (productName: string) => {
    setExpandedProduct(expandedProduct === productName ? null : productName);
  };

  return (
    <div className="w-full h-[90dvh] flex flex-wrap justify-center items-start bg-gray-200 overflow-auto pt-16">
      {productData.map((product) => (
        <div key={product.productName} className="flex justify-center py-4 px-2 w-full sm:w-1/2 lg:w-1/3 xl:w-1/4 sm:h-5/6 lg:h-5/6 xl:h-5/6">
          <Product
            {...product}
            isExpanded={expandedProduct === product.productName}
            onExpand={() => handleExpand(product.productName)}
          />
        </div>
      ))}
    </div>
  );
};

export default Products;