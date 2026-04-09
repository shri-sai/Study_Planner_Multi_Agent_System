import pandas as pd
import datetime as date
import openpyxl


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






# TESTING
if __name__ == "__main__":
    timetable = read_timetable("data/time_table.csv")

    for exam in timetable:
        print(exam)

    syllabus = read_syllabus("data/syllabus.xlsx")
    for item in syllabus:
        print(item)