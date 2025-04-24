"""
Streamlit adapter for SAIA.ai LangChain implementation.

This module provides a Streamlit interface for the SAIA.ai LangChain adapter,
specifically for survey applications with maturity questions.
"""
import pickle
import streamlit as st
from typing import List, Dict, Any, Optional

from adapters.langchain.saia_adapter import (
    SaiaSurveyChain,
    create_survey_chain,
    Question,
    ChatResponse
)
from adapters.postgres.repositories.maturity_question_repository import MaturityQuestionRepository


class StreamlitSurveyApp:
    """Streamlit application for SAIA.ai survey."""
    
    def __init__(self, session, session_id: str = "streamlit_session"):
        """
        Initialize the Streamlit survey application.
        
        Args:
            session: SQLAlchemy session
            session_id: Session identifier
        """
        self.session = session
        self.session_id = session_id
        self.repository = MaturityQuestionRepository(session)
        self.chain = None
    
    async def initialize(self, axis_id: Optional[int] = None):
        """
        Initialize the survey chain.
        
        Args:
            axis_id: Optional axis ID filter
        """
        # Check if we have a chain in the session state
        if 'chain' not in st.session_state:
            # Create a new chain
            self.chain = await create_survey_chain(
                self.repository,
                user_id=self.session_id,
                axis_id=axis_id
            )
            st.session_state.chain = self.chain
        else:
            # Use the existing chain
            self.chain = st.session_state.chain
    
    def render_survey(self):
        """Render the survey interface."""
        st.title("Maturity Assessment Survey")
        
        # Initialize messages if not in session state
        if 'messages' not in st.session_state:
            st.session_state.messages = []
        
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Your response"):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Display user message in chat message container
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Process the message
            with st.spinner("Thinking..."):
                response = self.chain.process_message(prompt)
                
                # Add assistant response to chat history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response.messages.content
                })
                
                # Display assistant response in chat message container
                with st.chat_message("assistant"):
                    st.markdown(response.messages.content)
    
    def save_session(self):
        """Save the session state."""
        if self.chain:
            # Dump the history
            history_data = self.chain.dump_history()
            
            # Save to file or database
            with open(f"{self.session_id}.pkl", "wb") as f:
                f.write(history_data)
    
    def load_session(self):
        """Load the session state."""
        try:
            # Load from file or database
            with open(f"{self.session_id}.pkl", "rb") as f:
                history_data = f.read()
            
            # Create a new chain and load the history
            self.chain = SaiaSurveyChain(user_id=self.session_id)
            self.chain.load_history(history_data)
            
            # Update session state
            st.session_state.chain = self.chain
            
            # Reconstruct messages for display
            st.session_state.messages = [
                {"role": msg["role"], "content": msg["content"]}
                for msg in self.chain.manager.messages
            ]
            
            return True
        except (FileNotFoundError, pickle.PickleError):
            return False


async def main(session, axis_id: Optional[int] = None):
    """
    Main function for the Streamlit application.
    
    Args:
        session: SQLAlchemy session
        axis_id: Optional axis ID filter
    """
    # Create the application
    app = StreamlitSurveyApp(session)
    
    # Try to load an existing session
    if not app.load_session():
        # If no session exists, initialize a new one
        await app.initialize(axis_id=axis_id)
    
    # Render the survey
    app.render_survey()
    
    # Save the session when the app is closed
    app.save_session()


if __name__ == "__main__":
    # This would be run from a Streamlit script that has access to a database session
    # import asyncio
    # asyncio.run(main(session, axis_id=1))
    print("Import this module and use the main function with a database session")
