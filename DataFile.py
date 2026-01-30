from faker import Faker
from datetime import datetime, timedelta
import random

fake = Faker('en_GB')


def generate_rhu_data(num_rhus=20):
    rhus = []
    for i in range(num_rhus):
        rhu = {
            'RHUID': f"RHU{1000 + i}",
            'Name': f"{random.choice(['Hope', 'Bridge', 'Pathway'])} Hostel",
            'Address': f"{random.randint(1, 99)} {fake.street_name()}, {fake.city()}",
            'Weekly Cost': random.randint(300, 600),
            'Available Beds': random.randint(1, 5)
        }
        rhus.append(rhu)
    return rhus


def generate_licensee_data(num_records=50):
    data = []

    for i in range(num_records):

        gender = random.choice(['Male', 'Female'])
        if gender == 'Male':
            first_name = fake.first_name_male()
        else:
            first_name = fake.first_name_female()

        risk = random.choice(['Low', 'Medium', 'High'])

        if risk == 'High':
            days_until_housing = random.randint(150, 300)
        else:
            days_until_housing = random.randint(30, 149)

        #makes the match for RHU
        matched_rhus = []
        for j in range(3):
            rhu = {
                'RHUID': f"RHU{1000 + j}",
                'Name': f"{random.choice(['Hope', 'Bridge', 'Pathway'])} Hostel",
                'Match Score': random.randint(60, 95),
                'Weekly Cost': random.randint(350, 550)
            }
            matched_rhus.append(rhu)

        #everything needed for licenses details
        license_details = {
            'LicenseID': f"LIC{10000 + i}",
            'SupervisingOfficer': fake.name(),
            'SupervisionLevel': risk,
            'Conditions': ['Regular reporting', 'Curfew'],
            'MatchedRHUs': matched_rhus,
            'AllocationPriority': random.randint(1, 100)
        }

        #gives a full record of details
        record = {
            'Name': f"{first_name} {fake.last_name()}",
            'Prisoner ID': f"PR{100000 + i}",
            'Gender': gender,
            'Age': random.randint(21, 65),
            'Risk Level': risk,
            'Days Until Housing': days_until_housing,
            'Current Location': random.choice(['Prison A', 'Prison B', 'Prison C']),
            'Offense Type': random.choice(['Burglary', 'Assault', 'Drug Offense']),
            'License Details': license_details
        }

        data.append(record)

    return data


def get_data_for_tables(data):
    names = [record['Name'] for record in data]
    prisoner_ids = [record['Prisoner ID'] for record in data]
    risk_levels = [record['Risk Level'] for record in data]
    days_list = [str(record['Days Until Housing']) for record in data]

    return {
        'names': names,
        'prisoner_ids': prisoner_ids,
        'risk_levels': risk_levels,
        'days_until_housing': days_list
    }


def get_filtered_data(data, risk_filter=None):
    if not risk_filter:
        return data

    filtered = []
    for record in data:
        if record['Risk Level'] == risk_filter:
            filtered.append(record)

    return filtered


def save_data(data, filename='prisoner_data.json'):
    import json
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Saved {len(data)} records")
    return data


def load_data(filename='prisoner_data.json'):
    import json
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
        print(f"Loaded {len(data)} records")
        return data
    except:
        print("File not found, generating new data")
        return generate_licensee_data(20)


