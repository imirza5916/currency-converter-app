from flask import Flask, render_template_string, jsonify, request
import requests
from datetime import datetime, timedelta

app = Flask(__name__)

# Cache for exchange rates
cache = {"data": None, "timestamp": None, "ttl": timedelta(minutes=10)}

CURRENCY_NAMES = {
    # A
    "AED": "UAE Dirham",
    "AFN": "Afghan Afghani",
    "ALL": "Albanian Lek",
    "AMD": "Armenian Dram",
    "ANG": "Netherlands Antillean Guilder",
    "AOA": "Angolan Kwanza",
    "ARS": "Argentine Peso",
    "AUD": "Australian Dollar",
    "AWG": "Aruban Florin",
    "AZN": "Azerbaijani Manat",
    
    # B
    "BAM": "Bosnia-Herzegovina Convertible Mark",
    "BBD": "Barbadian Dollar",
    "BDT": "Bangladeshi Taka",
    "BGN": "Bulgarian Lev",
    "BHD": "Bahraini Dinar",
    "BIF": "Burundian Franc",
    "BMD": "Bermudan Dollar",
    "BND": "Brunei Dollar",
    "BOB": "Bolivian Boliviano",
    "BRL": "Brazilian Real",
    "BSD": "Bahamian Dollar",
    "BTN": "Bhutanese Ngultrum",
    "BWP": "Botswanan Pula",
    "BYN": "Belarusian Ruble",
    "BZD": "Belize Dollar",
    
    # C
    "CAD": "Canadian Dollar",
    "CDF": "Congolese Franc",
    "CHF": "Swiss Franc",
    "CLP": "Chilean Peso",
    "CNY": "Chinese Yuan",
    "COP": "Colombian Peso",
    "CRC": "Costa Rican Colón",
    "CUP": "Cuban Peso",
    "CVE": "Cape Verdean Escudo",
    "CZK": "Czech Koruna",
    
    # D
    "DJF": "Djiboutian Franc",
    "DKK": "Danish Krone",
    "DOP": "Dominican Peso",
    "DZD": "Algerian Dinar",
    
    # E
    "EGP": "Egyptian Pound",
    "ERN": "Eritrean Nakfa",
    "ETB": "Ethiopian Birr",
    "EUR": "Euro",
    
    # F
    "FJD": "Fijian Dollar",
    "FKP": "Falkland Islands Pound",
    "FOK": "Faroese Króna",
    
    # G
    "GBP": "British Pound",
    "GEL": "Georgian Lari",
    "GGP": "Guernsey Pound",
    "GHS": "Ghanaian Cedi",
    "GIP": "Gibraltar Pound",
    "GMD": "Gambian Dalasi",
    "GNF": "Guinean Franc",
    "GTQ": "Guatemalan Quetzal",
    "GYD": "Guyanaese Dollar",
    
    # H
    "HKD": "Hong Kong Dollar",
    "HNL": "Honduran Lempira",
    "HRK": "Croatian Kuna",
    "HTG": "Haitian Gourde",
    "HUF": "Hungarian Forint",
    
    # I
    "IDR": "Indonesian Rupiah",
    "ILS": "Israeli New Shekel",
    "IMP": "Isle of Man Pound",
    "INR": "Indian Rupee",
    "IQD": "Iraqi Dinar",
    "IRR": "Iranian Rial",
    "ISK": "Icelandic Króna",
    
    # J
    "JEP": "Jersey Pound",
    "JMD": "Jamaican Dollar",
    "JOD": "Jordanian Dinar",
    "JPY": "Japanese Yen",
    
    # K
    "KES": "Kenyan Shilling",
    "KGS": "Kyrgystani Som",
    "KHR": "Cambodian Riel",
    "KID": "Kiribati Dollar",
    "KMF": "Comorian Franc",
    "KRW": "South Korean Won",
    "KWD": "Kuwaiti Dinar",
    "KYD": "Cayman Islands Dollar",
    "KZT": "Kazakhstani Tenge",
    
    # L
    "LAK": "Laotian Kip",
    "LBP": "Lebanese Pound",
    "LKR": "Sri Lankan Rupee",
    "LRD": "Liberian Dollar",
    "LSL": "Lesotho Loti",
    "LYD": "Libyan Dinar",
    
    # M
    "MAD": "Moroccan Dirham",
    "MDL": "Moldovan Leu",
    "MGA": "Malagasy Ariary",
    "MKD": "Macedonian Denar",
    "MMK": "Myanmar Kyat",
    "MNT": "Mongolian Tugrik",
    "MOP": "Macanese Pataca",
    "MRU": "Mauritanian Ouguiya",
    "MUR": "Mauritian Rupee",
    "MVR": "Maldivian Rufiyaa",
    "MWK": "Malawian Kwacha",
    "MXN": "Mexican Peso",
    "MYR": "Malaysian Ringgit",
    "MZN": "Mozambican Metical",
    
    # N
    "NAD": "Namibian Dollar",
    "NGN": "Nigerian Naira",
    "NIO": "Nicaraguan Córdoba",
    "NOK": "Norwegian Krone",
    "NPR": "Nepalese Rupee",
    "NZD": "New Zealand Dollar",
    
    # O
    "OMR": "Omani Rial",
    
    # P
    "PAB": "Panamanian Balboa",
    "PEN": "Peruvian Sol",
    "PGK": "Papua New Guinean Kina",
    "PHP": "Philippine Peso",
    "PKR": "Pakistani Rupee",
    "PLN": "Polish Zloty",
    "PYG": "Paraguayan Guarani",
    
    # Q
    "QAR": "Qatari Riyal",
    
    # R
    "RON": "Romanian Leu",
    "RSD": "Serbian Dinar",
    "RUB": "Russian Ruble",
    "RWF": "Rwandan Franc",
    
    # S
    "SAR": "Saudi Riyal",
    "SBD": "Solomon Islands Dollar",
    "SCR": "Seychellois Rupee",
    "SDG": "Sudanese Pound",
    "SEK": "Swedish Krona",
    "SGD": "Singapore Dollar",
    "SHP": "Saint Helena Pound",
    "SLE": "Sierra Leonean Leone",
    "SOS": "Somali Shilling",
    "SRD": "Surinamese Dollar",
    "SSP": "South Sudanese Pound",
    "STN": "São Tomé and Príncipe Dobra",
    "SYP": "Syrian Pound",
    "SZL": "Swazi Lilangeni",
    
    # T
    "THB": "Thai Baht",
    "TJS": "Tajikistani Somoni",
    "TMT": "Turkmenistani Manat",
    "TND": "Tunisian Dinar",
    "TOP": "Tongan Paʻanga",
    "TRY": "Turkish Lira",
    "TTD": "Trinidad & Tobago Dollar",
    "TVD": "Tuvaluan Dollar",
    "TWD": "New Taiwan Dollar",
    "TZS": "Tanzanian Shilling",
    
    # U
    "UAH": "Ukrainian Hryvnia",
    "UGX": "Ugandan Shilling",
    "USD": "US Dollar",
    "UYU": "Uruguayan Peso",
    "UZS": "Uzbekistani Som",
    
    # V
    "VES": "Venezuelan Bolívar",
    "VND": "Vietnamese Dong",
    "VUV": "Vanuatu Vatu",
    
    # W
    "WST": "Samoan Tala",
    
    # X
    "XAF": "Central African CFA Franc",
    "XCD": "East Caribbean Dollar",
    "XDR": "Special Drawing Rights",
    "XOF": "West African CFA Franc",
    "XPF": "CFP Franc",
    
    # Y
    "YER": "Yemeni Rial",
    
    # Z
    "ZAR": "South African Rand",
    "ZMW": "Zambian Kwacha",
    "ZWL": "Zimbabwean Dollar",
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Currency Converter</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        
        .container {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 24px;
            padding: 40px;
            width: 100%;
            max-width: 440px;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.4);
        }
        
        .header {
            text-align: center;
            margin-bottom: 32px;
        }
        
        .header h1 {
            font-size: 28px;
            font-weight: 700;
            color: #1a1a2e;
            margin-bottom: 8px;
        }
        
        .header p {
            color: #666;
            font-size: 14px;
        }
        
        .input-group {
            margin-bottom: 20px;
        }
        
        .input-group label {
            display: block;
            font-size: 13px;
            font-weight: 600;
            color: #444;
            margin-bottom: 8px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .currency-select, .amount-input {
            width: 100%;
            padding: 16px;
            border: 2px solid #e0e0e0;
            border-radius: 12px;
            font-size: 16px;
            font-family: inherit;
            transition: all 0.2s ease;
            background: white;
        }
        
        .currency-select:focus, .amount-input:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1);
        }
        
        .swap-btn {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 48px;
            height: 48px;
            margin: 0 auto 20px;
            background: #f0f0f0;
            border: none;
            border-radius: 50%;
            cursor: pointer;
            transition: all 0.2s ease;
            font-size: 20px;
        }
        
        .swap-btn:hover {
            background: #667eea;
            color: white;
            transform: rotate(180deg);
        }
        
        .convert-btn {
            width: 100%;
            padding: 18px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
            margin-top: 8px;
        }
        
        .convert-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
        }
        
        .convert-btn:active {
            transform: translateY(0);
        }
        
        .result {
            margin-top: 28px;
            padding: 24px;
            background: linear-gradient(135deg, #f5f7fa 0%, #e4e8eb 100%);
            border-radius: 16px;
            text-align: center;
            display: none;
        }
        
        .result.show {
            display: block;
            animation: slideUp 0.3s ease;
        }
        
        @keyframes slideUp {
            from {
                opacity: 0;
                transform: translateY(10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .result-amount {
            font-size: 32px;
            font-weight: 700;
            color: #1a1a2e;
            margin-bottom: 8px;
        }
        
        .result-details {
            color: #666;
            font-size: 14px;
            margin-bottom: 16px;
        }
        
        .copy-btn {
            padding: 10px 20px;
            background: white;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s ease;
        }
        
        .copy-btn:hover {
            border-color: #667eea;
            color: #667eea;
        }
        
        .copy-btn.copied {
            background: #10b981;
            border-color: #10b981;
            color: white;
        }
        
        .rate-info {
            margin-top: 12px;
            font-size: 12px;
            color: #888;
        }
        
        .error {
            color: #ef4444;
            background: #fef2f2;
            padding: 12px;
            border-radius: 8px;
            margin-top: 16px;
            font-size: 14px;
        }
        
        /* Searchable select styling */
        .select-wrapper {
            position: relative;
        }
        
        .currency-select {
            cursor: pointer;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>💱 Currency Converter</h1>
            <p>Real-time exchange rates</p>
        </div>
        
        <div class="input-group">
            <label>From</label>
            <select class="currency-select" id="fromCurrency">
                {% for code, name in currencies %}
                <option value="{{ code }}" {% if code == 'USD' %}selected{% endif %}>{{ name }} ({{ code }})</option>
                {% endfor %}
            </select>
        </div>
        
        <button class="swap-btn" onclick="swapCurrencies()" title="Swap currencies">⇅</button>
        
        <div class="input-group">
            <label>To</label>
            <select class="currency-select" id="toCurrency">
                {% for code, name in currencies %}
                <option value="{{ code }}" {% if code == 'EUR' %}selected{% endif %}>{{ name }} ({{ code }})</option>
                {% endfor %}
            </select>
        </div>
        
        <div class="input-group">
            <label>Amount</label>
            <input type="text" class="amount-input" id="amount" value="1.00" 
                   oninput="this.value = this.value.replace(/[^0-9.,]/g, '')">
        </div>
        
        <button class="convert-btn" onclick="convert()">Convert</button>
        
        <div class="result" id="result">
            <div class="result-amount" id="resultAmount"></div>
            <div class="result-details" id="resultDetails"></div>
            <button class="copy-btn" onclick="copyResult()">📋 Copy</button>
            <div class="rate-info" id="rateInfo"></div>
        </div>
        
        <div class="error" id="error" style="display: none;"></div>
    </div>
    
    <script>
        // Allow Enter key to convert
        document.getElementById('amount').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') convert();
        });
        
        function swapCurrencies() {
            const from = document.getElementById('fromCurrency');
            const to = document.getElementById('toCurrency');
            const temp = from.value;
            from.value = to.value;
            to.value = temp;
        }
        
        async function convert() {
            const from = document.getElementById('fromCurrency').value;
            const to = document.getElementById('toCurrency').value;
            const amount = parseFloat(document.getElementById('amount').value.replace(/,/g, ''));
            
            if (isNaN(amount) || amount <= 0) {
                showError('Please enter a valid amount');
                return;
            }
            
            try {
                const response = await fetch(`/convert?from=${from}&to=${to}&amount=${amount}`);
                const data = await response.json();
                
                if (data.error) {
                    showError(data.error);
                    return;
                }
                
                document.getElementById('error').style.display = 'none';
                document.getElementById('resultAmount').textContent = 
                    `${formatNumber(data.result)} ${to}`;
                document.getElementById('resultDetails').textContent = 
                    `${formatNumber(amount)} ${from} =`;
                document.getElementById('rateInfo').textContent = 
                    `1 ${from} = ${data.rate.toFixed(4)} ${to}`;
                document.getElementById('result').classList.add('show');
                
            } catch (err) {
                showError('Connection error. Please try again.');
            }
        }
        
        function formatNumber(num) {
            if (num >= 1000) {
                return num.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
            } else if (num >= 1) {
                return num.toFixed(2);
            } else {
                return num.toFixed(4);
            }
        }
        
        function showError(message) {
            document.getElementById('error').textContent = message;
            document.getElementById('error').style.display = 'block';
            document.getElementById('result').classList.remove('show');
        }
        
        function copyResult() {
            const amount = document.getElementById('resultDetails').textContent;
            const result = document.getElementById('resultAmount').textContent;
            navigator.clipboard.writeText(`${amount} ${result}`);
            
            const btn = document.querySelector('.copy-btn');
            btn.textContent = '✓ Copied!';
            btn.classList.add('copied');
            setTimeout(() => {
                btn.textContent = '📋 Copy';
                btn.classList.remove('copied');
            }, 2000);
        }
    </script>
</body>
</html>
"""

def get_rates(base="USD"):
    """Fetch exchange rates with caching."""
    now = datetime.now()
    
    if cache["data"] and cache["timestamp"]:
        if now - cache["timestamp"] < cache["ttl"]:
            return cache["data"]
    
    try:
        response = requests.get(
            f"https://api.exchangerate-api.com/v4/latest/{base}",
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        cache["data"] = data["rates"]
        cache["timestamp"] = now
        return data["rates"]
    except requests.RequestException as e:
        if cache["data"]:
            return cache["data"]
        raise e

@app.route("/")
def index():
    currencies = sorted(CURRENCY_NAMES.items(), key=lambda x: x[1])
    return render_template_string(HTML_TEMPLATE, currencies=currencies)

@app.route("/convert")
def convert():
    from_currency = request.args.get("from", "USD")
    to_currency = request.args.get("to", "EUR")
    amount = float(request.args.get("amount", 1))
    
    try:
        rates = get_rates(from_currency)
        rate = rates.get(to_currency)
        
        if rate is None:
            return jsonify({"error": f"Unknown currency: {to_currency}"})
        
        result = amount * rate
        return jsonify({
            "result": result,
            "rate": rate,
            "from": from_currency,
            "to": to_currency
        })
        
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    print("\n🚀 Currency Converter running at: http://localhost:5000\n")
    app.run(debug=True, port=5000)
