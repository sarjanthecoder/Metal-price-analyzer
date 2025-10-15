🏆 MetalVault - Precious Metals & Jewelry Price Tracker
A stunning, real-time precious metals price tracking application with a modern UI and powerful Flask backend. Track live prices for Gold, Silver, Platinum, Palladium, and more with beautiful visualizations and instant updates.
Show Image
Show Image
Show Image
✨ Features
🎨 Frontend

Modern Dark Theme with luxury gold accents
Real-Time Price Updates every 60 seconds
Live Price Cards for multiple precious metals
Advanced Search with metal type, currency, and unit selection
Unit Converter (Troy Ounce, Gram, Kilogram, Tola)
Responsive Design works on all devices
Smooth Animations and glassmorphism effects
Professional UI/UX with intuitive navigation

⚙️ Backend

RESTful API built with Flask
Multiple Endpoints for price data
Smart Fallback with mock data when API unavailable
Error Handling and logging
Multi-Currency Support (USD, EUR, GBP, INR, JPY, AUD)
Unit Conversion API
Historical Data support

💎 Supported Metals

Gold (XAU) - The king of precious metals
Silver (XAG) - Industrial and investment metal
Platinum (XPT) - Rare and valuable
Palladium (XPD) - Automotive catalyst
Copper (XCU) - Industrial metal

📁 Project Structure
metalvault/
├── app.py                  # Flask backend application
├── templates/
│   └── index.html         # Main HTML frontend
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (create this)
├── .gitignore            # Git ignore file
└── README.md             # This file
🚀 Quick Start
Prerequisites

Python 3.8 or higher
pip package manager
GoldAPI.io API key (get free at goldapi.io)

Installation

Clone or download the repository

bashgit clone <your-repo-url>
cd metalvault

Create a virtual environment

bash# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate

Install dependencies

bashpip install -r requirements.txt

Set up environment variables

Create a .env file in the project root:
bashGOLD_API_KEY=your_api_key_here
Or set as environment variable:
bash# Windows
set GOLD_API_KEY=your_api_key_here

# Mac/Linux
export GOLD_API_KEY=your_api_key_here

Run the application

bashpython app.py

Open your browser

http://localhost:5000
🔑 Getting an API Key

Visit GoldAPI.io
Sign up for a free account
Get your API key from the dashboard
Add it to your .env file

Note: The application will work with mock data if no API key is provided, perfect for testing!