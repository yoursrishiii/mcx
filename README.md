<<<<<<< HEAD
# mcx
=======
# GoldSpread: MCX Gold Futures Cross-Contract Spread Desk 📈

A client-side commodity analytics dashboard that normalizes disparate MCX (Multi Commodity Exchange) gold futures contracts (GOLDM, GOLDTEN, GOLDGUINEA, GOLDPETAL) into a single, purity-adjusted ₹/gram basis and evaluates tradeable spreads against realistic transaction cost hurdles.

🔗 **Live Deployment:** [https://yoursrishiii.github.io/mcx/](https://yoursrishiii.github.io/mcx/)

---

## ⚡ Key Features

- **Purity-Adjusted Normalization:** Automatically adjusts 995-purity contracts (GOLDM) and 999-purity contracts (GOLDTEN, GOLDGUINEA, GOLDPETAL) to a unified ₹/gram of 999 gold.
- **Cost-Aware Signal Filter:** Evaluates cross-contract basis differences against statutory and market friction (brokerage, turnover charges, GST, stamp duty, and bid-ask slippage).
- **Data Hygiene Pipeline:** Client-side validation enforcing clean expiry dates, contract types, and outlier checks on MCX Bhavcopy closing data.
- **Walk-Forward Backtesting:** Multi-fold out-of-sample evaluation testing persistence of spread signals without lookahead bias.
- **Paper Trading Simulator:** Interactive virtual blotter allowing users to simulate cross-contract execution against authentic exchange settlement snapshots.

---

## 🛠 Tech Stack

- **Front End:** Semantic HTML5, Modern Responsive CSS
- **Analytical Engine:** Vanilla JavaScript (ES6+)
- **Charts & Visualization:** HTML5 Canvas API
- **Data Layer:** Structured MCX Bhavcopy settlement JSON (`data.json`)
- **Hosting & Version Control:** Git & GitHub Pages

---

## 🚀 How to Run Locally

To test and run this project from a clean clone:

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/yoursrishiii/mcx.git](https://github.com/yoursrishiii/mcx.git)
   cd mcx
>>>>>>> 19eaf84d27516cd4f5ed10b967d10a7e5298c9fa
