import React from 'react';
import AppRoute from './views/Routes/AppRoute.tsx';
import { ProjectProvider } from "../src/context/ProjectContext.tsx";

function App() {
  return (
    <ProjectProvider>
    <div className='bg-gray-200 box-border'>
      <AppRoute />
    </div>
    </ProjectProvider>
  )
}

export default App;
