import json
import os

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By


def get_all_estates_id():
    driver.get(
        "https://www.immoweb.be/fr/recherche/maison-et-appartement/a-vendre/Dinant/5500?countries=BE&page=1&orderBy=newest"
    )
    elem = driver.find_elements(
        By.XPATH, "//li[@class='search-results__item']//article//div//h2//a"
    )
    link_array = [
        e.get_attribute("href")[-e.get_attribute("href").find("/") - 2 :] for e in elem
    ]
    return link_array


def get_estate_info(id):
    driver.get(
        "https://www.immoweb.be/fr/annonce/appartement/a-vendre/dinant/5500/" + str(id)
    )
    elem = driver.find_element(By.XPATH, "//*[@type='text/javascript']")
    script = elem.get_attribute("innerHTML")[32:]
    return script


def write_json(file_name, script):
    f = open(file_name, "w")
    final = script[: script.find("}};") + 2]
    f.write(final)
    f.close()


def download_img(media, id):
    for i, picture in enumerate(media):
        filename = "estates/" + str(id) + "/picture_" + str(id) + "_" + str(i) + ".png"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        res = requests.get(picture["largeUrl"], stream=True).content
        im = open(filename, "wb")
        im.write(res)
        im.close()


def work_on_json(path, id):
    f = open(path, "r")
    data = json.loads(f.read())
    title = data["property"]["title"]
    type = data["property"]["type"]
    description = data["property"]["description"]
    surface = data["property"]["netHabitableSurface"]
    bedroomCount = data["property"]["bedroomCount"]
    roomCount = data["property"]["roomCount"]
    creationDate = data["publication"]["creationDate"]
    lastModificationDate = data["publication"]["lastModificationDate"]
    price = data["transaction"]["sale"]["price"]
    media = data["media"]["pictures"]
    print(type, str(price) + "e", surface, roomCount, bedroomCount)
    download_img(media, id)
    f.close()


def scrap_website():
    for id in estate_ids:
        file_name = "estate_" + str(id) + ".json"
        path = "raw_data/" + file_name
        json_script = get_estate_info(id)
        write_json(path, json_script)


def write_data_file():
    for id in estate_ids:
        file_name = "estate_" + str(id) + ".json"
        path = "raw_data/" + file_name
        work_on_json(path, id)


driver = webdriver.Chrome()
estate_ids = get_all_estates_id()
# scrap_website()
driver.close()

write_data_file()
