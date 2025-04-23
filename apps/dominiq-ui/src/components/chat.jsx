import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import StepperSidebar from './Sidebar/StepperSidebar';

const Chat = () => {
    const [messages, setMessages] = useState([]);
    const [inputMessage, setInputMessage] = useState('');
    const [sessionId, setSessionId] = useState('session10');
    const [isTyping, setIsTyping] = useState(false);
    const [diagramUrl, setDiagramUrl] = useState(null);
    const [isGenerating, setIsGenerating] = useState(false);
    const [viewDiagram, setViewDiagram] = useState(false); // Nuevo estado para controlar la vista

    const messagesEndRef = useRef(null);

    useEffect(() => {
        const showWelcomeMessage = async () => {
            setIsTyping(true);
            setTimeout(() => {
                const welcomeMessage = { text: "Hola! Soy DominiQ. ¿En qué puedo ayudarte el día de hoy?", sender: 'bot' };
                setMessages([welcomeMessage]);
                setIsTyping(false);
            }, 1500);
        };
        showWelcomeMessage();
    }, []);

    useEffect(() => {
        if (messagesEndRef.current) {
            messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
        }
    }, [messages]);

    const handleSendMessage = async () => {
        if (!inputMessage.trim()) return;

        const newMessage = { text: inputMessage, sender: 'user' };
        setMessages(prevMessages => [...prevMessages, newMessage]);
        setInputMessage('');
        setIsTyping(true);

        try {
            const response = await axios.post(
                '/chat_with_agent',
                { id: sessionId, message: inputMessage },
                { headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' } }
            );

            const botResponseContent = response.data.choices && response.data.choices.length > 0
                ? response.data.choices[0].message.content
                : "Error: No se recibió respuesta del bot.";

            const botMessage = { text: botResponseContent, sender: 'bot' };
            setMessages(prevMessages => [...prevMessages, botMessage]);
        } catch (error) {
            console.error("Error al enviar el mensaje:", error);
            setMessages(prevMessages => [...prevMessages, { text: "Error al contactar con el servidor", sender: 'bot' }]);
        } finally {
            setIsTyping(false);
        }
    };

    const handleGenerateDiagram = async () => {
        setIsGenerating(true);
    
        try {
            const response = await fetch('/generate_diagram_from_chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify({ id: sessionId })
            });
    
            if (!response.ok) {
                throw new Error(`Error en la respuesta: ${response.status} ${response.statusText}`);
            }
    
            const data = await response.json();
            if (data.diagram_url) {
                setDiagramUrl(data.diagram_url);
                setViewDiagram(true); // Cambia a la vista del diagrama
            } else {
                console.error("No se recibió URL del diagrama:", data);
            }
        } catch (error) {
            console.error("Error al generar el diagrama:", error);
            alert(`Error: ${error.message}`);
            setDiagramUrl(null);
        } finally {
            setIsGenerating(false);
        }
    };

    const handleBackToChat = () => {
        setViewDiagram(false); // Regresa a la vista del chat
    };

    return (
        <div className="flex h-screen">
            <StepperSidebar />
            <div className="w-full h-full flex flex-col items-center justify-end overflow-hidden">
                {viewDiagram ? (
                    <div className="flex flex-col items-center justify-center w-full h-full">
                        <h2 className="text-xl font-bold mb-4">Diagrama Generado</h2>
                        <iframe 
                            src={diagramUrl} 
                            className="w-full h-96 border border-gray-300" 
                            title="Diagrama generado" 
                            sandbox="allow-same-origin allow-scripts"
                        ></iframe>
                        <button
                            className="mt-4 px-4 py-2 rounded-full bg-blue-500 text-white"
                            onClick={handleBackToChat}
                        >
                            Volver al Chat
                        </button>
                    </div>
                ) : (
                    <div className="w-full flex-grow p-4 overflow-y-auto box-border flex flex-col">
                        {messages.map((message, index) => (
                            <div
                                key={index}
                                className={`max-w-[70%] p-3 my-2 rounded-2xl ${message.sender === "user"
                                    ? "self-end bg-blue-600 text-white"
                                    : "self-start bg-white/90 text-gray-800"}`}
                            >
                                {message.text}
                            </div>
                        ))}
                        {isTyping && (
                            <div className="font-bold text-lg text-gray-600 bg-transparent p-1 rounded-md animate-pulse inline-block text-center w-6">...</div>
                        )}
                        <div ref={messagesEndRef} />
                    </div>
                )}
                {!viewDiagram && (
                    <div className="w-full sticky bottom-0 flex justify-evenly items-center mb-4 px-4">
                        <input
                            type="text"
                            className="ring-1 w-[80%] h-12 text-lg outline-none bg-white pl-5 box-border rounded-full shadow-md focus:ring-2 focus:ring-blue-400"
                            value={inputMessage}
                            onChange={(e) => setInputMessage(e.target.value)}
                            onKeyDown={(e) => e.key === 'Enter' && handleSendMessage()}
                            placeholder="Escribe un mensaje..."
                        />
                        <button
                            className="w-12 h-12 bg-blue-500 border-none text-white text-xl cursor-pointer rounded-full flex justify-center items-center box-border"
                            onClick={handleSendMessage}
                        >
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" className="w-5 h-5 font-extrabold" viewBox="0 0 16 16">
                                <path d="M15.854.146a.5.5 0 0 1 .11.54l-5.819 14.547a.75.75 0 0 1-1.329.124l-3.178-4.995L.643 7.184a.75.75 0 0 1 .124-1.33L15.314.037a.5.5 0 0 1 .54.11ZM6.636 10.07l2.761 4.338L14.13 2.576zm6.787-8.201L1.591 6.602l4.339 2.76z" />
                            </svg>
                        </button>
                    </div>
                )}
                {!viewDiagram && (
                    <button
                        className={`mt-4 px-4 py-2 rounded-full text-white ${isGenerating ? 'bg-gray-400 cursor-not-allowed' : 'bg-green-500'}`}
                        onClick={handleGenerateDiagram}
                        disabled={isGenerating}
                    >
                        {isGenerating ? 'Generando...' : 'Generar Diagrama'}
                    </button>
                )}
            </div>
        </div>
    );
};

export default Chat;