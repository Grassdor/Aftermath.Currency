from fastapi import FastAPI, status
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .parser.currency import Code
from .parser.parser import CBRParser
from .schema import Rate, HealthStatus
from .parser.utils import check_availability

app = FastAPI()
parser = CBRParser()


# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/healthcheck", response_model=HealthStatus, tags=["Health Check"], status_code=status.HTTP_200_OK)
async def health_check():
    """
    Health check endpoint to ensure the application is up and running.
    """
    if await check_availability(parser.URL):
        return HealthStatus(status="ok") 
    else:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="CBR service is unavailable")


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


@app.exception_handler(Exception)
async def server_error_exception_handler(request, exc):
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


@app.get('/rates', status_code=status.HTTP_200_OK, response_model=Rate)
async def get_course(source_currency: Code, target_currency: Code | None = Code.RUB):
    return Rate(
        pair=f"{source_currency}/{target_currency}", 
        rate=await parser.get_rate(source_currency, target_currency)
    )
