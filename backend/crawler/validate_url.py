import requests

def validate_url(url: str) -> dict:
    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            return {"valid": True}
        else:
            return {
                "valid": False,
                "error": f"Received status code {response.status_code}"
            }
    
    except requests.RequestException as e:
        return {
            "valid": False,
            "error": str(e)
        }
