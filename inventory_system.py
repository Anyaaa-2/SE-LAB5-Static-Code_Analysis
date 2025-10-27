import json
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Global variable
stock_data={}

def addItem(item="default",qty=0,logs=None):
    """Add an item and its quantity to the stock."""
    if logs is None:
        logs=[]

    if not isinstance(item,str):
        logging.error("Invalid item name: must be a string")
        return

    if not isinstance(qty, int):
        logging.error("Invalid quantity: must be an integer")
        return

    # if not item:
    #     return
    logs.append(f"{datetime.now()}: Added {qty} of {item}")
    logging.info("Added %d units of %s", qty, item)

def removeItem(item, qty):
    """Safely remove quantity of an item."""
    try:
        stock_data[item]-=qty
        if stock_data[item]<=0:
            del stock_data[item]
        logging.info("Removed %d of %s", qty, item)

    except KeyError as e:
        logging.error("Item not found while removing: %s", e)
    except (ValueError, OSError) as e:
        logging.error("Unexpected error while removing item: %s", e)

def getQty(item):
    """Return quantity of an item."""
    try:
        return stock_data[item]
    except KeyError:
        logging.warning("Item '%s' not found in stock.", item)
        return 0

def loadData(file="inventory.json"):
    """Load stock data from a file safely."""
    #f = open(file, "r")
    global stock_data
    try:
        with open(file, "r", encoding="utf-8") as f:
            stock_data=json.load(f)
        logging.info("Data loaded from %s", file)
    except FileNotFoundError:
        logging.warning("%s not found. Starting with empty stock.", file)
        stock_data={}
    except json.JSONDecodeError as e:
        logging.error("Error decoding JSON from %s: %s", file, e)
        stock_data={}

def saveData(file="inventory.json"):
    """Save stock data to a file safely."""
    # f = open(file, "w")
    # f.write(json.dumps(stock_data))
    # f.close()
    try:
        with open(file, "w", encoding="utf-8") as f:
            json.dump(stock_data, f, indent=4)
        logging.info("Data saved to %s", file)
    except (OSError, PermissionError, IOError) as e:
        logging.error("Error saving data: %s", e)

def printData():
    """Print all stock data."""
    logging.info("Items Report:")
    #print("Items Report")
    for i in stock_data:
        print(f"{i} -> {stock_data[i]}")

def checkLowItems(threshold=5):
    """Return list of items below a given quantity threshold."""
    # result = []
    # for i in stock_data:
    #     if stock_data[i] < threshold:
    #         result.append(i)
    # return result
    result=[i for i in stock_data if stock_data[i] < threshold]
    return result

def main():
    """Main execution block."""
    addItem("apple", 10)
    addItem("banana", -2)
    addItem(123, "ten")  # invalid types, no check
    removeItem("apple", 3)
    removeItem("orange", 1)
    print("Apple stock:", getQty("apple"))
    print("Low items:", checkLowItems())
    saveData()
    loadData()
    printData()
    #eval("print('eval used')")  # dangerous

main()
