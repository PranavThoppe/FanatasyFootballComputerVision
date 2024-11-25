import requests

# Start a session to maintain cookies
session = requests.Session()

# URL of the login page (you need to inspect the actual URL on the website)
login_url = 'https://www.ontvtonight.com/user/login/'

# Your login credentials
payload = {
    'username': 'prv.thoppe@gmail.com',  # replace with your actual username
    'password': 'hyguys..',  # replace with your actual password
    # You may need to include other hidden form fields here if required
}

# Send a POST request to log in
response = session.get(login_url, data=payload, timeout=10)  # Timeout set to 10 seconds


# Check if login was successful
if response.status_code == 200:
    print("Login successful!")
    next_page_url = 'https://www.ontvtonight.com/user/home/'
    response = session.get(next_page_url)

    if response.status_code == 200:
        print("Navigated to new page successfully!")
        print(response.text)  # Print the content of the page
    else:
        print(f"Failed to navigate to the page. Status code: {response.status_code}")
    # Now you can use `session` to make further requests to the site
else:
    print("Login failed. Status code:", response.status_code)