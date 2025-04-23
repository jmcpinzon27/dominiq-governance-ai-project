import React, { useState, useEffect } from "react";
import axios from "axios";
import { Formik, Form, Field, FieldArray, ErrorMessage } from "formik";
import * as Yup from "yup";

import { useIndustries, useUpdateDomain, useUpdateSubdomain, useUpdateResponsible } from "./hooks";

// Validación de formulario
const validationSchema = Yup.object().shape({
  option1: Yup.string().required("Option 1 is required"),
  rows: Yup.array().of(
    Yup.object().shape({
      domain: Yup.string().required("Domain is required"),
      subdomain: Yup.string().required("Subdomain is required"),
      responsible: Yup.string(), // No es requerido
      email: Yup.string().email("Invalid email"), // No es requerido
    })
  ),
});

const ModalForm = ({ isOpen, onClose }) => {
  const [feedbackMessage, setFeedbackMessage] = useState<string | null>(null);
  const [initialRowsData, setInitialRowsData] = useState([]);
  const industries = useIndustries();
  const { updateDomain } = useUpdateDomain();
  const { updateSubdomain } = useUpdateSubdomain();
  const { updateResponsible } = useUpdateResponsible();
  const [selectedIndustryId, setSelectedIndustryId] = useState(null);
  const [idIndustria, setIdIndustria] = useState(null);
  const [changedRows, setChangedRows] = useState([]);

  useEffect(() => {
    if (isOpen) {
      setFeedbackMessage(null);
      setInitialRowsData([]);
      setChangedRows([]); // Resetea el estado de filas cambiadas al abrir el modal
    }
  }, [isOpen]);

  const handleSelectChange = (setFieldValue) => async (event) => {
    const selectedValue = event.target.value;
    setFieldValue("option1", selectedValue);

    // Encuentra la industria seleccionada
    const selectedIndustry = industries.find(industry => industry.Nombre === selectedValue);
    const id_industria = selectedIndustry ? selectedIndustry.ID_Industria : undefined;

    // Almacenar id_industria en el estado
    setIdIndustria(id_industria);

    if (selectedValue) {
      try {
        const response = await axios.get(`http://localhost:5000/api/domains/${selectedValue}`);
        const formattedData = response.data.map(item => ({
          domain: item.dominio,
          subdomain: item.subdominio,
          responsible: '',
          email: '',
          id_subdomain: item.id_subdomain,
          id_dominio: item.id_dominio,
          id_responsable: undefined,
          id_industria: id_industria // Asegúrate de incluir id_industria aquí
        }));

        const responsiblesResponse = await axios.get(`http://localhost:5000/api/responsibles/industry/${selectedValue}`);
        const responsibles = responsiblesResponse.data;

        formattedData.forEach(row => {
          const responsible = responsibles.find(r => r.id_subdomain === row.id_subdomain);
          if (responsible) {
            row.responsible = responsible.responsible;
            row.email = responsible.email;
            row.id_responsable = responsible.id_responsable;
          }
        });

        setFieldValue("rows", formattedData);
        setInitialRowsData(formattedData);
        setChangedRows(Array(formattedData.length).fill(false)); // Inicializa el estado de filas cambiadas
      } catch (error) {
        console.error("Error fetching domains or responsibles:", error);
        setFeedbackMessage("Error al obtener dominios o responsables.");
      }
    } else {
      setFieldValue("rows", []);
    }
  };

  const handleChange = (index, setFieldValue) => {
    setChangedRows(prev => {
      const newChangedRows = [...prev];
      newChangedRows[index] = true; // Marca la fila como cambiada
      return newChangedRows;
    });
  };

  const handleDelete = async (row, index, values, setFieldValue) => {
    const { id_subdomain, id_dominio, id_responsable } = row;

    const requestData = {
      idDominio: id_dominio,
      idSubdominio: id_subdomain,
    };

    if (id_responsable) {
      requestData.idResponsable = id_responsable;
    }

    try {
      const response = await axios.delete(`http://localhost:5000/api/delete`, {
        data: requestData,
      });

      setFeedbackMessage(response.data.message);
      setFieldValue("rows", values.rows.filter((_, i) => i !== index));
      setChangedRows(prev => prev.filter((_, i) => i !== index)); // Elimina la fila cambiada
    } catch (error) {
      console.error("Error al eliminar:", error);
      setFeedbackMessage("Error al eliminar el registro.");
    }
  };

  const handleSave = async (values) => {
    const updatePromises = [];
    const insertPromises = [];
    let feedbackMessages = [];

    for (const row of values.rows) {
      const existingRow = initialRowsData.find(r => r.id_subdomain === row.id_subdomain);

      // Primero, maneja el caso donde el subdominio no existe
      if (!existingRow) {
        let idDominio = row.id_dominio;

        // Si no hay un id_dominio, inserta un nuevo dominio
        if (!idDominio) {
          const newDomainBody = {
            nombre: row.domain,
            id_industria: idIndustria // Usar la id_industria global
          };

          console.log("Cuerpo de la solicitud para insertar nuevo dominio:", newDomainBody);

          try {
            const domainResponse = await axios.post(`http://localhost:5000/api/domains`, newDomainBody);
            idDominio = domainResponse.data.id_dominio; // Asegúrate de que esto funcione correctamente
            feedbackMessages.push(`Nuevo dominio insertado: ${row.domain}`);
          } catch (error) {
            console.error("Error al insertar nuevo dominio:", error.response?.data || error.message);
            feedbackMessages.push(`Error al insertar nuevo dominio: ${row.domain}. ${error.response?.data.message || error.message}`);
            continue; // Salir de esta iteración si falla la inserción del dominio
          }
        }

        // Inserta el nuevo subdominio
        const insertSubdomainBody = {
          nombre: row.subdomain,
          id_dominio: idDominio,
        };

        console.log("Cuerpo de la solicitud para insertar subdominio:", insertSubdomainBody);

        insertPromises.push(
          axios.post(`http://localhost:5000/api/subdomains`, insertSubdomainBody)
            .then(response => {
              const newSubdomainId = response.data.id_subdomain; // Supón que el ID del subdominio insertado se devuelve aquí
              feedbackMessages.push(`Nuevo subdominio insertado: ${row.subdomain}`);

              // Ahora que tenemos el ID del nuevo subdominio, insertemos el responsable si es necesario
              if (row.responsible) {
                const responsibleBody = {
                  id_subdomain: newSubdomainId,
                  responsible: row.responsible,
                  email: row.email,
                };
                console.log("Cuerpo de la solicitud para insertar responsable:", responsibleBody);

                return axios.post(`http://localhost:5000/api/responsibles`, responsibleBody)
                  .then(() => {
                    feedbackMessages.push(`Nuevo responsable insertado para el subdominio: ${row.subdomain}`);
                  });
              }
            })
            .catch(error => {
              console.error("Error al insertar subdominio:", error.response?.data || error.message);
              feedbackMessages.push(`Error al insertar subdominio: ${row.subdomain}. ${error.response?.data.message || error.message}`);
            })
        );
      } else {
        // Maneja el caso donde el subdominio ya existe
        const responsibleExists = existingRow.id_responsable !== undefined;

        // Actualiza el responsable si es necesario
        if (responsibleExists) {
          if (row.responsible !== existingRow.responsable || row.email !== existingRow.email) {
            const updateBody = {
              responsible: row.responsible,
              email: row.email,
              id_subdomain: existingRow.id_subdomain,
            };

            console.log("Cuerpo de la solicitud para actualizar responsable:", updateBody);

            updatePromises.push(
              axios.put(`http://localhost:5000/api/responsibles/${existingRow.id_responsable}`, updateBody)
                .then(() => {
                  feedbackMessages.push(`Responsable actualizado para el subdominio: ${row.subdomain}`);
                })
                .catch(error => {
                  console.error("Error al actualizar responsable:", error);
                  feedbackMessages.push(`Error al actualizar responsable para el subdominio: ${row.subdomain}.`);
                })
            );
          }
        } else {
          // Inserta un nuevo responsable si no existe
          if (row.responsible) {
            const responsibleBody = {
              id_subdomain: existingRow.id_subdomain,
              responsible: row.responsible,
              email: row.email,
            };
            console.log("Cuerpo de la solicitud para insertar nuevo responsable:", responsibleBody);

            insertPromises.push(
              axios.post(`http://localhost:5000/api/responsibles`, responsibleBody)
            );
            feedbackMessages.push(`Nuevo responsable insertado para el subdominio: ${row.subdomain}`);
          }
        }

        // ** Aquí se añade la lógica para actualizar el dominio **
        if (row.domain !== existingRow.domain) {
          updatePromises.push(
            updateDomain(existingRow.id_dominio, row.domain)
              .then(() => {
                feedbackMessages.push(`Dominio actualizado para: ${row.domain}`);
              })
              .catch(error => {
                console.error("Error al actualizar dominio:", error);
                feedbackMessages.push(`Error al actualizar dominio para: ${row.domain}.`);
              })
          );
        }

        // Actualiza el subdominio si es necesario
        if (row.subdomain !== existingRow.subdomain) {
          updatePromises.push(updateSubdomain(existingRow.id_subdomain, row.subdomain));
          feedbackMessages.push(`Subdominio actualizado para: ${row.subdomain}`);
        }
      }
    }

    // Esperar a que se completen las promesas de actualización
    try {
      await Promise.all(updatePromises);
    } catch (error) {
      console.error("Error al actualizar responsables, subdominios o dominios:", error);
      setFeedbackMessage("Error al actualizar responsables, subdominios o dominios.");
      return;
    }

    // Ahora insertar responsables nuevos
    if (insertPromises.length > 0) {
      try {
        await Promise.all(insertPromises);
        feedbackMessages.push("Nuevos responsables insertados correctamente.");
      } catch (error) {
        console.error("Error al insertar nuevos responsables:", error);
        setFeedbackMessage("Error al insertar nuevos responsables.");
        return;
      }
    }

    // Lógica para enviar correos electrónicos
    try {
      const emailPromises = values.rows.map(row => {
        if (row.email && row.responsible) {
          return axios.post('https://sendemail-rfodgphkaq-uc.a.run.app/sendEmailFunction', {
            industry: values.option1,
            domain: row.domain,
            subdomain: row.subdomain,
            responsible: row.responsible,
            email: row.email
          });
        }
        return Promise.resolve();
      });

      await Promise.all(emailPromises);
      feedbackMessages.push("Correos electrónicos enviados correctamente.");
    } catch (error) {
      console.error("Error al enviar correos electrónicos:", error);
      setFeedbackMessage("Error al enviar correos electrónicos.");
      return;
    }

    // Mostrar mensajes de retroalimentación
    if (feedbackMessages.length > 0) {
      setFeedbackMessage(feedbackMessages.join(" | "));
    } else {
      setFeedbackMessage("No se realizaron cambios.");
    }
  };

  const handleAddRow = (values, setFieldValue) => {
    const newRow = {
      domain: '',
      subdomain: '',
      responsible: '',
      email: '',
      id_subdomain: '',
      id_responsable: undefined
    };

    setFieldValue("rows", [...values.rows, newRow]);
    setChangedRows(prev => [...prev, true]); // Marca la nueva fila como cambiada
    setFeedbackMessage("Nueva fila agregada correctamente.");
  };

  const autocompleteDomain = (value, setFieldValue, index) => {
    const existingDomain = initialRowsData.find(row => row.domain === value);
    if (existingDomain) {
      setFieldValue(`rows[${index}].id_dominio`, existingDomain.id_dominio);
    }
  };

  const autocompleteSubdomain = (value, setFieldValue, index) => {
    const existingSubdomain = initialRowsData.find(row => row.subdomain === value);
    if (existingSubdomain) {
      setFieldValue(`rows[${index}].id_subdomain`, existingSubdomain.id_subdomain);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-gray-800 bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-slate-900 p-6 rounded shadow-lg w-full max-w-5xl h-auto max-h-[94dvh] overflow-auto">
        <h2 className="text-xl font-bold mb-4 text-white">Dominios</h2>
        {feedbackMessage && (
          <div className={`mb-4 p-2 text-center ${feedbackMessage.includes("Error") ? "text-red-500" : "text-green-500"}`}>
            {feedbackMessage}
          </div>
        )}
        <Formik
          initialValues={{
            option1: "",
            rows: [],
          }}
          validationSchema={validationSchema}
          enableReinitialize
          onSubmit={handleSave}
        >
          {({ values, setFieldValue }) => (
            <Form className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label htmlFor="option1" className="block mb-1 text-white">
                    Industria
                  </label>
                  <Field
                    as="select"
                    id="option1"
                    name="option1"
                    className="w-full border rounded p-2 bg-slate-700 text-slate-300"
                    onChange={handleSelectChange(setFieldValue)}
                  >
                    <option value="" label="Select an option" disabled />
                    {industries.map((industry) => (
                      <option key={industry.ID_Industria} value={industry.Nombre}>
                        {industry.Nombre}
                      </option>
                    ))}
                  </Field>
                  <ErrorMessage name="option1" component="div" className="text-red-500 text-sm" />
                </div>
              </div>

              <FieldArray name="rows">
                {({ remove }) => (
                  <>
                    <div className="overflow-y-auto max-h-60">
                      <table className="w-full text-left table-auto">
                        <thead>
                          <tr className="bg-slate-800">
                            <th className="p-2 text-white">Domain</th>
                            <th className="p-2 text-white">Subdomain</th>
                            <th className="p-2 text-white">Responsible</th>
                            <th className="p-2 text-white">Email</th>
                            <th className="p-2 text-white">Action</th>
                          </tr>
                        </thead>
                        <tbody>
                          {values.rows.map((row, index) => {
                            const isChanged = changedRows[index];
                            const isEven = index % 2 === 0;
                            const rowClass = isChanged ? 'bg-yellow-200 text-black' : (isEven ? 'bg-slate-800 text-slate-300' : 'bg-slate-700 text-slate-300');

                            return (
                              <tr key={index} className={rowClass}>
                                <td className="p-2">
                                  <Field
                                    name={`rows[${index}].domain`}
                                    className="w-full bg-transparent p-1 resizeable-cell"
                                    style={{ border: 'none' }}
                                    onChange={(e) => {
                                      const value = e.target.value;
                                      autocompleteDomain(value, setFieldValue, index);
                                      setFieldValue(`rows[${index}].domain`, value);
                                      handleChange(index, setFieldValue); // Marca la fila como cambiada
                                    }}
                                  />
                                  <ErrorMessage name={`rows[${index}].domain`} component="div" className="text-red-500 text-sm" />
                                </td>
                                <td className="p-2">
                                  <Field
                                    name={`rows[${index}].subdomain`}
                                    className="w-full bg-transparent p-1 resizeable-cell"
                                    style={{ border: 'none' }}
                                    onChange={(e) => {
                                      const value = e.target.value;
                                      autocompleteSubdomain(value, setFieldValue, index);
                                      setFieldValue(`rows[${index}].subdomain`, value);
                                      handleChange(index, setFieldValue); // Marca la fila como cambiada
                                    }}
                                  />
                                  <ErrorMessage name={`rows[${index}].subdomain`} component="div" className="text-red-500 text-sm" />
                                </td>
                                <td className="p-2">
                                  <Field
                                    name={`rows[${index}].responsible`}
                                    className="w-full bg-transparent p-1 resizeable-cell"
                                    style={{ border: 'none' }}
                                    onChange={(e) => {
                                      setFieldValue(`rows[${index}].responsible`, e.target.value);
                                      handleChange(index, setFieldValue); // Marca la fila como cambiada
                                    }}
                                  />
                                  <ErrorMessage name={`rows[${index}].responsible`} component="div" className="text-red-500 text-sm" />
                                </td>
                                <td className="p-2">
                                  <Field
                                    name={`rows[${index}].email`}
                                    type="email"
                                    className="w-full bg-transparent p-1 resizeable-cell"
                                    style={{ border: 'none' }}
                                    onChange={(e) => {
                                      setFieldValue(`rows[${index}].email`, e.target.value);
                                      handleChange(index, setFieldValue); // Marca la fila como cambiada
                                    }}
                                  />
                                  <ErrorMessage name={`rows[${index}].email`} component="div" className="text-red-500 text-sm" />
                                </td>
                                <td className="p-2 text-center">
                                  <button
                                    type="button"
                                    onClick={() => handleDelete(row, index, values, setFieldValue)}
                                    className="text-red-500 hover:underline"
                                  >
                                    Delete
                                  </button>
                                </td>
                              </tr>
                            );
                          })}
                        </tbody>
                      </table>
                    </div>
                  </>
                )}
              </FieldArray>

              <div className="flex justify-end gap-2">
                <button
                  type="button"
                  onClick={() => handleAddRow(values, setFieldValue)}
                  className={`mt-2 px-4 py-2 ${values.option1 ? 'bg-green-500' : 'bg-gray-300 cursor-not-allowed'} text-white rounded hover:bg-green-600`}
                  disabled={!values.option1}
                >
                  Add Row
                </button>
                <button type="button" onClick={onClose} className="px-4 py-2 bg-gray-500 text-white rounded hover:bg-gray-600">Close</button>
                <button type="submit" className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">Save</button>
              </div>
            </Form>
          )}
        </Formik>
      </div>
    </div>
  );
};

export default ModalForm;