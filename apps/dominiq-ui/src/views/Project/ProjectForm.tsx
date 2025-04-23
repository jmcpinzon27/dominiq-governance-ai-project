import React, { useState } from "react";
import { Formik, Form, Field } from "formik";
import * as Yup from "yup";
import { useNavigate } from "react-router-dom";
import { useProject } from "../../context/ProjectContext"; // Importa el hook del contexto
import Header from "../../components/header";
import imageTwo from "../../assets/img/gen-ia-product-hub-ux/14.png";

const initialEventsData = [
  { id: 1, name: "Proyecto 1", description: "Descripción del Proyecto 1" },
  { id: 2, name: "Proyecto 2", description: "Descripción del Proyecto 2" },
];

const ProjectForm = () => {
  const [events, setEvents] = useState(initialEventsData);
  const [showForm, setShowForm] = useState(false);
  const [isCreating, setIsCreating] = useState(false);
  const navigate = useNavigate();
  const { setCurrentProjectName } = useProject(); // Obtener el setter del contexto

  const initialValues = {
    eventName: "",
    eventDescription: "",
  };

  const validationSchema = Yup.object({
    eventName: Yup.string().required("El nombre del evento es requerido"),
    eventDescription: Yup.string().required("La descripción es requerida"),
  });

  const handleSubmit = (values, { resetForm }) => {
    const newEvent = {
      id: events.length + 1,
      name: values.eventName,
      description: values.eventDescription,
    };
    setEvents([...events, newEvent]);
    resetForm();
    setIsCreating(false);
  };

  const handleProjectClick = (id) => {
    const project = events.find(event => event.id === id);
    if (project) {
      setCurrentProjectName(project.name); // Establecer el nombre del proyecto actual en el contexto
    }
    navigate(`/project/${id}`); // Navega a la vista del proyecto
  };

  return (
    <div className="flex flex-col h-screen">
      <Header />
      <div className="flex-1 flex items-center justify-center p-6 bg-gray-100"> {/* Contenedor principal */}
        <div className={isCreating ? 'w-full max-w-2xl p-6 bg-white' : 'w-full max-w-2xl p-6 '}> {/* Contenedor del formulario */}
          {isCreating ? (
            <>
              <section className="flex flex-row space-evenly">
                <div >
                  <h2 className="text-2xl font-bold mb-4">Crear Proyecto en DominiQ</h2>
                  <p className="text-gray-500">Ingresa los datos esenciales para comenzar la evaluación: identifica el cliente, nombra el proyecto y selecciona su industria.</p>
                </div>
                <img src={imageTwo} alt="Modelo de Madurez" className="w-32 h-32 rounded-full object-cover ml-4"/>
              </section>
              <Formik
                initialValues={initialValues}
                validationSchema={validationSchema}
                onSubmit={handleSubmit}
              >
                {() => (
                  <Form className="">
                    <div className="mb-3">
                      <label htmlFor="eventName" className="block text-sm font-medium text-gray-700">
                        Nombre del Cliente
                      </label>
                      <Field
                        name="eventName"
                        className="mt-1 block w-full border border-gray-300 rounded-md p-2"
                      />
                    </div>

                    <div className="mb-3">
                      <label htmlFor="projectName" className="block text-sm font-medium text-gray-700">
                        Nombre del Proyecto
                      </label>
                      <Field
                        name="projecttName"
                        className="mt-1 block w-full border border-gray-300 rounded-md p-2"
                      />
                    </div>

                    <div className="mb-3 flex items-center"> 
                      <input type="checkbox" name="" id="" />
                      <label htmlFor="industry" className="block text-sm font-medium text-gray-700 pl-2">
                      Acepta los terminos y condiciones
                      </label>
                    </div>

                    <button
                      type="submit"
                      className="w-full bg-gray-900 text-white px-4 py-2 rounded-md hover:bg-green-600"
                    >
                      Agregar Proyecto
                    </button>

                    <button
                      type="button"
                      onClick={() => setIsCreating(false)}
                      className="mt-2 w-full bg-red-500 text-white px-4 py-2 rounded-md hover:bg-red-600"
                    >
                      Cancelar
                    </button>
                  </Form>
                )}
              </Formik>
            </>
          ) : (
            <>
              <section className="flex flex-row p-4 mb-4 shadow rounded space-evenly bg-white">
                <div>
                  <h2 className="text-2xl font-bold">Proyecto</h2>
                  <p className="text-gray-600 max-w-sm">Ingresa los datos esenciales para comenzar la evaluación: identifica el cliente, nombra el proyecto y selecciona su industria.</p>
                  <button
                    onClick={() => {
                      setShowForm(true);
                      setIsCreating(true);
                    }}
                    className="mt-6 w-full bg-gray-900 text-white px-4 py-2 rounded-md hover:bg-gray-600"
                  >
                    Nuevo Proyecto
                  </button>
                </div>
                <img src={imageTwo} alt="Modelo de Madurez" className="w-32 h-32 rounded-full object-cover mt-4" />
              </section>

              <div className="space-y-4 pt-4">
                {events.map((event) => (
                  <div
                    key={event.id}
                    className="p-4 border bg-white border-gray-300 rounded-md cursor-pointer hover:bg-gray-100 shadow"
                    onClick={() => handleProjectClick(event.id)} // Maneja el clic en el proyecto
                  >
                    <h3 className="text-lg font-semibold">{event.name}</h3>
                    <p className="text-gray-700">{event.description}</p>
                  </div>
                ))}
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default ProjectForm;