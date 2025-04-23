import React from "react";
import Header from "../../components/header.tsx";
import ProjectDetail from "./ProjectDetail.tsx";

function Project() {
  return (
    <div className="h-[100dvh] flex flex-col">
      <Header />
      <ProjectDetail/>
    </div>
  );
}

export default Project;