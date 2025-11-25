from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import json
from time import sleep

OPTIONS = webdriver.ChromeOptions()
OPTIONS.add_argument("--headless")
OPTIONS.add_argument("--window-size=1920,1080")


def scrape_hotels(location, pages=5):
    driver = webdriver.Chrome(options=OPTIONS)
    actions = ActionChains(driver)
    url = f"https://www.google.com/travel/search?q={location}"
    driver.get(url)
    done = False

    found_hotels = []
    page = 1
    result_number = 1
    while page <= pages:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(5)
        hotel_links = driver.find_elements(By.CSS_SELECTOR, "c-wiz > div > a")
        print(f"-----------------PAGE {page}------------------")
        print("FOUND ITEMS: ", len(hotel_links))
        for hotel_link in hotel_links:
            hotel_card = hotel_link.find_element(By.XPATH, "..")
            try:
                info = {}
                info["url"] = hotel_link.get_attribute("href")
                info["rating"] = 0.0
                info["price"] = "n/a"
                info["name"] = hotel_card.find_element(By.CSS_SELECTOR, "h2").text
                price_holder = hotel_card.find_elements(By.CSS_SELECTOR, "span")
                info["amenities"] = []
                amenities_holders = hotel_card.find_elements(By.CSS_SELECTOR, "li")
                for amenity in amenities_holders:
                    info["amenities"].append(amenity.text)
                if "DEAL" in price_holder[0].text or "PRICE" in price_holder[0].text:
                    if price_holder[1].text[0] == "$":
                        info["price"] = price_holder[1].text
                else:
                    info["price"] = price_holder[0].text
                rating_holder = hotel_card.find_elements(By.CSS_SELECTOR, "span[role='img']")
                if rating_holder:
                    info["rating"] = float(rating_holder[0].get_attribute("aria-label").split(" ")[0])
                info["result_number"] = result_number

                if info not in found_hotels:
                    found_hotels.append(info)
                result_number += 1

            except:
                continue
        print("Scraped Total:", len(found_hotels))

        next_button = driver.find_elements(By.XPATH, "//span[text()='Next']")
        if next_button:
            print("next button found!")
            sleep(1)
            actions.move_to_element(next_button[0]).click().perform()
            page += 1
            sleep(5)
        else:
            done = True

    driver.quit()

    with open("scraped-hotels.json", "w") as file:
        json.dump(found_hotels, file, indent=4)


if __name__ == "__main__":
    PAGES = 2
    scrape_hotels("miami", pages=PAGES)
