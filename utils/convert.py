import os
import sys
import django
import pandas as pd

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Add the parent directory to the Python path
sys.path.append(os.path.join(current_dir, ".."))  # Adjust as necessary

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cooking_uts.settings")

# Initialize Django
django.setup()

from api.restaurant.models import Restaurant, Food, Menu


def sanitize_value(cell):
    """Convert snake case to a capitalized title."""
    if isinstance(cell, (int, float)):
        return cell
    return (
        cell.title()
        if str(cell).split("_").__len__() <= 1
        else " ".join(word.capitalize() for word in cell.split("_"))
    )


def sanitize_row(row):
    """Sanitize the row keys and return a sanitized dictionary."""
    sanitized_data = {}
    for key, value in row.items():
        if key == "Harga" or key == "Foto":
            sanitized_data[key] = value
            continue
        sanitized_data[key] = sanitize_value(value)
    return sanitized_data


# Read the Excel file
file_path = os.path.join(current_dir, "./data.xlsx")  # Adjust the path accordingly
df = pd.read_excel(file_path)

# Loop through the rows and save the data
for index, row in df.iterrows():
    # Sanitize the row
    sanitized_row = sanitize_row(row)

    # Create or get the restaurant
    restaurant, created = Restaurant.objects.get_or_create(
        name=sanitized_row["Nama Restoran"],
        district=sanitized_row["Kecamatan"],
        address=sanitized_row["Alamat"],
        operational_hours=sanitized_row["Jam Operasional"],
        photo_url=sanitized_row["Foto"],
    )

    # Split food names, types, and prices
    food_names = sanitized_row["Nama Makanan"].split(", ")
    food_type = sanitized_row["Jenis Makanan"].split(", ")[0].strip()
    price_string = str(sanitized_row["Harga"]).split(", ")
    prices = (
        price_string[0]
        if price_string.__len__() <= 1
        else " - ".join(sorted(price_string, reverse=True))
    )

    for i in range (len(food_type)):
        # if the menu category already exists, get it, otherwise create it
        Menu.objects.get_or_create(
            restaurant=restaurant,
            category=food_type[i].strip(),
        )
    for i in range(len(food_names)):
        # Create food item
        Food.objects.get_or_create(
            restaurant=restaurant,
            menu=Menu.objects.get(restaurant=restaurant, category=food_type[i].strip()),
            name=food_names[i].strip(),
            price=prices,
        )
        
    print(f'Row {index} done!')

print("Data successfully imported!")
