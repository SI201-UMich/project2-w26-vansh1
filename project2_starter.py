# SI 201 HW4 (Library Checkout System)
# Your name: Vansh Patel
# Your student id: 91874961
# Your email: vanshpat@umich.edu

# Who or what you worked with on this homework (including generative AI like ChatGPT):
# If you worked with generative AI also add a statement for how you used it.
# e.g.:
# Asked ChatGPT for hints on debugging and for suggestions on overall code structure

# I used ChatGPT mostly to debug a lot of the errors I was running into and also to help
# with some of the more complex regex parts. I also used it to kinda understand how to
# parse the HTML better and structure my functions since that part was confusing at first.

# Did your use of GenAI on this assignment align with your goals and guidelines in your Gen AI contract? If not, why?
#Yeah this use mostly aligned with my GenAI guidelines, I didn’t just copy answers but
# more used it as a tool to guide me and fix mistakes when I got stuck
#
# --- ARGUMENTS & EXPECTED RETURN VALUES PROVIDED --- #
# --- SEE INSTRUCTIONS FOR FULL DETAILS ON METHOD IMPLEMENTATION --- #

from bs4 import BeautifulSoup
import re
import os
import csv
import unittest
import requests  # kept for extra credit parity


# IMPORTANT NOTE:
"""
If you are getting "encoding errors" while trying to open, read, or write from a file, add the following argument to any of your open() functions:
    encoding="utf-8-sig"
"""


def load_listing_results(html_path) -> list[tuple]:
    """
    Load file data from html_path and parse through it to find listing titles and listing ids.

    Args:
        html_path (str): The path to the HTML file containing the search results

    Returns:
        list[tuple]: A list of tuples containing (listing_title, listing_id)
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
       
    file1 = open(html_path, encoding="utf-8-sig")
    html = file1.read()
    file1.close()
    results = []
    pattern = re.compile(r'aria-labelledby="title_(\d+)".*?data-testid="listing-card-title">(.*?)</div>', re.DOTALL)
    matches = pattern.findall(html)

    for listing_id, listing_title in matches:
        listing_title = BeautifulSoup(listing_title, "html.parser").get_text(strip=True)
        results.append((listing_title, listing_id))

    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================
    return results


def get_listing_details(listing_id) -> dict:
    """
    Parse through listing_<id>.html to extract listing details.

    Args:
        listing_id (str): The listing id of the Airbnb listing

    Returns:
        dict: Nested dictionary in the format:
        {
            "<listing_id>": {
                "policy_number": str,
                "host_type": str,
                "host_name": str,
                "room_type": str,
                "location_rating": float
            }
        }
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    path = os.path.join("html_files", f"listing_{listing_id}.html")
    file1 = open(path, encoding="utf-8-sig")
    soup = BeautifulSoup(file1, "html.parser")
    html = soup.get_text(" ", strip=True)
    file1.close()

    policy_number = ""
    policy_match = re.search(r"Policy number[:\s]*([A-Za-z0-9\-]+)", html, re.IGNORECASE)

    if policy_match:
        raw_policy = policy_match.group(1).strip()

        if re.search(r"pending", raw_policy, re.IGNORECASE):
            policy_number = "Pending"
        elif re.search(r"exempt", raw_policy, re.IGNORECASE):
            policy_number = "Exempt"
        else:
            policy_number = raw_policy
    else:
        policy_number = ""

    if "Superhost" in html:
        host_type = "Superhost"
    else:
        host_type = "regular"

    host_name = ""

    host_match = re.search(r"Hosted by\s+([A-Za-z]+(?:\s+(?:and|And)\s+[A-Za-z]+)?)", html)
    if host_match:
        host_name = host_match.group(1).strip()
    else:
        host_match = re.search(r"([A-Z][a-z]+(?:\s+(?:And|and)\s+[A-Z][a-z]+)?)\s+is a Superhost", html)
        if host_match:
            host_name = host_match.group(1).strip()

    room_type = "Entire Room"

    subtitle_match = re.search(
        r"(Entire|Private|Shared)[^·\|\n]*?(room|suite|home|apartment|guesthouse|guest suite)",
        html,
        re.IGNORECASE
    )
    subtitle_text = subtitle_match.group(0) if subtitle_match else html

    if "Private" in subtitle_text:
        room_type = "Private Room"
    elif "Shared" in subtitle_text:
        room_type = "Shared Room"
    else:
        room_type = "Entire Room"

    location_rating = 0.0
    loc_match = re.search(r"Location\s+([0-9]\.[0-9])", html)
    if loc_match:
        location_rating = float(loc_match.group(1))
    else:
        loc_match = re.search(r"Location[^0-9]*([0-9]\.[0-9])", html)
        if loc_match:
            location_rating = float(loc_match.group(1))

    return {listing_id: { "policy_number": policy_number, "host_type": host_type, "host_name": host_name, "room_type": room_type, "location_rating": location_rating}}
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


