### SCSU Campus Closet
By Reynaldo, Sana, Giovanna, Ayin, Max (Group 3)

### Overview
- Using Flask and SQLalchemy, we have created an app that works as a virtual thrift store for anybody at SCSU. Users can browse and inquire about clothes, dorm furniture, supplies, services, and more for free with fellow users.

### Features 
- Authentication and Authorization – Secure login system restricted to @southernct.edu email addresses.
- Core Campus Closet Functionality – Ability to create and view listings.
- Messaging – In-app direct messaging system to facilitate coordination between users.
- Favorites - Allows user to favorite and store listings in a 'Favorites list'.
- User Profile - User can the details of their account.
- Administrator Dashboard - Whitelist emails can access the app statistics through a dashboard after being verified as an administrator once submitting login form.

### Prerequisites
- Python 3.10+
- `pip` (Python package manager)
- Virtual environment tool (recommended)

### GCP Configuration
- URL for App: http://34.46.250.126:8080
- VM Instance External IP Address: 34.46.250.126

### Installation
```bash
# Clone the repository
git clone https://github.com/masterpillow/campus-closet.git
cd campus-closet

# Create and activate virtual environment (Recommended)
python -m venv venv
source venv/bin/activate  # on Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python run.py




