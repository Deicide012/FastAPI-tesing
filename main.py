from fastapi import FastAPI, HTTPException
import httpx
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# Δημιουργία του FastAPI app
app = FastAPI()

# Ρυθμίσεις για CORS
origins = [
    "http://localhost",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Άφησε να γίνονται αιτήματα από το frontend στο ίδιο ή άλλο port
    allow_credentials=True,
    allow_methods=["*"],  # Επιτρέπει όλες τις HTTP μεθόδους
    allow_headers=["*"],  # Επιτρέπει όλα τα headers
)

# Instagram Access Token και User ID (πρέπει να τα αντικαταστήσεις με τα δικά σου)
access_token = "IGAAIyBRH0gxZABZAE9fNXRoaTVjVFRkb0VDa1Bwc0VUblVmSEVYZAThNU0JSRXdOcXNxcmNSdWUzaXp5NlB4REdqTGNwdThXZAmFsNnkxTDFXTTlKRjFUS25LUVJIRnhvVTNTaHN1OXZAtTTJhQjU1Vy1KNDhiZAkRiaXZATOU1uNXpoYwZDZD"  # Αντικατάστησε με το πραγματικό Access Token
user_id = "17841461816260149"  # Αντικατάστησε με το πραγματικό Instagram User ID

# Διεύθυνση για το root endpoint
@app.get("/")
async def read_root():
    return {"message": "Hello, this is the backend API!"}

# Endpoint για να φέρεις τα βίντεο από το Instagram
@app.get("/instagram-profile")
async def get_instagram_profile():
    try:
        url = f"https://graph.instagram.com/{user_id}/media"
        params = {
            "fields": "follower_count,profile_views",
            "access_token": access_token,
        }
        
        # Κάνουμε την αίτηση στο Instagram Graph API
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
        
        # Αν το status code είναι OK, επιστρέφουμε τα δεδομένα
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail="Error fetching Instagram data.")
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while making the request: {e}")

