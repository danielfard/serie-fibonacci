from fastapi import FastAPI, HTTPException, Depends
import uvicorn
from utils import get_seeds_from_time, enviar_correo, fibonacci_series
import re
app = FastAPI(title="Generador de Serie Fibonacci y Envío de Correos")

# Función para validar el formato del correo electrónico utilizando regex
def validate_email_format(email: str) -> str:
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if not re.match(pattern, email):
        raise HTTPException(status_code=400, detail="Formato de correo electrónico no válido")
    return email

# Define una ruta y su función controladora
@app.get("/", summary="Generar Serie Fibonacci y Enviar Correos", tags=["Fibonacci"])
async def read_root(email_1: str = Depends(validate_email_format), email_2: str = None):
    """
    ## Endpoint para generar la serie de Fibonacci y enviarla por correo electrónico.

    **Parámetros:**
    - **email 1** (str): Correo electrónico al que se enviará la serie de Fibonacci.
    - **email 2** (str - Optional): Correo electrónico al que se enviará la serie de Fibonacci.

    **Retorna:**
    - Lista de números de la serie de Fibonacci generada.
    """
    try:
        if email_2 is not None:
            validate_email_format(email_2)
            
        seed_x, seed_y, n, current_time = get_seeds_from_time()
        fibonacci_numbers = fibonacci_series(seed_x, seed_y, n + 2)
        
        # Convertir los elementos que no son cadenas a cadenas
        lista_convertida = [str(x) for x in fibonacci_numbers]
        
        # Convertir la lista a una cadena
        cadena = ', '.join(lista_convertida)
        enviar_correo(cadena, email_1, email_2, current_time)
        
        return {"Hora":current_time, "Fibonacci List":fibonacci_numbers}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))
