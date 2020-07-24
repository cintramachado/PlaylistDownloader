# modulos do selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# modulo pytube permite o download dos videos
from pytube import YouTube
from os import path
import os.path


def delete_saved():
    missing_links = []

    with open("missing_links.dat", "r") as f:
        links = f.readlines()
    f.close()

    for link in links:
        missing_links.append(link.split()[0])
    current = os.getcwd() + "\\information_retrieval"

    for i in missing_links:
        title = get_title(i)
        if path.exists("%s\\%s.mp4" % (current, title)):
            missing_links.remove(i)
            with open("missing_links.dat", "w") as f:
                for link in missing_links:
                    f.write("%s \n" % link)
            f.close()

def retry_missing():
    missing_links = []

    with open("missing_links.dat", "r") as f:
        links = f.readlines()
    f.close()

    for i in links:
        missing_links.append(i.split()[0])

    download_video(missing_links)


def download_video(lista_links):
    for link_video in lista_links:  # faz o download para a pasta de trabalho do Jupyter
        video = YouTube(link_video)
        print("link: %s" % link_video)

        try:
            current = os.getcwd() + "\\information_retrieval"

            # while title == None:
            # title = get_title(link_video)

            print(current)

            video.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download(
                output_path=current)


        except:

            retry_missing()


def get_playlist(site):
    options = webdriver.ChromeOptions()
    options.add_argument("Headless")
    driver = webdriver.Chrome(options=options)  # inicializa o webdriver
    driver.get(site)
    wait = WebDriverWait(driver, 500)  # espera o tempo necessario para o javascript carregar

    lista_links = []  # inicializa a variavel lista_links to tipo lista

    for a in driver.find_elements_by_xpath('//*[@id="wc-endpoint"]'):  # extrai os links
        lista_links.append(a.get_attribute("href"))

    driver.quit()
    return lista_links


if __name__ == "__main__":

    playlist = []
    while (len(playlist) == 0):
        playlist = get_playlist("https://www.youtube.com/watch?v=3Dt_yh1mf_U&list=PLQiyVNMpDLKnZYBTUOlSI9mi9wAErFtFm")
        print("Playlist:")

    with open("missing_links.dat", "w+") as f:
        for i in playlist:
            f.write("%s \n" % i)
            print(i)
    f.close()

    retry_missing()

    delete_saved()
