import csv
from operator import itemgetter
from datetime import datetime, timedelta


def get_closest_friday_5pm(timestamp, is_dst=False):
    """
    Get the closest Friday at 5 PM before and after the given timestamp.

    Args:
        @:param (datetime): The timestamp to calculate the closest Fridays.
        @:param (bool): Whether the timestamp is in DST (Daylight Saving Time) or not.

    Returns:
        @:return: A tuple containing the closest Friday before and after the given timestamp.
    """

    # Get the weekday of the given timestamp
    weekday = timestamp.weekday()

    # Calculate the number of days passed since the last Friday
    if weekday < 4:
        days_since_friday = weekday + 3
    elif weekday == 4:
        # Depends on the time, whether before or after 17:00
        if timestamp.hour < (17 + int(is_dst)):
            days_since_friday = 7
        else:
            days_since_friday = 0
    else:
        days_since_friday = weekday - 4

    # Subtract the days to get the closest Friday
    closest_friday_before = timestamp - timedelta(days=days_since_friday)
    closest_friday_before = datetime(
        closest_friday_before.year,
        closest_friday_before.month,
        closest_friday_before.day,
        17 + int(is_dst), 0  # 17:00 or 18:00 depending on DST
    )

    # Add 7 days to get the closest Friday after
    closest_friday_after = closest_friday_before + timedelta(days=7)

    return closest_friday_before, closest_friday_after


def get_closest_saturday_8pm(timestamp, is_dst=False):
    """
    Get the closest Saturday at 8 PM before and after the given timestamp.

    Args:
        @:param (datetime): The timestamp to calculate the closest Saturdays.
        @:param (bool): Whether the timestamp is in DST (Daylight Saving Time) or not.

    Returns:
        @:return: A tuple containing the closest Saturday before and after the given timestamp.
    """

    # Get the weekday of the given timestamp
    weekday = timestamp.weekday()

    # Calculate the number of days passed since the last Saturday
    if weekday < 5:
        days_since_saturday = weekday + 2
    elif weekday == 5:
        # Depends on the time, whether before or after 20:00
        if timestamp.hour < (20 + int(is_dst)):
            days_since_saturday = 7
        else:
            days_since_saturday = 0
    else:
        days_since_saturday = weekday - 5

    # Subtract the days to get the closest Saturday
    closest_saturday_before = timestamp - timedelta(days=days_since_saturday)
    closest_saturday_before = datetime(
        closest_saturday_before.year,
        closest_saturday_before.month,
        closest_saturday_before.day,
        20 + int(is_dst), 0  # 20:00 or 21:00 depending on DST
    )

    # Add 7 days to get the closest Saturday after
    closest_saturday_after = closest_saturday_before + timedelta(days=7)

    return closest_saturday_before, closest_saturday_after


def calculate_sabbatical_duration(takeoff_date, takeoff_time, landing_date, landing_time, is_dst=False):
    """
    Calculates the duration of a sabbatical trip in hours.

    Args:
        @:param takeoff_date (str): The date of takeoff in the format "YYYY-MM-DD".
        @:param takeoff_time (str): The time of takeoff in the format "HH:MM".
        @:param landing_date (str): The date of landing in the format "YYYY-MM-DD".
        @:param landing_time (str): The time of landing in the format "HH:MM".
        @:param is_dst (bool, optional): Whether daylight saving time is in effect. Defaults to False.

    Returns:
        @:return The duration of the sabbatical trip in hours.
    """

    # Convert takeoff and landing timestamps to datetime objects
    takeoff_timestamp = datetime.strptime(takeoff_date + " " + takeoff_time, "%Y-%m-%d %H:%M")
    landing_timestamp = datetime.strptime(landing_date + " " + landing_time, "%Y-%m-%d %H:%M")

    # Get the closest Friday 5 PM before and after takeoff
    friday_5pm_before_takeoff, friday_5pm_after_takeoff = get_closest_friday_5pm(takeoff_timestamp, is_dst)

    # Get the closest Saturday 8 PM before and after takeoff
    saturday_8pm_before_takeoff, saturday_8pm_after_takeoff = get_closest_saturday_8pm(takeoff_timestamp, is_dst)

    # Check if the takeoff is during the sabbatical period
    is_sabbatical_takeoff = (saturday_8pm_after_takeoff - friday_5pm_before_takeoff).days < 2

    if is_sabbatical_takeoff:
        if landing_timestamp <= saturday_8pm_after_takeoff:
            # Landed during the sabbatical
            sabbatical_duration = landing_timestamp - takeoff_timestamp
        else:
            # Landed after the sabbatical
            sabbatical_duration = saturday_8pm_after_takeoff - takeoff_timestamp
    else:
        if landing_timestamp <= friday_5pm_after_takeoff:
            # Landed before the sabbatical
            sabbatical_duration = timedelta(0)
        elif landing_timestamp <= saturday_8pm_after_takeoff:
            # Landed during the sabbatical
            sabbatical_duration = landing_timestamp - friday_5pm_after_takeoff
        else:
            # Landed after the sabbatical (unlikely scenario)
            sabbatical_duration = saturday_8pm_after_takeoff - friday_5pm_after_takeoff

    # Convert the duration to hours
    sabbatical_duration_hours = sabbatical_duration.total_seconds() / 3600

    return sabbatical_duration_hours


