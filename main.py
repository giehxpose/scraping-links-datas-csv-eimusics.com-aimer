import json
import glob
import pandas as pd
import requests
from bs4 import BeautifulSoup


def get_urls():
    print("Collecting urls...")
    links = []
    for page in range(1, 7):
        req = requests.get(f'https://eimusics.com/artist/aimer/page/{page}/')
        soup = BeautifulSoup(req.content, features='html.parser')
        urls = soup.find_all('div', attrs={'class': 'media mb-4'})
        for url in urls:
            links.append(url.find('a')['href'])
            print("Saving : ", url.find('a')['href'])
    print(f"{len(links)} urls collected!")
    return links


def get_datas(links):
    # linke = 'https://eimusics.com/single-aimer-black-bird-tiny-dancers-omoide-wa-kirei-de-cd-flac-zip2018-09-05/'

    req = requests.get(links)
    soup = BeautifulSoup(req.content, features='html.parser')

    filename = soup.find('h1', attrs={'class': 'mb-3'}).text.strip().replace('/', '_').replace(':', ' ')
    lis = soup.find_all('li', attrs={'class': 'py-1'})
    try:
        artist = lis[0].text.strip().replace('Artist: ', '')
    except:
        artist = 'no artist'
    try:
        category = lis[1].text.strip().replace('Category: ', '')
    except:
        category = 'no category'
    try:
        series = lis[2].text.strip().replace('Series: ', '')
    except:
        series = 'no series'
    dict_data = {
        'File Name': filename,
        'Artist': artist,
        'Category': category,
        'Series': series
    }
    print("Saving : ", dict_data['File Name'])

    file = './results/{}.json'.format(filename)
    with open(file, 'w', encoding="utf-8") as outfile:
        json.dump(dict_data, outfile)


def create_csv():
    print("Converting results to JSON file...")

    files = sorted(glob.glob('./results/*.json'))
    datas = []
    for file in files:
        print(file)
        with open(file) as json_file:
            data = json.load(json_file)
            datas.append(data)

    df = pd.DataFrame(datas)
    df.to_csv('results.csv', index=False)
    print("output files generated!")


def run():
    order = int(input("Hello, Input number to run program;\n1.collect urls\nType number here:"))
    if order == 1:
        links = get_urls()
        order2 = int(input("Waiting to execute next program;\n2.collect datas\nType number here:"))
        if order2 == 2:
            print("Collecting results...")
            for link in links:
                get_datas(link)
            print(f"{len(links)}Datas collected!")
            order3 = int(input("Waiting to execute next program;\n3.creating .csv file\nType number here:"))
            if order3 == 3:
                create_csv()
    else:
        print("Error! Input not available")
    print("Operations done!")


if __name__ == '__main__':
    run()
