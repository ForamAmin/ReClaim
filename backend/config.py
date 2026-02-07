import os
from dotenv import load_dotenv

# 1. Load the .env file from the project root
# We go up one level from 'backend' to find the root
load_dotenv()

# 2. Get the Secret Key
SECRET_KEY = os.getenv("SECRET_KEY")

# 3. Validation: Crash if missing
if not SECRET_KEY:
    raise RuntimeError("CRITICAL ERROR: SECRET_KEY is not set in the .env file.")

# (Optional: In the future, you can add DATABASE_URL here too)