def enter_flight_details():
    """
    Records flight details provided by the user and updates the flight_data.csv file.
    Prompts the user to enter various flight details such as takeoff date, takeoff time,
    takeoff airport, landing date, landing time, landing airport, mission (pilot/passenger),
    and any additional notes. Then, the function reads the existing flight data from the
    flight_data.csv file, adds the new flight details, sorts the flights by takeoff date and
    time, and writes the updated data back to the CSV file.

    @:returns: None
    """

    # Prompt user for flight details
    takeoff_date = input("Enter takeoff date (YYYY-MM-DD): ")
    takeoff_time = input("Enter takeoff time (HH:MM): ")
    takeoff_airport = input("Enter takeoff airport: ")
    landing_date = input("Enter landing date (YYYY-MM-DD): ")
    landing_time = input("Enter landing time (HH:MM): ")
    landing_airport = input("Enter landing airport: ")
    mission = input("Were you a pilot or a passenger? ")
    notes = input("Enter any notes: ")

    # Read the existing flight data from the CSV file
    with open(r"flight_data.csv", 'r') as file:
        reader = csv.DictReader(file)
        data = list(reader)

    # Create a dictionary for the new flight details
    new_flight = {
        'takeoff_date': takeoff_date,
        'takeoff_time': takeoff_time,
        'takeoff_airport': takeoff_airport,
        'landing_date': landing_date,
        'landing_time': landing_time,
        'landing_airport': landing_airport,
        'mission': mission,
        'notes': notes
    }

    # Add the new flight details to the existing flight data
    data.append(new_flight)

    # Sort the flight data by takeoff date and time
    sorted_data = sorted(data, key=lambda x: (x['takeoff_date'], x['takeoff_time']))

    # Write the sorted data back to the CSV file
    with open(r"flight_data.csv", 'w', newline='') as file:
        fieldnames = sorted_data[0].keys()
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(sorted_data)

    print("Flight details successfully recorded!")


