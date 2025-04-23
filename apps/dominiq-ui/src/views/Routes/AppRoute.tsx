import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from '../Home/Home';
import ProjectForm from '../Project/ProjectForm.js';
import Project from '../Project/Project.js';
import MaturityModel from '../Chat-modelo-madurez/MaturityModel.js';
import ModeloMadurez from '../Modelo-Madurez/ModeloMadurez.js';

function AppRoute() {
  return (
    <Router>
      <Routes>
        {/* Vista principal, inde */}
        <Route path="/" element={<Home/>} />
        <Route path="/dominiQ" element={<ProjectForm/>} />
        <Route path="/project/:id" element={<Project/>} />
        <Route path='/modelo-madurez/:id' element={<MaturityModel/>}></Route>
        <Route path='/modelo-madurez-form' element={<ModeloMadurez/>}></Route>
      </Routes>
    </Router>
  );
}

export default AppRoute;
