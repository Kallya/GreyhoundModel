from selenium import webdriver
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.by import By

def extract_distance(text):
    return text.split()[-1].strip("()")

def extract_race_class(header):
    race_class =  header.split('$')[0]
    return race_class[:-3]

def extract_fastest_split(header):
    return float(header.split()[1].strip(','))

# first_entry is "runnerContainer" element
def extract_win_time(first_entry):
    sub_details = first_entry.find_elements(By.CSS_SELECTOR, ".runnerSubDetails div")
    time = sub_details[1].get_attribute("innerText").strip()[4:]
    return float(time)

def get_variant_times(time_dict):
    variant_times = {}

    for distance in time_dict:
        total_averages = 0
        for grade in time_dict[distance]:
            times = []
            times = time_dict[distance][grade]
            total_averages += sum(times) / len(times)
        variant_times[distance] = total_averages / len(time_dict[distance])
    
    return variant_times

def get_time_variant(variant_time, standard_time):
    return variant_time - standard_time

def get_adjusted_time(actual_time, time_variant):
    return actual_time - time_variant

results_page_url = input("Results page URL: ")

service = Service(executable_path=EdgeChromiumDriverManager().install())
options = webdriver.EdgeOptions()
driver = webdriver.Edge(service=service, options=options)
driver.get(results_page_url)

races = driver.find_elements(By.CLASS_NAME, "dogContainer")
 # track = driver.title.split()[0]
 # maybe use track to access
race_time_dict = {}
sect_time_dict = {}

for race in races:
    # extract distance
    race_summary = race.find_element(By.CLASS_NAME, "font14")
    distance = extract_distance(race_summary.get_attribute("innerText"))

    # extract grade and 1st split
    header = race.find_elements(By.CSS_SELECTOR, ".runnerFormHeader div")
    grade = extract_race_class(header[1].get_attribute("innerText"))
    fastest_1st_split = extract_fastest_split(header[2].get_attribute("innerText"))

    # get win time
    first_runner_entry = race.find_element(By.CLASS_NAME, "runnerContainer")
    win_time = extract_win_time(first_runner_entry)

    if distance not in race_time_dict:
        race_time_dict[distance] = {}
        sect_time_dict[distance] = {}

    if grade not in race_time_dict[distance]:
        race_time_dict[distance][grade] = []
        sect_time_dict[distance][grade] = []

    race_time_dict[distance][grade].append(win_time)
    sect_time_dict[distance][grade].append(fastest_1st_split)

# calculating time variants
variant_race_times = get_variant_times(race_time_dict)
variant_sect_times = get_variant_times(sect_time_dict)

race_time_variants = {}
sect_time_variants = {}
for distance in variant_race_times:
    standard_race_time = float(input(f"{distance} standard race time: "))
    standard_sect_time = float(input(f"{distance} standard 1st sectional time: "))
    race_time_variants[distance] = get_time_variant(variant_race_times[distance], standard_race_time)
    sect_time_variants[distance] = get_time_variant(variant_sect_times[distance], standard_sect_time)

# user inputs
racing_distance = input("Please enter the racing distance (e.g. '300m'): ")

while racing_distance:
    recorded_race_time = float(input("Recorded race time: "))
    recorded_sect_time = float(input("Recorded 1st sectional time: "))
    print(f"Adjusted race time: {recorded_race_time - race_time_variants[racing_distance]}")
    print(f"Adjusted 1st sectional time: {recorded_sect_time - sect_time_variants[racing_distance]}")
    racing_distance = input("Please enter the racing distance (e.g. '300m'): ")

driver.close()


