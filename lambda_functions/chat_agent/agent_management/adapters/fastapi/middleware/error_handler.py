"""Error handling middleware."""
from fastapi import Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from typing import Union
import logging

logger = logging.getLogger(__name__)

class ErrorHandler:
    """Error handling middleware."""
    
    async def __call__(
        self,
        request: Request,
        call_next
    ) -> Union[JSONResponse, None]:
        """Handle errors in request processing."""
        try:
            return await call_next(request)
        except IntegrityError as e:
            logger.error(f"Database integrity error: {str(e)}")
            return JSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content={"detail": "Resource already exists"}
            )
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"detail": "Internal server error"}
            )