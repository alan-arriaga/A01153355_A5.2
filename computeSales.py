import sys
import json
import time

def load_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Error reading JSON file '{file_path}': {e}")
        return {}

def compute_total_sales(price_catalogue, sales_record):
    total_cost = 0.0
    errors = []

    for sale in sales_record:
        try:
            product_id = sale.get("product_id")
            quantity = float(sale.get("quantity", 0))

            if product_id not in price_catalogue:
                errors.append(f"Product ID '{product_id}' not found in price catalogue.")
                continue

            price_per_unit = float(price_catalogue[product_id])
            total_cost += price_per_unit * quantity

        except (ValueError, TypeError) as e:
            errors.append(f"Error processing sale record {sale}: {e}")

    return total_cost, errors

def save_results_to_file(total_cost, errors, elapsed_time, output_file="SalesResults.txt"):
    with open(output_file, 'w') as file:
        file.write("Sales Calculation Results\n")
        file.write(f"Total Sales Cost: ${total_cost:.2f}\n")
        file.write(f"Execution Time: {elapsed_time:.4f} seconds\n\n")
        if errors:
            file.write("Errors:\n")
            for error in errors:
                file.write(f"- {error}\n")

def main():
    if len(sys.argv) != 3:
        print("Usage: python computeSales.py priceCatalogue.json salesRecord.json")
        sys.exit(1)

    price_catalogue_file = sys.argv[1]
    sales_record_file = sys.argv[2]

    start_time = time.time()

    price_catalogue = load_json_file(price_catalogue_file)
    sales_record = load_json_file(sales_record_file)

    total_cost, errors = compute_total_sales(price_catalogue, sales_record)

    elapsed_time = time.time() - start_time

    print("\nSales Calculation Results")
    print(f"Total Sales Cost: ${total_cost:.2f}")
    print(f"Execution Time: {elapsed_time:.4f} seconds")

    if errors:
        print("\nErrors:")
        for error in errors:
            print(f"- {error}")

    save_results_to_file(total_cost, errors, elapsed_time)
    print(f"\nResults have been saved to 'SalesResults.txt'.")

if __name__ == "__main__":
    main()