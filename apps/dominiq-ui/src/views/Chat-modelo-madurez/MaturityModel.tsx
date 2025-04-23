import React from "react";
import Header from "../../components/header";
import ChatAssistant from "../../components/Chats/ChatAssistant";

const ConnectedProduct = () => {
    return (
        <div className="flex flex-col">
            <Header />
            <div> {/* Contenedor principal */}
                <ChatAssistant />
            </div>
        </div>
    );
};

export default ConnectedProduct;