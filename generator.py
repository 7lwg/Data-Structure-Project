import csv
import os
from faker import Faker
import random

# Initialize Faker with Egyptian locale for realistic names/addresses
fake = Faker('ar_EG') 

def generate_etl_data(file_path="data/transactions.csv", num_rows=10000):
    # Ensure the data directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    # Pre-defined Egyptian branch locations
    branches = ["Cairo - Nasr City", "Alexandria - Smouha", "Giza - Dokki", "Port Said - Port Fuad", "Suez - Port Tawfik"]
    categories = ["Electronics", "Groceries", "Home Appliances", "Fashion", "Toys"]

    print(f"Generating {num_rows} rows of realistic data...")

    with open(file_path, mode='w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        # Header row
        writer.writerow(["TransactionID", "CustomerName", "Category", "Amount", "Branch", "Date", "Status"])

        for _ in range(num_rows):
            writer.writerow([
                fake.unique.random_int(min=100000, max=999999), # Unique ID for indexing
                fake.name(),                                    # Realistic names
                random.choice(categories),                      # Category
                round(random.uniform(10.5, 15000.0), 2),        # Random prices
                random.choice(branches),                        # Egyptian branches
                fake.date_between(start_date='-1y', end_date='today'), # Dates within last year
                random.choice(["Success", "Pending", "Failed"]) # Transaction status
            ])

    print(f"Successfully created {file_path}")

if __name__ == "__main__":
    generate_etl_data()