# Function to generate a report of flights and payment details
def generate_report():
    ESHEL_FACTOR = 3  # [USD/hour]
    FLIGHT_HOURS_PAYMENT = 100  # [USD/hour]
    SABBATICAL_FACTOR = 1.5  # [-]
    total_flight_time = 0  # [hours]
    total_sabbatical_time = 0  # [hours]
    total_abroad_time = 0  # [hours]

    # Get the current date and the first day of the current month
    current_date = datetime.now()
    first_day_of_month = current_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    # Filter flights that occurred in the last month
    flights_last_month = []
    with open('flight_data.csv', 'r') as file:
        reader = csv.reader(file)
        flights = list(reader)

        # Assume that the flights are sorted by takeoff date and time
        for flight in flights[1:]:  # Skip the header row
            takeoff_date, takeoff_time, _, _, _, _, mission, _ = flight

            takeoff_timestamp = datetime.strptime(takeoff_date + " " + takeoff_time, "%Y-%m-%d %H:%M")

            # Check if the flight occurred in the last month
            if takeoff_timestamp < first_day_of_month:  # Flight occurred before the last month
                prev_month_last_flight_details = flight
            else:
                flights_last_month.append(flight)

    # Calculate the total payment for the last month's flights
    for i, flight in enumerate(flights_last_month):
        takeoff_date, takeoff_time, takeoff_airport, landing_date, landing_time, landing_airport, mission, _ = flight
        takeoff_timestamp = datetime.strptime(takeoff_date + " " + takeoff_time, "%Y-%m-%d %H:%M")
        landing_timestamp = datetime.strptime(landing_date + " " + landing_time, "%Y-%m-%d %H:%M")
        if i >= 1:
            prev_month_last_flight_details = flights_last_month[i - 1]
        _, _, _, prev_landing_date, prev_landing_time, prev_landing_airport, _, _ = prev_month_last_flight_details
        prev_landing_timestamp = datetime.strptime(prev_landing_date + " " + prev_landing_time, "%Y-%m-%d %H:%M")

        """If the pilot stayed abroad, that is, the landing airport of the previous flight is not LLBG (Ben-Gurion),
        calculate the staying duration (the difference between the takeoff time of the current flight and the landing
        time of the previous flight) and multiply by a factor"""
        if (prev_landing_airport != "LLBG") and (takeoff_airport != "LLBG"):
            abroad_duration = calculate_duration(prev_landing_date, prev_landing_time, takeoff_date, takeoff_time)
            total_abroad_time += abroad_duration

        # If the pilot was a passenger, skip the calculation of the flight duration
        if mission != "pilot":
            continue

        # Calculate the flight duration and the sabbatical duration
        flight_duration = calculate_duration(takeoff_date, takeoff_time, landing_date, landing_time)
        sabbatical_duration = calculate_sabbatical_duration(takeoff_date, takeoff_time, landing_date, landing_time)

        # Add the flight and sabbatical durations to the total flight and sabbatical durations
        total_flight_time += flight_duration
        total_sabbatical_time += sabbatical_duration

    # Calculate the total payment
    total_payment = (total_flight_time + (SABBATICAL_FACTOR - 1) * total_sabbatical_time) * FLIGHT_HOURS_PAYMENT + \
                    total_abroad_time * ESHEL_FACTOR

    # Print the report
    print("Last Month's Salary Report")
    # Ensure the salary is at least the base salary
    if total_payment < 4000:
        total_payment = 4000
        less_than_base_string = f"Total payment was less than the base salary ({total_payment}$), and was \n" \
                            f"therefore increased to the base salary (4000$)"
        print(less_than_base_string)
    total_payment_string = f"The total payment for the last month's flights is\t{total_payment}$\n"
    regular_flight_hours_payment_string = f"\tThe regular flight hours payment is\t\t\t\t" \
                                          f"{total_flight_time * FLIGHT_HOURS_PAYMENT}$\n"
    sabbatical_flight_hours_payment_string = f"\tThe sabbatical flight hours payment is\t\t\t" \
                                             f"{total_sabbatical_time * SABBATICAL_FACTOR * FLIGHT_HOURS_PAYMENT}$\n"
    abroad_payment_string = f"\tThe abroad payment is\t\t\t\t\t\t\t{total_abroad_time * ESHEL_FACTOR}$\n"
    print(total_payment_string,
          regular_flight_hours_payment_string,
          sabbatical_flight_hours_payment_string,
          abroad_payment_string)

    print("--------------------------")


def calculate_duration(a_date, a_time, b_date, b_time):
    """
    Calculate the duration between two timestamps
    :param a_date: The date of the first timestamp
    :param a_time: The time of the first timestamp
    :param b_date: The date of the second timestamp
    :param b_time: The time of the second timestamp
    :return: (float) The duration between the two timestamps in hours
    """
    a_timestamp = datetime.strptime(a_date + " " + a_time, "%Y-%m-%d %H:%M")
    b_timestamp = datetime.strptime(b_date + " " + b_time, "%Y-%m-%d %H:%M")
    duration = b_timestamp - a_timestamp
    duration_hours = duration.total_seconds() / 3600  # Convert duration to hours
    return duration_hours


if __name__ == "__main__":
    # Main program loop
    while True:
        print("Flight Tracking and Payment System")
        print("1. Enter Flight Details")
        print("2. Generate Report")
        print("3. Exit")
        choice = input("Select an option: ")

        if choice == "1":
            enter_flight_details()
        elif choice == "2":
            generate_report()
        elif choice == "3":
            print("Exiting the program...")
            break
        else:
            print("Invalid choice. Please try again.\n")
