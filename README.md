# 💱 Currency Converter

A modern, web-based currency converter with real-time exchange rates and a beautiful UI.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

- **Real-time exchange rates** — Fetches live rates from ExchangeRate API
- **60+ currencies** — All major world currencies supported
- **Modern UI** — Clean gradient design with smooth animations
- **Swap currencies** — One-click to flip conversion direction
- **Copy to clipboard** — Easily copy results
- **Smart caching** — Reduces API calls with 10-minute cache
- **Mobile responsive** — Works great on any device
- **Keyboard support** — Press Enter to convert

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone or download** this repository:
   ```bash
   git clone https://github.com/yourusername/currency-converter.git
   cd currency-converter
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install flask requests
   ```

4. **Run the app**:
   ```bash
   python currency_converter_web.py
   ```

5. **Open your browser** and go to:
   ```
   http://localhost:5000
   ```

## 📸 Screenshot

The app features a modern dark gradient background with a clean white card interface:

- Dropdown selectors for "From" and "To" currencies
- Swap button to quickly reverse conversion
- Amount input field
- Convert button with hover effects
- Result display with copy functionality

## 🛠️ Tech Stack

- **Backend**: Python, Flask
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **API**: [ExchangeRate-API](https://www.exchangerate-api.com/)
- **Fonts**: Inter (Google Fonts)

## 📁 Project Structure

```
currency-converter/
├── currency_converter_web.py   # Main application
├── README.md                   # This file
└── venv/                       # Virtual environment (created by you)
```

## 🔧 Configuration

### Change the port

Edit the last line of `currency_converter_web.py`:

```python
app.run(debug=True, port=8080)  # Change 5000 to any port
```

### Add more currencies

Add entries to the `CURRENCY_NAMES` dictionary:

```python
CURRENCY_NAMES = {
    # ... existing currencies ...
    "XYZ": "New Currency Name",
}
```

### Adjust cache duration

Change the TTL (time-to-live) in the cache config:

```python
cache = {"data": None, "timestamp": None, "ttl": timedelta(minutes=30)}  # 30 min cache
```

## 🌐 API Reference

The app uses the free [ExchangeRate-API](https://www.exchangerate-api.com/):

- **Endpoint**: `https://api.exchangerate-api.com/v4/latest/{base}`
- **Rate limit**: 1,500 requests/month (free tier)
- **Update frequency**: Daily

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [ExchangeRate-API](https://www.exchangerate-api.com/) for free exchange rates
- [Inter Font](https://fonts.google.com/specimen/Inter) by Rasmus Andersson
- [Flask](https://flask.palletsprojects.com/) for the web framework

---

Made with ❤️ by Ibrahim Mirza
