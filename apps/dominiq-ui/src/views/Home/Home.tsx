import React from "react";
import Header from "../../components/header.tsx";
import Products from '../../components/Products.tsx';

function Home() {
  return (
    <div className="h-screen flex flex-col">
      <Header />
      <Products/>
    </div>
  );
}

export default Home;