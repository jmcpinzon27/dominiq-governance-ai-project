import React from "react";
import Chat from "../../components/chat";
import Header from "../../components/header";

const ConnectedProduct = () => {
    return (
        <div className="flex flex-col h-screen">
            <Header />
            <Chat />
        </div>
    );
};

export default ConnectedProduct;