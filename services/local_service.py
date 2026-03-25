import csv
import os

def save_to_local_csv(data, file_name):
    file_exists = os.path.isfile(file_name)

    with open(file_name, mode='a', newline='') as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(["Name", "Email", "Phone"])

        writer.writerow([data['name'], data['email'], data['phone']])