import os

ACCESS_TOKEN = os.environ.get("PAGE_ACCESS_TOKEN") or "EAAKsvDbkZCf4BAFez4LoYPGcvsZAzX3iakXX2C7fPzbVYIRKI1esVf87EqWEBFhHM7RZCnMuyTqyyFufIZAlLHW6BZAMNrGqjD4Wb3xf6ms40nTXa6rsrZBkpWmmR26IFXUFtlG2SXvBfe184dnSjprNxy8okAKAMiBwEgjXagpP2rPBlxKENA"
VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN") or "no_verify_token"
WEATHER_API_URL = "http://openweathermap.org/data/2.5/weather?appid=f388c63063d1ade1b9221a036a6fa1af&q="

SUCCESS_STATUS = 200
VERIFY_FAIL_STATUS = 403
