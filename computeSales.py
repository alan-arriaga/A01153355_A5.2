import json
import sys
import time
from pathlib import Path

RESULT_FILE = "SalesResults.txt"


def load_json_file(file_path):
    """
    Loads and returns data from a JSON file.
    """
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in '{file_path}'.")
        sys.exit(1)


def compute_total_sales(prices, sales):
    """
    Computes total sales and handles missing products gracefully.
    """
    price_lookup = {item['title']: item['price'] for item in prices}
    total_cost = 0.0
    errors = []

    for sale in sales:
        product = sale.get("Product")
        quantity = sale.get("Quantity", 0)

        if product in price_lookup:
            total_cost += price_lookup[product] * quantity
        else:
            errors.append(f"Warning: Product '{product}' not found in price catalogue.")

    return total_cost, errors


def write_results_to_file(total_cost, errors, execution_time):
    """
    Writes results to a file in a human-readable format.
    """
    with open(RESULT_FILE, 'w') as file:
        file.write("Sales Results\n")
        file.write("=" * 30 + "\n")
        file.write(f"Total Sales Cost: ${total_cost:.2f}\n")
        file.write("\n")
        if errors:
            file.write("Errors:\n")
            for error in errors:
                file.write(f"{error}\n")
        file.write("\n")
        file.write(f"Execution Time: {execution_time:.2f} seconds\n")


def main():
    """
    Main program entry point.
    """
    # Ensure correct number of arguments
    if len(sys.argv) != 3:
        print("Usage: python computeSales.py <priceCatalogue.json> <salesRecord.json>")
        sys.exit(1)

    # Load input files
    price_catalogue_file = sys.argv[1]
    sales_record_file = sys.argv[2]

    # Start timing execution
    start_time = time.time()

    prices = load_json_file(price_catalogue_file)
    sales = load_json_file(sales_record_file)

    # Compute total sales cost
    total_cost, errors = compute_total_sales(prices, sales)

    # End timing
    execution_time = time.time() - start_time

    # Display results to console
    print("Sales Results")
    print("=" * 30)
    print(f"Total Sales Cost: ${total_cost:.2f}")
    print()
    if errors:
        print("Errors:")
        for error in errors:
            print(error)
    print()
    print(f"Execution Time: {execution_time:.2f} seconds")

    # Write results to file
    write_results_to_file(total_cost, errors, execution_time)


if __name__ == "__main__":
    main()