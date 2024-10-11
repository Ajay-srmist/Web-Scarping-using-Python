from bs4 import BeautifulSoup
import requests

def scrape_imdb_top_250():
    try:
        # Set the user-agent to mimic a browser request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        
        # Fetch the IMDb Top 250 page
        response = requests.get('https://www.imdb.com/chart/top/', headers=headers)
        response.raise_for_status()  # Check if the request was successful
        
        # Parse the page content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Print the HTML content to check if we're getting the correct page
        print("Page fetched successfully. Checking HTML structure...")
        print(soup.prettify()[:1000])  # Print only the first 1000 characters of the page for inspection

        # Find the table containing the top movies
        movies_table = soup.select('table.chart.full-width tr')
        print(f"Found {len(movies_table)} rows in the table.")  # Debugging statement

        # Check if any rows are found
        if len(movies_table) > 0:
            top_movies = []

            # Loop through each movie entry (skipping the header row)
            for movie in movies_table[1:]:
                title_column = movie.find('td', class_='titleColumn')
                if title_column:
                    rank = title_column.get_text(strip=True).split('.')[0]  # Rank
                    title = title_column.a.get_text()  # Title
                    year = title_column.span.get_text(strip=True).strip('()')  # Release year
                    rating_column = movie.find('td', class_='ratingColumn imdbRating')
                    rating = rating_column.strong.get_text() if rating_column else 'N/A'  # IMDb Rating

                    # Append movie data to the list
                    top_movies.append({
                        'rank': rank,
                        'title': title,
                        'year': year,
                        'rating': rating
                    })
            
            # Print the result
            for movie in top_movies:
                print(f"{movie['rank']}. {movie['title']} ({movie['year']}) - Rating: {movie['rating']}")
        else:
            print("No movies found in the table. Check the structure.")
    
    except Exception as e:
        print(f"An error occurred: {e}")

# Run the function to scrape the data
scrape_imdb_top_250()

