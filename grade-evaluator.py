import csv
import sys
import os

def load_csv_data():
    """
    Prompts the user for a filename, checks if it exists, 
    and extracts all fields into a list of dictionaries.
    """
    filename = input("Enter the name of the CSV file to process (e.g., grades.csv): ")
    
    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        sys.exit(1)
        
    assignments = []
    
    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Convert numeric fields to floats for calculations
                assignments.append({
                    'assignment': row['assignment'],
                    'group': row['group'],
                    'score': float(row['score']),
                    'weight': float(row['weight'])
                })
        return assignments
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        sys.exit(1)

def evaluate_grades(data):
    """
    Implement your logic here.
    'data' is a list of dictionaries containing the assignment records.
    """
    print("\n--- Processing Grades ---")
    
     #  handles empty CSV (file exists but has 0 rows) ===
    if not data:
        print("No assignment data found in the file. Nothing to evaluate.")
        return

    # a) Checks if all scores are 0-100 ===
    invalid_scores = [row for row in data if row['score'] < 0 or row['score'] > 100]
    if invalid_scores:
        print("Error: The following assignments have invalid scores (must be 0-100):")
        for row in invalid_scores:
            print(f"  - {row['assignment']}: {row['score']}")
        return

    #  b) Validates total weights (Total=100, Formative=60, Summative=40) ===
    formative_rows = [row for row in data if row['group'].strip().lower() == 'formative']
    summative_rows = [row for row in data if row['group'].strip().lower() == 'summative']

    formative_weight = sum(row['weight'] for row in formative_rows)
    summative_weight = sum(row['weight'] for row in summative_rows)
    total_weight = formative_weight + summative_weight

    if round(total_weight, 2) != 100:
        print(f"Error: Total weight is {total_weight}, but it must equal 100.")
        return
    if round(formative_weight, 2) != 60:
        print(f"Error: Formative weights sum to {formative_weight}, but must equal 60.")
        return
    if round(summative_weight, 2) != 40:
        print(f"Error: Summative weights sum to {summative_weight}, but must equal 40.")
        return

    # c) Calculates the Final Grade and GPA ===
    total_grade = sum(row['score'] * row['weight'] for row in data) / 100
    gpa = (total_grade / 100) * 5.0

    # === ADDED: category scores, needed for the pass/fail rule in (d) ===
    formative_score = (sum(row['score'] * row['weight'] for row in formative_rows) / formative_weight
                        if formative_weight > 0 else 0)
    summative_score = (sum(row['score'] * row['weight'] for row in summative_rows) / summative_weight
                        if summative_weight > 0 else 0)

    print(f"\nFormative Category Score: {formative_score:.2f}%")
    print(f"Summative Category Score: {summative_score:.2f}%")
    print(f"Total Weighted Grade: {total_grade:.2f}%")
    print(f"GPA: {gpa:.2f} / 5.0")

    # d) Determines Pass/Fail status (>= 50% in BOTH categories) ===
    passed = formative_score >= 50 and summative_score >= 50
    status = "PASSED" if passed else "FAILED"

    # e) Finds failed formative assignments with the highest weight ===
    resubmission_candidates = []
    if not passed:
        failed_formatives = [row for row in formative_rows if row['score'] < 50]
        if failed_formatives:
            highest_weight = failed_formatives[0]['weight']
            for row in failed_formatives[1:]:
                if row['weight'] > highest_weight:
                    highest_weight = row['weight']

            resubmission_candidates = [row for row in failed_formatives if row['weight'] == highest_weight]

    # f) Prints the final decision and resubmission options ===
    print(f"\nFinal Status: {status}")

    if not passed:
        if resubmission_candidates:
            print("Eligible for Resubmission:")
            for row in resubmission_candidates:
                print(f"  - {row['assignment']} (Weight: {row['weight']}, Score: {row['score']})")
        else:
            print("No formative assignments are eligible for resubmission.")
          

if __name__ == "__main__":
    # 1. Load the data
    course_data = load_csv_data()
    
    # 2. Process the features
    evaluate_grades(course_data)
