import React, { useEffect, useState } from 'react';
import { Formik, Form, Field, ErrorMessage } from 'formik';
import * as Yup from 'yup';
import StepperSidebar from '../Sidebar/StepperSidebar';

// Función para interactuar con la API
const api = {
  fetchUsers: async () => {
    const response = await fetch('http://127.0.0.1:8000/users/');
    if (!response.ok) {
      throw new Error('Error al obtener usuarios');
    }
    return response.json();
  },
  fetchCompanies: async () => {
    const response = await fetch('http://127.0.0.1:8000/companies/');
    if (!response.ok) {
      throw new Error('Error al obtener compañías');
    }
    return response.json();
  },
  fetchIndustries: async () => {
    const response = await fetch('http://127.0.0.1:8000/industries/');
    if (!response.ok) {
      throw new Error('Error al obtener industrias');
    }
    return response.json();
  },
  addUser: async (user) => {
    const response = await fetch('http://127.0.0.1:8000/users/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(user),
    });
    if (!response.ok) {
      throw new Error('Error al agregar usuario');
    }
    return response.json(); // Devuelve el usuario creado
  },
};

const UserManagement = () => {
  const [users, setUsers] = useState([]);
  const [companies, setCompanies] = useState([]);
  const [industries, setIndustries] = useState([]);
  const [feedbackMessage, setFeedbackMessage] = useState('');

  useEffect(() => {
    const loadData = async () => {
      try {
        const [fetchedUsers, fetchedCompanies, fetchedIndustries] = await Promise.all([
          api.fetchUsers(),
          api.fetchCompanies(),
          api.fetchIndustries(),
        ]);
        console.log('Usuarios obtenidos:', fetchedUsers); // Mostrar usuarios en la consola
        console.log('Compañías obtenidas:', fetchedCompanies); // Mostrar compañías en la consola
        console.log('Industrias obtenidas:', fetchedIndustries); // Mostrar industrias en la consola
        setUsers(fetchedUsers.users); // Acceder al array de usuarios
        setCompanies(fetchedCompanies); // Acceder al array de compañías
        setIndustries(fetchedIndustries); // Acceder al array de industrias
      } catch (error) {
        console.error('Error al cargar datos:', error);
        setFeedbackMessage('Error al cargar datos.');
      }
    };

    loadData();
  }, []);

  // Validación de formulario
  const validationSchema = Yup.object().shape({
    user_name: Yup.string().required('El nombre de usuario es requerido'),
    email: Yup.string().email('Email inválido').required('El email es requerido'),
    role: Yup.string().required('Selecciona un rol'),
    company: Yup.string().required('El nombre de la compañía es requerido'),
    industry: Yup.string().required('Selecciona una industria'),
  });

  return (
    <div className="flex flex-row h-full overflow-hidden bg-gray-800 text-white">
      <StepperSidebar />
      <main className='w-full p-6'>
        <h2 className="text-xl font-bold mb-4">Gestión de Usuarios</h2>
        {feedbackMessage && (
          <div className="mb-4 p-2 text-center text-red-500">
            {feedbackMessage}
          </div>
        )}

        <Formik
          initialValues={{
            user_name: '',
            email: '',
            role: '',
            company: '',
            industry: '',
          }}
          validationSchema={validationSchema}
          onSubmit={async (values, { resetForm }) => {
            try {
              const newUser = await api.addUser(values);
              setUsers((prev) => [...prev, newUser]); // Agregar el nuevo usuario al estado
              resetForm(); // Resetear el formulario
              setFeedbackMessage('Usuario agregado exitosamente.'); // Mensaje de éxito
            } catch (error) {
              console.error('Error al agregar usuario:', error);
              setFeedbackMessage('Error al agregar usuario.');
            }
          }}
        >
          {() => (
            <Form className="bg-gray-900 p-4 rounded-md mb-4 flex flex-wrap gap-4">
              <div className="flex flex-col mb-2 w-full sm:w-1/5">
                <Field
                  type="text"
                  name="user_name"
                  placeholder="Nombre de usuario"
                  className="p-2 bg-gray-700 text-white rounded"
                />
                <ErrorMessage name="user_name" component="div" className="text-red-500 text-sm" />
              </div>
              <div className="flex flex-col mb-2 w-full sm:w-1/5">
                <Field
                  type="email"
                  name="email"
                  placeholder="Email"
                  className="p-2 bg-gray-700 text-white rounded"
                />
                <ErrorMessage name="email" component="div" className="text-red-500 text-sm" />
              </div>
              <div className="flex flex-col mb-2 w-full sm:w-1/5">
                <Field as="select" name="role" className="p-2 bg-gray-700 text-white rounded">
                  <option value="">Seleccionar rol</option>
                  {/* Aquí puedes agregar opciones de roles más tarde */}
                </Field>
                <ErrorMessage name="role" component="div" className="text-red-500 text-sm" />
              </div>
              <div className="flex flex-col mb-2 w-full sm:w-1/5">
                <Field as="select" name="company" className="p-2 bg-gray-700 text-white rounded">
                  <option value="">Seleccionar compañía</option>
                  {companies.map((company) => (
                    <option key={company.company_id} value={company.company_id}>
                      {company.name}
                    </option>
                  ))}
                </Field>
                <ErrorMessage name="company" component="div" className="text-red-500 text-sm" />
              </div>
              <div className="flex flex-col mb-2 w-full sm:w-1/5">
                <Field as="select" name="industry" className="p-2 bg-gray-700 text-white rounded">
                  <option value="">Seleccionar industria</option>
                  {industries.map((industry) => (
                    <option key={industry.industry_id} value={industry.industry_id}>
                      {industry.name}
                    </option>
                  ))}
                </Field>
                <ErrorMessage name="industry" component="div" className="text-red-500 text-sm" />
              </div>
              <button
                type="submit"
                className="bg-blue-600 text-white p-2 rounded hover:bg-blue-700"
              >
                Agregar Usuario
              </button>
            </Form>
          )}
        </Formik>

        <div className="overflow-x-auto">
          <table className="min-w-full border-collapse border border-gray-700 mt-4">
            <thead>
              <tr className="bg-gray-900">
                <th className="border border-gray-700 p-2 w-1/5">Nombre de Usuario</th>
                <th className="border border-gray-700 p-2 w-1/5">Email</th>
                <th className="border border-gray-700 p-2 w-1/5">Rol</th>
                <th className="border border-gray-700 p-2 w-1/5">Compañía</th>
                <th className="border border-gray-700 p-2 w-1/5">Industria</th>
              </tr>
            </thead>
            <tbody>
              {users.map((user) => (
                <tr key={user.user_id} className="bg-gray-800">
                  <td className="border border-gray-700 p-2 text-center">{user.user_name}</td>
                  <td className="border border-gray-700 p-2 text-center">{user.email}</td>
                  <td className="border border-gray-700 p-2 text-center">{user.role_id}</td> {/* Cambia esto si tienes un mapeo de roles */}
                  <td className="border border-gray-700 p-2 text-center">{user.company_id}</td> {/* Cambia esto si tienes un mapeo de compañías */}
                  <td className="border border-gray-700 p-2 text-center">{user.industry}</td> {/* Cambia esto si tienes un mapeo de industrias */}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </main>
    </div>
  );
};

export default UserManagement;