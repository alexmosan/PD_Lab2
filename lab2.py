import os
import requests
import time
import cloudscraper
from bs4 import BeautifulSoup

user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    ]

def save_reviews(movie_id, review_type, num_reviews, agentIndex):
    base_url = f"https://www.kinopoisk.ru/film/{movie_id}/reviews/ord/rating/status/{review_type}/perpage/10/page/"

    
    folder_path = f"dataset/{review_type}"
    os.makedirs(folder_path, exist_ok=True)
    exitFlag = False
    agentIndex = 0
    
    scraper = cloudscraper.create_scraper()
    
    for page in range(1, num_reviews // 10 + 1):
        if exitFlag:
            return
        url = base_url + str(page)
        
        try:
            response = scraper.get(url, headers={"User-Agent":user_agents[agentIndex]})
            if response.status_code != 200:
                print(response.text)
            
            while 'captcha' in response.url:
                agentIndex += 1
                response = scraper.get(url, headers={"User-Agent":user_agents[agentIndex]})
                input()

            soup = BeautifulSoup(response.text, 'html.parser')
            reviews = soup.find_all('div', class_='brand_words')
            
            if reviews.__len__() == 0:
                exitFlag = True
            for i, review in enumerate(reviews):
                review_text = review.get_text(strip=True)
                movie_name = soup.title.text.split('—')[0].strip()
                
                
                file_number = str(i).zfill(4)
                
                
                with open(f"{folder_path}/{file_number}.txt", 'w', encoding='utf-8') as file:
                    file.write(f"Название фильма: {movie_name}\n")
                    file.write(review_text)
                    
                time.sleep(100) 
        
        except Exception as e:
            print("Ошибка при запросе страницы:", e)

movie_id = 435 
num_reviews_per_type = 10

save_reviews(movie_id, "good", num_reviews_per_type, 0)
save_reviews(movie_id, "bad", num_reviews_per_type, 0)
