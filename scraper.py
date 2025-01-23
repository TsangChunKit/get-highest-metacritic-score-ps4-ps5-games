import requests
from bs4 import BeautifulSoup
import time

def extract_game_data(url):
    """Extracts game data from a Metacritic page."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an exception for bad status codes
    soup = BeautifulSoup(response.content, 'html.parser')

    games = []
    game_cards = soup.find_all('div', class_='c-finderProductCard_info')
    for card in game_cards:
        try:
            title_element = card.find('h3', class_='c-finderProductCard_titleHeading')
            if title_element:
                parts = title_element.find_all('span')
                if len(parts) == 2:
                    no = parts[0].text.strip().replace('.', '')
                    game_name = parts[1].text.strip()
                else:
                    no = "N/A"
                    game_name = title_element.text.strip()
            else:
                no = "N/A"
                game_name = "N/A"

            score_element = card.find('div', class_='c-siteReviewScore_xsmall')
            mc_score = score_element.text.strip() if score_element else "N/A"

            games.append({
                'No': no,
                'Game Name': game_name,
                'MC Score': mc_score,
                'Platform': "PS4/PS5", # since all the pages are PS4/PS5
                'Available on PS Plus': "N/A", # Placeholder
                'Status': "Not yet" # Placeholder
            })
        except Exception as e:
            print(f"Error processing card: {e}")
            continue
    return games


def generate_html_table(games):
    """Generates an HTML table from the game data."""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
    <title>Metacritic Games</title>
    <style>
        table {
            border-collapse: collapse;
            width: 100%;
        }
        th, td {
            border: 1px solid black;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
        }
    </style>
    </head>
    <body>
    <h2>Metacritic Games</h2>
    <table>
        <thead>
            <tr>
                <th>No.</th>
                <th>Platform</th>
                <th>Game Name</th>
                <th>MC Score</th>
                <th>Available on PS Plus</th>
                <th>Status</th>
            </tr>
        </thead>
        <tbody>
    """
    for game in games:
        html += f"""
            <tr>
                <td>{game['No']}</td>
                <td>{game['Platform']}</td>
                <td>{game['Game Name']}</td>
                <td>{game['MC Score']}</td>
                <td>{game['Available on PS Plus']}</td>
                <td>{game['Status']}</td>
            </tr>
        """
    html += """
        </tbody>
    </table>
    </body>
    </html>
    """
    return html


if __name__ == "__main__":
    urls = [
        "https://www.metacritic.com/browse/game/?releaseYearMin=1958&releaseYearMax=2025&platform=ps5&platform=ps4&page=1",
        "https://www.metacritic.com/browse/game/?releaseYearMin=1958&releaseYearMax=2025&platform=ps5&platform=ps4&page=2",
        "https://www.metacritic.com/browse/game/?releaseYearMin=1958&releaseYearMax=2025&platform=ps5&platform=ps4&page=3",
        "https://www.metacritic.com/browse/game/?releaseYearMin=1958&releaseYearMax=2025&platform=ps5&platform=ps4&page=4",
        "https://www.metacritic.com/browse/game/?releaseYearMin=1958&releaseYearMax=2025&platform=ps5&platform=ps4&page=5",
        "https://www.metacritic.com/browse/game/?releaseYearMin=1958&releaseYearMax=2025&platform=ps5&platform=ps4&page=6"
    ]

    all_games = []
    for url in urls:
        all_games.extend(extract_game_data(url))
        time.sleep(0.5)  # Add a 2-second delay

    html_table = generate_html_table(all_games)

    with open("metacritic_games.html", "w", encoding="utf-8") as f:
        f.write(html_table)

    print("Data extracted and saved to 'metacritic_games.html'")
