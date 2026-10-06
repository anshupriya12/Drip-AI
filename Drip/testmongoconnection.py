"""Quick connectivity check: python Drip/testmongoconnection.py  (needs MONGO_URI)."""
from db import MissingConfigError, get_client

try:
    client = get_client()
    client.admin.command("ping")
    print("Pinged your deployment. You successfully connected to MongoDB!")
except MissingConfigError as e:
    print(e)
except Exception as e:
    print(f"Connection failed: {e}")
