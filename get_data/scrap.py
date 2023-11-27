import os
import csv
import random
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as Ec
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import time

urls = [
    "https://www.google.com/search?q=voiture+de+luxe+rolls-royce&bih=495&biw=1131&hl=fr&tbm=shop&sa=X&ved=2ahUKEwigj5nYyt2CAxUgGGIAHVi6C5EQ1TV6BQgBEJAB",
    "https://www.google.com/search?q=voiture+de+luxe+mercedes&sa=X&sca_esv=585503012&biw=1468&bih=656&tbm=shop&sxsrf=AM9HkKkuElA04xBEwiOXIO12AlLvK7gENQ%3A1701053882799&ei=ugVkZYKAMP6q5NoPkNGTwAc&oq=voiture+de+luxe+me&gs_lp=Egtwcm9kdWN0cy1jYyISdm9pdHVyZSBkZSBsdXhlIG1lKgIIADIGEAAYFhgeMgYQABgWGB5IyC5QpAdYshxwAXgAkAEAmAHoAaAB_QaqAQUwLjUuMbgBAcgBAPgBAcICCxCuARjKAxiwAxgnwgIEECMYJ4gGAZAGAw&sclient=products-cc"
]

dossier_images = 'images'
dossier_donnees = 'donnees'
if not os.path.exists(dossier_images):
    os.makedirs(dossier_images)
if not os.path.exists(dossier_donnees):
    os.makedirs(dossier_donnees)

donnees = []
compteur_total = 0

for url in urls:
    compteur = 0
    page = 0
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(5)
    wait = WebDriverWait(driver, 10)

    try:
        while True:
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            for card in soup.find_all('div', class_='sh-dgr__content'):
                compteur += 1
                compteur_total += 1
                card_img = card.find_all('img')
                for img in card_img:
                    img_src = img.get('src', img.get('data-src', 'n\\a'))
                    info = card.find('h3', class_="tAxDx").text.strip()
                    span_prix_ca = card.find(
                        'span', class_="a8Pemb").text.strip()
                    span_prix_US = card.find('span', class_="hahPbb")
                    prix_us_text = span_prix_US.text.strip(
                    ) if span_prix_US is not None else "n\a"
                    compagne = card.find('div', class_="aULzUe").text.strip()
                    livraison = card.find('div', class_="vEjMR")
                    livraison_text = livraison.text.strip(
                    ) if livraison is not None else "n\a"
                    response = None
                    if img_src.startswith('data:'):
                        print(
                            f"Image {compteur_total} est une image de données (non téléchargée).")
                    else:
                        response = requests.get(img_src)
                        if response.status_code == 200:
                            chemin_dossier = os.path.join(dossier_images)
                            if not os.path.exists(chemin_dossier):
                                os.makedirs(chemin_dossier)
                            nom_image = f"image_{str(compteur_total)}_.jpg"
                            chemin_image = os.path.join(
                                dossier_images, nom_image)
                            try:
                                with open(chemin_image, 'wb') as fichier_image:
                                    fichier_image.write(response.content)
                                classe_aleatoire = random.randint(1, 5)
                                donnees.append([chemin_image, info, span_prix_ca,
                                                prix_us_text, compagne, livraison_text, classe_aleatoire])
                                print(
                                    f"Image {nom_image} téléchargée avec succès.")
                            except Exception as e:
                                print(
                                    f"Échec du téléchargement de l'image {img_src}")
                                print(
                                    f"Nom du fichier problématique : {nom_image}")
                                print(
                                    "-------------------------------------------------------------------------------------------------------")
                        else:
                            print(
                                f"Échec du téléchargement de l'image {img_src}")
                            print(
                                "-------------------------------------------------------------------------------------------------------")
            page += 1
            print(f'\nPages : {page}\n')
            try:
                btnSuvant = WebDriverWait(driver, 20).until(
                    Ec.element_to_be_clickable((By.XPATH, '//span[contains(text(),"Suivant")]')))
                btnSuvant.click()
                time.sleep(8)
            except Exception as e:
                print(f"Erreur lors du clic sur le bouton suivant : {e}")
                break
    finally:
        driver.quit()
df = pd.DataFrame(donnees, columns=[
                  "Chemin_Image", "Nom", "Prix_CA", "Prix_US", "Compagne_Model", "Livraison", "Classe"])
df.to_csv(os.path.join(dossier_donnees, 'donnees_total.csv'), index=False)
print('\n -------------------------------------------------------------------Head rows \n -------------------------------------------------------------------')
print(df.head())
print('\n -------------------------------------------------------------------Tail rows \n -------------------------------------------------------------------')
print(df.tail())
print("Les images et les données ont été enregistrées avec succès dans le dossier et le fichier CSV.")
