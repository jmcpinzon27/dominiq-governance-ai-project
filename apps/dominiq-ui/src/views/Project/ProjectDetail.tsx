import React, { useState } from "react";
import StepperSidebar from "../../components/Sidebar/StepperSidebar";
import imageTwo from "../../assets/img/gen-ia-product-hub-ux/14.png";
import { useProject } from "../../context/ProjectContext";

const ProjectDetail = () => {
    const { currentProjectName } = useProject();
    const [participants, setParticipants] = useState([{ name: "" }, { name: "" }]);

    const handleParticipantsChange = (index: number, value: string) => {
        const updatedParticipants = [...participants];
        updatedParticipants[index].name = value;
        setParticipants(updatedParticipants);
    };

    const handleAddRow = () => {
        setParticipants([...participants, { name: "" }]);
    };

    const handleDeleteRow = (index: number) => {
        const updatedParticipants = participants.filter((_, i) => i !== index);
        setParticipants(updatedParticipants);
    };

    const handleSubmit = () => {
        const surveyBody = { participants: participants.filter(p => p.name !== '') };
        console.log("Encuesta creada y enviada:", surveyBody);
    };

    return (
        <main className="flex flex-row h-full overflow-hidden">
            <StepperSidebar />
            <div className="p-2 bg-gray-100 pr-4 overflow-auto flex-1">
                <h2 className="text-2xl font-bold mb-2">Detalles del {currentProjectName}</h2>
                
                {/* Sección Modelo de Madurez */}
                <section className="flex p-2 bg-white shadow rounded">
                    <div className="flex-1">
                        <h3 className="text-xl font-semibold">Modelo de Madurez</h3>
                        <p className="text-sm">
                            Ingresa los datos esenciales para comenzar la evaluación: identifica el cliente, nombra el proyecto y selecciona su industria.
                        </p>
                    </div>
                    <div className="ml-2">
                        <img src={imageTwo} alt="Modelo de Madurez" className="w-24 h-24 rounded-full object-cover" />
                    </div>
                </section>

                <section>
                    <h3 className="text-xl font-semibold">Agregar Participantes</h3>
                    <table className="w-full mt-2 border-collapse">
                        <thead>
                            <tr>
                                <th className="border p-1">Nombre del Participante</th>
                                <th className="border p-1">Acciones</th>
                            </tr>
                        </thead>
                        <tbody>
                            {participants.map((participant, index) => (
                                <tr key={index}>
                                    <td className="border p-1">
                                        <input
                                            type="text"
                                            value={participant.name}
                                            onChange={(e) => handleParticipantsChange(index, e.target.value)}
                                            placeholder="Ingresa el nombre del participante"
                                            className="w-full p-1 border rounded"
                                        />
                                    </td>
                                    <td className="border p-1">
                                        <button
                                            onClick={() => handleDeleteRow(index)}
                                            className="bg-red-500 text-white rounded px-1 py-1 hover:bg-red-600"
                                        >
                                            Eliminar
                                        </button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                    <button
                        onClick={handleAddRow}
                        className="mt-2 p-1 bg-blue-500 text-white rounded hover:bg-blue-600"
                    >
                        Agregar Fila
                    </button>
                    <div className="mt-2 flex justify-end">
                        <button
                            onClick={handleSubmit}
                            className="p-1 bg-black text-white rounded hover:bg-gray-800"
                        >
                            Crear y Enviar Encuesta
                        </button>
                    </div>
                </section>

                <div className="flex mt-4 space-x-2">
                    <section className="flex-1 p-2 bg-white shadow rounded">
                        <h3 className="text-xl font-semibold">Instrucciones iniciales para los encuestados</h3>
                        <p className="text-sm">
                            Descripción de la sección 1. Lorem ipsum dolor sit amet,
                            consectetur adipiscing elit. Sed do eiusmod tempor incididunt
                            ut labore et dolore magna aliqua.
                        </p>
                    </section>

                    <section className="flex-1 p-2 bg-white shadow rounded">
                        <h3 className="text-xl font-semibold">Instrucciones iniciales para los encuestados</h3>
                        <p className="text-sm">
                            Ingresa los datos esenciales para comenzar la evaluación: identifica el cliente, nombra el proyecto y selecciona su industria.
                        </p>
                    </section>

                </div>
            </div>
        </main>
    );
};

export default ProjectDetail;