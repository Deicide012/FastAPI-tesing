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

# Endpoint για να φέρεις τα στατιστικά του προφίλ από το Instagram
@app.get("/instagram-profile")
async def get_instagram_profile():
    try:
        url = f"https://graph.instagram.com/{user_id}"
        params = {
            "fields": "id,username,account_type,follower_count,media_count",
            "access_token": access_token,
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail="Error fetching Instagram profile data.")
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while making the request: {e}")

# Endpoint για να φέρεις τα media του χρήστη
@app.get("/instagram-media")
async def get_instagram_media():
    try:
        url = f"https://graph.instagram.com/{user_id}/media"
        params = {
            "fields": "id,caption,media_type,media_url,thumbnail_url,timestamp",
            "access_token": access_token,
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail="Error fetching Instagram media data.")
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while making the request: {e}")

# Endpoint για να φέρεις insights για ένα συγκεκριμένο media
@app.get("/media-insights/{media_id}")
async def get_media_insights(media_id: str):
    try:
        url = f"https://graph.instagram.com/{media_id}/insights"
        params = {
            "metric": "engagement,impressions,reach",
            "access_token": access_token,
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail="Error fetching media insights.")
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while making the request: {e}")

# Endpoint για να φέρεις insights του προφίλ
@app.get("/profile-insights")
async def get_profile_insights():
    try:
        url = f"https://graph.instagram.com/{user_id}/insights"
        params = {
            "metric": "audience_gender_age,audience_locale,impressions,reach",
            "access_token": access_token,
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail="Error fetching profile insights.")
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while making the request: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
