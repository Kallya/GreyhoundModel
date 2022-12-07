from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

def get_page_soup(url: str):
    r = Request(url, headers={"User-Agent": "Mozilla/5.0"})

    with urlopen(r) as webpage:
        content = webpage.read().decode()
        soup = BeautifulSoup(content)

    return soup

# soup refers to the result page beautifulsoup object
def get_track_loc(soup):
    soup.find("h1", class_="pageTitle").text.split()[0]

# race_header refers to header of the table element containing the results
def get_race_no(race_header):
    return int(race_header[0].text.split()[1])

def get_distance(race_header):
    return int(race_header[2].text[:-1])

def get_grade(race_header):
    return race_header[3].text

def get_fastest_split(race_header):
    try:
        return float(race_header[5].text.split()[1].strip(','))
    except:
        return None

# race_results refers to table element containing the results
def get_win_time(race_result_data):
    return float(race_result_data[0].find_all("td", recursive=False)[4].text)

def add_race_metadata(result_entry, race_header):
    result_entry["distance"] = get_distance(race_header)
    result_entry["grade"] = get_grade(race_header)
    result_entry["race_no"] = get_race_no(race_header)
    result_entry["fastest_split"] = get_fastest_split(race_header)

# entry refers to a row in the results table
def get_dog_result(entry):
    data = entry.find_all("td", recursive=False)
    dog_results = {}
    try:
        dog_results["place"] = int(data[0].text)
    except:
        return None
    dog_results["place"] = int(data[0].text)
    dog_results["box"] = int(data[1].text)
    dog_results["dog_id"] = data[2].strong.a.text # lower case or uppercase?
    dog_results["time"] = float(data[4].text)
    dog_results["sect_time"] = float(data[6].text)
    dog_results["weight"] = float(data[8].text[:-2])

    return dog_results

# get results from single results page
def get_race_results(result_url):
    soup = get_page_soup(result_url)
    results = soup \
        .find("div", class_="resultsDesktopContent") \
        .find_all("div")
    track_loc = get_track_loc(soup)

    all_race_results = []
    for r in results:
        result_entry = {}
        race_header = r.find("table", class_="raceHeader").find_all("td")
        result_entry["track_loc"] = track_loc
        add_race_metadata(result_entry, race_header)

        race_result_data = r \
            .find("table", class_="raceResultsTable") \
            .tbody \
            .find_all("tr", recursive=False)
        result_entry["win_time"] = get_win_time(race_result_data)

        runner_num = 0
        race_results = []
        for entry in race_result_data:
            dog_result = get_dog_result(entry)
            if dog_result != None:
                race_results.append(dog_result)
                runner_num += 1
        
        result_entry["runner_num"] = runner_num
        result_entry["results"] = race_results
        all_race_results.append(result_entry)

    return all_race_results


