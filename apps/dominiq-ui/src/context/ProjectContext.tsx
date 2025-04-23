// ProjectContext.tsx
import React, { createContext, useContext, useState, ReactNode } from "react";

interface ProjectContextType {
  currentProjectName: string;
  setCurrentProjectName: (name: string) => void;
}

const ProjectContext = createContext<ProjectContextType | undefined>(undefined);

export const ProjectProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [currentProjectName, setCurrentProjectName] = useState("");

  return (
    <ProjectContext.Provider value={{ currentProjectName, setCurrentProjectName }}>
      {children}
    </ProjectContext.Provider>
  );
};

export const useProject = () => {
  const context = useContext(ProjectContext);
  if (!context) {
    throw new Error("useProject must be used within a ProjectProvider");
  }
  return context;
};