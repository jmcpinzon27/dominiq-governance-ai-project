import React from "react";
import Header from "../../components/header.tsx";
import UserManagement from '../../components/Tables/UserManagement.js';

function ModeloMadurez() {
  return (
    <div className="h-[100dvh] flex flex-col">
      <Header />
      <UserManagement/>
    </div>
  );
}

export default ModeloMadurez;