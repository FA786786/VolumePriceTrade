api_key = "your_api_key"
api_secret = "your_api_secret"

kite = KiteConnect(api_key=api_key)

# Step 1: Get request token from this login URL
print(kite.login_url())
