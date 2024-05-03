

# Sample bank transaction data (replace with your data import logic)
transactions = [
    {"amount": 100, "merchant": "Grocery Store"},
    {"amount": 50, "merchant": "Restaurant"},
    {"amount": 1500, "merchant": "Travel Agency", "is_recurring": True},  # Recurring transaction
    {"amount": 2000, "merchant": "Jewelry Store"},  # Potential anomaly
    {"amount": 200, "merchant": "Casino"} # Potential anomaly
]

def is_anomalous(transaction, params):
  amount_threshold = params["amount_threshold"]
  unusual_merchants = params["unusual_merchants"]
  return transaction["amount"] > amount_threshold and transaction["merchant"] in unusual_merchants and not transaction.get("is_recurring", False)

def analyze_transactions(transactions, params):
  """
  Analyzes transactions and identifies anomalies.
  """
  anomalies = []
  for transaction in transactions:
    if is_anomalous(transaction, params):
      anomalies.append(transaction)
  return anomalies