def create_listing_database(html_path) -> list[tuple]:
    """
    Use prior functions to gather all necessary information and create a database of listings.

    Args:
        html_path (str): The path to the HTML file containing the search results

    Returns:
        list[tuple]: A list of tuples. Each tuple contains:
        (listing_title, listing_id, policy_number, host_type, host_name, room_type, location_rating)
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    listings = load_listing_results(html_path)
    database = []

    for listing_title, listing_id in listings:
        details = get_listing_details(listing_id)[listing_id]
        row = (listing_title, listing_id, details["policy_number"], details["host_type"], details["host_name"], details["room_type"], details["location_rating"])
        database.append(row)

    return database
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


def output_csv(data, filename) -> None:
    """
    Write data to a CSV file with the provided filename.

    Sort by Location Rating (descending).

    Args:
        data (list[tuple]): A list of tuples containing listing information
        filename (str): The name of the CSV file to be created and saved to

    Returns:
        None
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    sorted1 = sorted(data, key=lambda x: x[6], reverse=True)

    file11 = open(filename, "w", newline="", encoding="utf-8-sig")
    writer = csv.writer(file11)
    writer.writerow([ "Listing Title", "Listing ID", "Policy Number", "Host Type", "Host Name", "Room Type", "Location Rating"])

    for row in sorted1:
        writer.writerow(row)

    file11.close()

    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


def avg_location_rating_by_room_type(data) -> dict:
    """
    Calculate the average location_rating for each room_type.

    Excludes rows where location_rating == 0.0 (meaning the rating
    could not be found in the HTML).

    Args:
        data (list[tuple]): The list returned by create_listing_database()

    Returns:
        dict: {room_type: average_location_rating}
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    totals = {}
    counts = {}
    for row in data:
        roomType = row[5]
        rating = row[6]
        if rating == 0.0:
            continue
        if roomType not in totals:
            totals[roomType] = 0
            counts[roomType] = 0
        totals[roomType] += rating
        counts[roomType] += 1

    averages = {}
    for roomType in totals:
        averages[roomType] = round(totals[roomType] / counts[roomType], 1)
    return averages
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


def validate_policy_numbers(data) -> list[str]:
    """
    Validate policy_number format for each listing in data.
    Ignore "Pending" and "Exempt" listings.

    Args:
        data (list[tuple]): A list of tuples returned by create_listing_database()

    Returns:
        list[str]: A list of listing_id values whose policy numbers do NOT match the valid format
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    invalid = []
    pattern1 = re.compile(r"20\d{2}-00\d{4}STR$")
    pattern2 = re.compile(r"STR-000\d{4}$")

    for row in data:
        listing_id = row[1]
        policy = row[2]

        # ignore Pending / Exempt
        if policy in ["Pending", "Exempt"]:
            continue

        # check validity
        if not (pattern1.match(policy) or pattern2.match(policy)):
            invalid.append(listing_id)

    return invalid
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


