from bs4 import BeautifulSoup
import openpyxl.workbook
import requests

excel = openpyxl.workbook()
print(excel.sheetnames)

sheet = excel.active
sheet.title = 'Top Rated Movies'
print(excel.sheetnames)

sheet.append(['Movie Rank', 'Movie Name', 'Year of Release', 'IMDB Rating'])

try:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    source = requests.get("https://www.imdb.com/chart/top/", headers=headers)
    source.raise_for_status()
    soup = BeautifulSoup(source.text,'html.parser')
    movies = soup.find("tbody", class_="lister-list").find_all('tr')

    for movie in movies:
        name = movie.find('td', class_="titleColumn").a.text
        rank = movie.find('td', class_="titleColumn").get_text(strip = True).split('.')[0]
        year = movie.find('td', class_="titleColumn").span.text.strip('()')
        rating = movie.find('td', class_="ratingColumn imdbRating").strong.text

        print(rank, name, year, rating)
        sheet.append([rank, name, year, rating])
        break

except Exception as e:
    print(e)

excel.save('IMDBrating.xlsx')
