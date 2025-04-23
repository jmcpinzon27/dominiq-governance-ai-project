import React, { useState } from 'react';
import axios from 'axios';

const ChatAssistant = () => {
    const [messages, setMessages] = useState([]);
    const [inputText, setInputText] = useState('');
    const [loading, setLoading] = useState(false);
    const userID = "AAA"; // Puedes cambiar esto según sea necesario

    const handleSendMessage = async () => {
        if (!inputText) return;

        // Agregar el mensaje del usuario al estado
        const userMessage = { role: 'user', content: inputText };
        setMessages((prev) => [...prev, userMessage]);

        // Limpiar el campo de entrada
        setInputText('');

        // Llamar a la API
        setLoading(true);
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
        <div>
            <h1>Asistente Conversacional</h1>
            <div style={{ height: '400px', overflowY: 'scroll', border: '1px solid #ccc', padding: '10px' }}>
                {messages.map((msg, index) => (
                    <div key={index} style={{ textAlign: msg.role === 'user' ? 'right' : 'left' }}>
                        <strong>{msg.role === 'user' ? 'Tú' : 'Asistente'}:</strong> {msg.content}
                    </div>
                ))}
                {loading && <div>Cargando...</div>}
            </div>
            <input
                type="text"
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                placeholder="Escribe tu mensaje..."
            />
            <button onClick={handleSendMessage}>Enviar</button>
        </div>
    );
};

export default ChatAssistant;