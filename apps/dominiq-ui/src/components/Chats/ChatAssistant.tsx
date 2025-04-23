import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Face6OutlinedIcon from '@mui/icons-material/Face6Outlined';
import SmartToyOutlinedIcon from '@mui/icons-material/SmartToyOutlined';

const ChatAssistant = () => {
    const [messages, setMessages] = useState([]);
    const [inputText, setInputText] = useState('');
    const [loading, setLoading] = useState(false);
    const userID = "AAA"; // Puedes cambiar esto según sea necesario

    useEffect(() => {
        // Obtener el ID de la URL
        const path = window.location.pathname; // Obtener la ruta
        const parts = path.split('/'); // Dividir la ruta en partes
        const id = parts[parts.length - 1]; // Obtener el último elemento que debería ser el ID
        console.log("ID obtenido por la URL:", id); // Mostrar el ID en la consola
    }, []);

    const handleSendMessage = async () => {
        if (!inputText) return;

        // Agregar el mensaje del usuario al estado
        const userMessage = { role: 'user', content: inputText };
        setMessages((prev) => [...prev, userMessage]);

        // Limpiar el campo de entrada
        setInputText('');

        // Llamar a la API
        setLoading(true);
        console.log(messages);
        try {
            const response = await axios.post('/api/chat/completions', {
                model: "saia:assistant:[DominiQ]Maturity",
                revision: 4,
                messages: [
                    ...messages, // Incluye todos los mensajes anteriores
                    { role: 'user', content: inputText } // Agrega el nuevo mensaje del usuario
                ]
            }, {
                headers: {
                    "Authorization": "Bearer default_QJ6z12CWdeLnW3uKOag7xUUkzmwOC8vQk161eAJyV4NT4ozBkZyruWW9XdJqxuNKqjTVLcnS3EWt7QF9qff_C0t0-JkoevWcaOmVpzwgq6E968Dg6HfDZWEWWorsaO4j_fgC_gV3GNM3_qXgDuKr7jUbeE7xu8va9BeTlVA-Lb4=",
                    "Content-Type": "application/json",
                    "saia-conversation-id": "user1"
                }
            });
            console.log(response);

            const assistantMessage = {
                role: 'assistant',
                content: response.data.choices[0].message.content
            };
            setMessages((prev) => [...prev, assistantMessage]);
        } catch (error) {
            console.error("Error al comunicarse con la API:", error.response ? error.response.data : error.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex flex-col h-[90dvh] bg-gray-800 text-white items-center">
            <h1 className="text-3xl font-bold mb-4">DominiQ</h1>
            <div className="flex-1 overflow-y-auto bg-gray-700 rounded-lg w-full max-w-md max-h-[400px] p-4">
                {messages.map((msg, index) => (
                    <div key={index} className={`mb-2 flex items-start ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                        {msg.role === 'user' ? (
                            <Face6OutlinedIcon className="text-red-600 mr-2" />
                        ) : (
                            <SmartToyOutlinedIcon className="text-yellow-500 mr-2" />
                        )}
                        <div className={`inline-block p-3 rounded-lg bg-gray-700`}>
                            <strong>{msg.role === 'user' ? 'Tú' : 'Asistente'}:</strong> {msg.content}
                        </div>
                    </div>
                ))}
                {loading && <div className="text-center">Cargando...</div>}
            </div>
            <div className="flex mt-4 w-full max-w-md">
                <input
                    type="text"
                    value={inputText}
                    onChange={(e) => setInputText(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                    placeholder="What is up?"
                    className="flex-1 p-3 rounded-lg bg-gray-700 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <button
                    onClick={handleSendMessage}
                    className="ml-2 p-3 bg-blue-600 rounded-lg hover:bg-blue-500 transition"
                >
                    &gt;
                </button>
            </div>
        </div>
    );
};

export default ChatAssistant;