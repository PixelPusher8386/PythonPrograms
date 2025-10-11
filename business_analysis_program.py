'''
Problem statement:
What are the trends in current work of work?  
1. Which occupations show the highest growth rates over time 
2. In a given year, which is the most popular among each age range?
 

Structure          
Ask user which question user would like to use -> choice
If 1
    Ask user for start and end year -> start_year, end_year
    Check years are valid --> continue to functions
    growth_rate(start_year, end_year)
Else
    Ask only 1 year
    Check years are valid --> continue to functions
    age_popularity(start_year, end_year)
Would you like to continue
    If yes
        Ask user which question user would like to use -> choice
    Else
        Exit if user presses Enter'''

import csv

file_path = r"C:\Users\User\Documents\datasetb.csv"
# FILE SHOULD BE JUST A NAME!!! (TOP RIGHT SIDE OF MY SCREEN)

data = {} #initiate a dictionary to store years, age range, occupation
years = [str(y) for y in range(2007, 2025)] #this can be simplified but idk how yet
age_ranges = set()
occupations = set()


with open(file_path, newline='', encoding='utf-8') as csvfile:
    csvreader = csv.reader(csvfile)
    header = next(csvreader)

#csvreader will create a list of strings where each member of the list is the next column of that row
    for row in csvreader:
        age = row[0].strip() #extract age range strings,.strip() will remove any unnecessary space
        occ = row[1].strip() #extract occupation strings, same as above
        age_ranges.add(age) #store the strings of age ranges into a set. 11 age group categories
        occupations.add(occ) #store occupation strings into a set. 9 occupation categories

        for i, year in enumerate(header[2:]):  #this whole part can be simplified as well
            if year not in years:
                continue
            val = row[i+2].strip() #add as safety cleaning of extra spaces, because "Apple" and "Apple " can be recognised as 2 different entries
            if val.lower() in ("na", "-"): #i think this .lower() is unnecessary
                continue
            count = float(val)
            data[(int(year), age, occ)] = count

def growth_rate(start_year, end_year):  
    growth = {}
    # Loop through each occupation
    for occ in occupations:
        start_total = 0
        end_total = 0
    
        for age in age_ranges:
            start_total = start_total + data.get((start_year, age, occ), 0)
            end_total = end_total + data.get((end_year, age, occ), 0)
    
        if start_total > 0:
            growth_rate = (end_total - start_total) / start_total
            growth[occ] = growth_rate

    # Convert to list
    growth_list = []
    for occ in growth:
        growth_list.append([occ, growth[occ]])

    # Manual sort (highest → lowest)
    for i in range(len(growth_list) - 1):
        for j in range(i + 1, len(growth_list)):
            if growth_list[i][1] < growth_list[j][1]:
                temp = growth_list[i]
                growth_list[i] = growth_list[j]
                growth_list[j] = temp

    # Display table
    print("\nOccupation Growth Rates ({} → {}):".format(start_year, end_year))
    print("_" * 96)
    print("| {:<75} | {:>15} |".format("Occupation", "Growth Rate"))
    print("|" + "_" * 95 + "|")

    for item in growth_list:
        occ_name = item[0]
        rate = item[1]
        print("| {:<75} | {:>14.2f}% |".format(occ_name, rate * 100))
        print("|" + "_" * 95 + "|")
    
def age_popularity(start_year):
    year = int(start_year)
    if 2007 <= year <= 2024:
        # Collect most popular occupation for each age range
        most_popular_by_age = {}

        for age in age_ranges:
            top_occ = None
            top_count = -1
            for occ in occupations:
                count = data.get((year, age, occ), 0)
                if count > top_count:
                    top_occ = occ
                    top_count = count
            most_popular_by_age[age] = (top_occ,top_count)

        # Display results in table format
        print(f"\nMost Popular Occupations Among Each Age Range in {year}:")
        print("_" * 86)
        print(f"| {'Age Range':<15} | {'Most Popular Occupation':<40} | {'Total Workforce(\'000)':<19} |")
        print("|" + "_" * 84 + "|")
        
        for age, (occ, count) in most_popular_by_age.items():
            print(f"| {age:<15} | {occ:<40} | {count:<21} | ")
            print("|" + "_" * 84 + "|")

def get_analysis_choice():
    """Prompts the user for analysis choice (1 or 2) or 'q' to quit."""
    print("\n--- Analysis Selection ---")
    print("Press 1 for 'Which occupations show the highest growth rates over time?'")
    print("Press 2 for 'Which is the most popular among each age range?'")
    print("Press 'q' to quit the program.")

    while True:
        user_input = input("Enter choice (1, 2, or q): ").strip().lower()

        if user_input == 'q':
            return None # Signal to quit
        
        try:
            choice = int(user_input)
            if choice in (1, 2):
                return choice
            else:
                print("Invalid choice. Please enter 1, 2, or 'q'.")
        except ValueError:
            print("Invalid input. Please enter 1, 2, or 'q'.")

def get_years_for_choice(choice):
    """Prompts the user for the required year(s) based on the choice."""
    min = 2007
    max = 2024
    
    while True:
        try:
            if choice == 1:
                start_year = input(f"Enter start year ({min}–{max}): ").strip()
                if start_year.lower() == 'q': return None, None
                start_year = int(start_year)
                
                end_year = input(f"Enter end year ({min}–{max}): ").strip()
                if end_year.lower() == 'q': return None, None
                end_year = int(end_year)
                
                if not (min <= start_year <= max and min <= end_year <= max and start_year < end_year):
                    print(f"Invalid range. Years must be between {min} and {max}, and start year must be less than end year.")
                    continue
                return start_year, end_year
            
            elif choice == 2:
                year_input = input(f"Enter the year ({min}–{max}): ").strip()
                if year_input.lower() == 'q': return None, None
                year = int(year_input)
                
                if not (min <= year <= max):
                    print(f"Invalid year. Please enter a year between {min} and {max}.")
                    continue
                return year, None
            
            else:
                return None, None # Should not happen if logic is correct

        except ValueError:
            print("Invalid input. Please enter a valid numerical year or 'q' to quit.")
        
def main():
    while True:
    
        user_input = input("\nWould you like to continue with the analysis? (Type 'Y' or press any key to exit): ").strip().upper()
        
        if user_input != "Y":
            print("\nExiting analysis program. Goodbye! 👋")
            break # Exit the while loop
        
        # 2. Get the analysis choice
        choice = get_analysis_choice()
        
        if choice is None:
            # User pressed Enter during choice selection
            print("\nExiting analysis program. Goodbye! 👋")
            break 
            
        # 3. Get the year(s) and execute the function
        start_year, end_year = get_years_for_choice(choice)
        
        if start_year is not None:
            if choice == 1:
                growth_rate(start_year, end_year)
            elif choice == 2:
                # The age_popularity function only needs one year
                age_popularity(start_year)
        else:
            # This part handles errors in year input, though get_years_for_choice
            # is designed to loop until valid input is given.
            print("Could not proceed due to invalid year input.")

main()