# EXTRA CREDIT
def google_scholar_searcher(query):
    """
    EXTRA CREDIT

    Args:
        query (str): The search query to be used on Google Scholar
    Returns:
        List of titles on the first page (list)
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    url = "https://scholar.google.com/scholar"
    params = {"q": query}
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code != 200:
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    titles = []

    for item in soup.find_all("h3", class_="gs_rt"):
        title = item.get_text(" ", strip=True)
        if title:
            titles.append(title)

    return titles
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


class TestCases(unittest.TestCase):
    def setUp(self):
        self.base_dir = os.path.abspath(os.path.dirname(__file__))
        self.search_results_path = os.path.join(self.base_dir, "html_files", "search_results.html")

        self.listings = load_listing_results(self.search_results_path)
        self.detailed_data = create_listing_database(self.search_results_path)

    def test_load_listing_results(self):
        # TODO: Check that the number of listings extracted is 18.
        #//print(self.listings)
        self.assertEqual(len(self.listings), 18)
        # TODO: Check that the FIRST (title, id) tuple is  ("Loft in Mission District", "1944564").
        self.assertEqual(self.listings[0], ("Loft in Mission District", "1944564"))

    def test_get_listing_details(self):
        html_list = ["467507", "1550913", "1944564", "4614763", "6092596"]

        # TODO: Call get_listing_details() on each listing id above and save results in a list.
        results = [get_listing_details(lid) for lid in html_list]
        #print(results)
        # TODO: Spot-check a few known values by opening the corresponding listing_<id>.html files.
        # 1) Check that listing 467507 has the correct policy number "STR-0005349".
        self.assertEqual(results[0]["467507"]["policy_number"], "STR-0005349")
        # 2) Check that listing 1944564 has the correct host type "Superhost" and room type "Entire Room".
        self.assertEqual(results[2]["1944564"]["host_type"], "Superhost")
        # 3) Check that listing 1944564 has the correct location rating 4.9.
        self.assertEqual(results[2]["1944564"]["location_rating"], 4.9)

    def test_create_listing_database(self):
        # TODO: Check that each tuple in detailed_data has exactly 7 elements:
        # (listing_title, listing_id, policy_number, host_type, host_name, room_type, location_rating)
        for row in self.detailed_data:
            self.assertEqual(len(row), 7)
        # TODO: Spot-check the LAST tuple is ("Guest suite in Mission District", "467507", "STR-0005349", "Superhost", "Jennifer", "Entire Room", 4.8).
        last = ("Guest suite in Mission District", "467507", "STR-0005349", "Superhost", "Jennifer", "Entire Room", 4.8)
        self.assertEqual(self.detailed_data[-1], last)

    def test_output_csv(self):
        out_path = os.path.join(self.base_dir, "test.csv")

        # TODO: Call output_csv() to write the detailed_data to a CSV file.
        output_csv(self.detailed_data, out_path)
        # TODO: Read the CSV back in and store rows in a list.
        rows = []
        with open(out_path, newline="", encoding="utf-8-sig") as file1:
            reader = csv.reader(file1)
            next(reader)
            for row in reader:
                rows.append(row)
        # TODO: Check that the first data row matches ["Guesthouse in San Francisco", "49591060", "STR-0000253", "Superhost", "Ingrid", "Entire Room", "5.0"].
        first = ["Guesthouse in San Francisco", "49591060", "STR-0000253", "Superhost", "Ingrid", "Entire Room", "5.0",]
        self.assertEqual(rows[0], first)
        os.remove(out_path)

    def test_avg_location_rating_by_room_type(self):
        # TODO: Call avg_location_rating_by_room_type() and save the output.
        averages = avg_location_rating_by_room_type(self.detailed_data)
        # TODO: Check that the average for "Private Room" is 4.9.
        self.assertEqual(averages["Private Room"], 4.9)

    def test_validate_policy_numbers(self):
        # TODO: Call validate_policy_numbers() on detailed_data and save the result into a variable invalid_listings.
        invalid_listings = validate_policy_numbers(self.detailed_data)
        # TODO: Check that the list contains exactly "16204265" for this dataset.
        self.assertEqual(invalid_listings, ["16204265"])

def main():
    detailed_data = create_listing_database(os.path.join("html_files", "search_results.html"))
    output_csv(detailed_data, "airbnb_dataset.csv")
    results = google_scholar_searcher("cheesecake")
    for title in results:
        print(title)


if __name__ == "__main__":
    main()
    unittest.main(verbosity=2)