import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import tkinter as tk
from tkinter import ttk
import pandas as pd

def get_links(url):
    headers = {'User5.5'}
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()  # Raise an exception for bad responses
    content = response.text
    response.close()

    soup = BeautifulSoup(content, 'html.parser')
    links = soup.find_all('h2', attrs={'itemprop': ['headline']})

    result = []
    for link in links:
        if link.name == 'a':
            title = link.text
            href = link['href']
        else:
            title = link.find('a').text
            href = link.find('a')['href']

        if href.startswith("/"):
            full_link = urljoin(url, href)
        else:
            full_link = href

        title = title.strip().splitlines()[0]
        result.append({'Link': full_link, 'Text': title})

    return result

def display_links_in_gui(links):
    root = tk.Tk()
    root.title("Extracted Links")

    tree = ttk.Treeview(root, columns=('Link', 'Text'), show='headings')
    tree.heading('Link', text='Link')
    tree.heading('Text', text='Text')

    for link_info in links:
        tree.insert('', 'end', values=(link_info['Link'], link_info['Text']))

    tree.pack(expand=tk.YES, fill=tk.BOTH)

    root.mainloop()

if __name__ == "__main__":
    url = "hom"
    extracted_links = get_links(url)

  
    display_links_in_gui(extracted_links)
