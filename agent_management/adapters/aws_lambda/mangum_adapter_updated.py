"""
AWS Lambda handler for FastAPI application using Mangum
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

# Import all route modules
from adapters.fastapi.routes.agent_routes import router as agent_router
from adapters.fastapi.routes.project_routes import router as project_router
from adapters.fastapi.routes.role_routes import router as role_router
from adapters.fastapi.routes.domain_routes import router as domain_router
from adapters.fastapi.routes.question_routes import router as question_router
from adapters.fastapi.routes.answer_routes import router as answer_router
from adapters.fastapi.routes.subdomain_routes import router as subdomain_router
from adapters.fastapi.routes.company_routes import router as company_router
from adapters.fastapi.routes.user_routes import router as user_router
from adapters.fastapi.routes.domain_question_routes import router as domain_question_router
from adapters.fastapi.routes.session_routes import router as session_router
from adapters.fastapi.routes.agent_response_routes import router as agent_response_router
from adapters.fastapi.routes.registration_routes import router as registration_routes
from adapters.fastapi.routes.industry_routes import router as industry_router  # New industry router

def create_app() -> FastAPI:
    """
    Create and configure FastAPI application
    
    Returns:
        FastAPI: Configured FastAPI application
    """
    app = FastAPI(
        title="Agent Management API",
        description="API for managing agents and related resources",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include all routers
    routers = (
        agent_router,
        project_router,
        role_router,
        domain_router,
        question_router,
        answer_router,
        subdomain_router,
        company_router,
        user_router,
        domain_question_router,
        session_router,
        agent_response_router,
        registration_routes,
        industry_router  # Add the industry router
    )

    for router in routers:
        app.include_router(router)

    return app

# Create FastAPI application
app = create_app()

# Create Lambda handler
handler = Mangum(app, lifespan="off")

# For local development
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
