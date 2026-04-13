import pandas as pd
from datetime import datetime


# 1. READ THE TIMETABLE

def read_timetable(file_path):
    """
    Reads the exam timetable from a CSV file.
    Returns a list of dicts with keys: date, day, subject.
    """
    try:
        df = pd.read_csv(file_path, encoding='latin-1')

        # drop rows where all the values are missing
        df.dropna(how='all', inplace=True)
        
        timetable = []
        for _, row in df.iterrows():
            timetable.append({
                "date": row["Date"],
                "day": row["DAY"],
                "subject": row["Subject"]
            })
        
        return timetable
    
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return []
    
    except KeyError as e:
        print(f"Error: Column {e} not found in timetable file")
        return []
    


# 2. READ THE SYLLABUS
def read_syllabus(file_path):
    """
    Reads the syllabus from a CSV file.
    Returns a list of dicts with keys: subject, branch, chapter, sub_topic.
    """
    try:
        df = pd.read_excel(file_path)

        # Drop rows where all values are empty
        df = df.dropna(how="all")

        # Drop rows where both Branch and Chapter are missing, as they are essential for syllabus structure
        df = df.dropna(subset=["Branch", "Chapter"], how="all")

        # Forward fill Subject column to handle any missing subject cells
        df["Subject"] = df["Subject"].ffill()

        syllabus = []
        for _, row in df.iterrows():
            syllabus.append({
                "subject": row["Subject"],
                "branch": row["Branch"] if pd.notna(row["Branch"]) else "",
                "chapter": row["Chapter"] if pd.notna(row["Chapter"]) else "",
                "sub_topic": row["Sub Topic"] if pd.notna(row["Sub Topic"]) else ""
            })

        return syllabus

    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return []

    except KeyError as e:
        print(f"Error: Column {e} not found in syllabus file")
        return []



# 3. READ TARGET PLAN

def read_target_plan(file_path):
    """
    Reads the manually created ideal target plan from an Excel file.
    Returns a list of dicts with keys: date, day, subject, branch, topic, start_time, end_time.
    """
    try:
        
        df = pd.read_excel(file_path)

        # Drop rows where all values are empty
        df = df.dropna(how="all")

        # Forward fill DATE and DAY columns to handle merged cells
        df["DATE"] = df["DATE"].ffill()
        df["DAY"] = df["DAY"].ffill()



        target_plan = []
        for _, row in df.iterrows():
            target_plan.append({
                "date": str(row["DATE"]),
                "day": row["DAY"],
                "subject": row["SUBJECT"],
                "branch": row["BRANCH"] if pd.notna(row["BRANCH"]) else "",
                "topic": row["TOPIC"] if pd.notna(row["TOPIC"]) else "",
                "start_time": str(row["START TIME"]),
                "end_time": str(row["END TIME"])
            })

        return target_plan
    
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return []

    except KeyError as e:
        print(f"Error: Column {e} not found in target plan file")
        return []
    

# 4. GET LIST OF PUBLIC HOLIDAYS

def get_holidays():
    """
    Returns a list of public holidays for 2026 (Tamil Nadu).
    These days are treated as 4-hour study days (same as weekends).
    """
    return [
        "01-01-2026",  # New Year's Day
        "15-01-2026",  # Pongal
        "26-01-2026",  # Republic Day
        "21-03-2026",  # Ramzan (Id-ul-Fitr)
        "03-04-2026",  # Good Friday
        "14-04-2026",  # Tamil New Year's Day
        "28-05-2026",  # Bakrid (Id-ul-Zuha)
        "26-06-2026",  # Muharram
        "15-08-2026",  # Independence Day
        "26-08-2026",  # Milad-un-Nabi
        "04-09-2026",  # Krishna Jayanti
        "14-09-2026",  # Vinayakar Chathurthi
        "02-10-2026",  # Gandhi Jayanti
        "19-10-2026",  # Ayutha Pooja
        "20-10-2026",  # Vijaya Dasami
        "08-11-2026",  # Deepavali
        "25-12-2026",  # Christmas Day
    ]



# 5. CLASSIFY DAY TYPE

def get_day_type(date_str):
    """
    Takes a date string in DD-MM-YYYY format.
    Returns day type (weekday/weekend/holiday) and study sessions with timings.
    """
    try:
        
        date = datetime.strptime(date_str, "%d-%m-%Y").date()
        holidays = get_holidays()

        # Check if holiday
        if date_str in holidays:
            day_type = "holiday"

        # Check if weekend
        elif date.weekday() == 6:  # 6 = Sunday
            day_type = "weekend"

        else:
            day_type = "weekday"

        # Return sessions based on day type
        if day_type in ("weekend", "holiday"):
            return {
                "type": day_type,
                "hours": 4,
                "sessions": [
                    {"session": 1, "start_time": "11:00", "end_time": "12:10"},
                    {"session": 2, "start_time": "12:20", "end_time": "13:30"},
                    {"session": 3, "start_time": "18:00", "end_time": "19:10"},
                    {"session": 4, "start_time": "19:20", "end_time": "20:30"},
                ]
            }
        else:
            return {
                "type": day_type,
                "hours": 2,
                "sessions": [
                    {"session": 1, "start_time": "18:00", "end_time": "19:10"},
                    {"session": 2, "start_time": "19:20", "end_time": "20:30"},
                ]
            }

    except ValueError:
        print(f"Error: Invalid date format {date_str}. Use DD-MM-YYYY.")
        return {}



# 6. SAVE THE OUTPUT PLAN


def save_output_plan(plan_data, file_path):
    """
    Saves the final generated study plan to an Excel file.
    Expects plan_data as a list of dicts with keys:
    date, day, subject, branch, topic, start_time, end_time.
    """
    try:
        df = pd.DataFrame(plan_data)
        df.to_excel(file_path, index=False)
        print(f"Study plan saved to {file_path}")

    except Exception as e:
        print(f"Error saving study plan: {e}")









# TESTING
if __name__ == "__main__":
    print("=== TIMETABLE ===")
    timetable = read_timetable("data/time_table.csv")
    for exam in timetable:
        print(exam)

    print("\n=== SYLLABUS ===")
    syllabus = read_syllabus("data/syllabus.xlsx")
    for item in syllabus:
        print(item)

    print("\n=== TARGET PLAN ===")
    target_plan = read_target_plan("data/target_plan.xlsx")
    for session in target_plan:
        print(session)

    print("\n=== HOLIDAYS ===")
    holidays = get_holidays()
    print(holidays)

    print("\n=== DAY TYPE TEST ===")
    print(get_day_type("06-04-2026"))  # Weekday
    print(get_day_type("04-04-2026"))  # Weekend
    print(get_day_type("14-04-2026"))  # Holiday