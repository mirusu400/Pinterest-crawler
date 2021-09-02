from selenium import webdriver
from pinterest import Pinterest
from sys import exit
from chromedriver import chromedriver_download
import yaml
import os.path
import argparse

if __name__ == "__main__":
    currentdir = os.getcwd()

    # Using argparse
    parser = argparse.ArgumentParser(description='An infinite pinterest crawler. Auther: mirusu400')

    parser.add_argument('-e', '--email', required=False, default="", help='Your Pinterest account email')
    parser.add_argument('-p', '--password', required=False, default="", help='Your Pinterest account password')
    parser.add_argument('-d', '--directory', required=False, default="", help='Directory you want to download')
    parser.add_argument('-l', '--link', required=False, default="", help='Link of Pinterest which you want to scrape')
    parser.add_argument('-g', '--page', required=False, default="", help='Number of pages which you want to scrape')

    args = parser.parse_args()

    email = args.email
    password = args.password
    directory = args.directory
    link = args.link
    pages = args.page
    
    yaml_email = ""
    yaml_password = ""
    yaml_directory = ""
    

    # Check chromedriver exists
    if not os.path.isfile(currentdir + "/chromedriver.exe"):
        print("No chromedriver found! I'll download it automatically..")
        chromedriver_download()

    # Check yaml exists
    if os.path.isfile(currentdir + "/config.yaml"):
        with open("./config.yaml", "r") as f:
            config = yaml.load(f)
            yaml_email = config["email"]
            yaml_password = config["password"]
            yaml_directory = config["directory"]

    if email == "":
        if yaml_email != "":
            email = yaml_email
        else: 
            email = input("Enter your email: ")

    if password == "":
        if yaml_password:
            password = yaml_password
        else: 
            password = input("Enter your password: ")
    
    if directory == "":
        if yaml_directory:
            directory = yaml_directory
        else: 
            directory = input("Enter the directory to save the images (Blank if you set default): ")

    if directory == "":
        directory = "download"

    if pages == "":
        page = input("Enter the number of pages to scrape (Blank if infinity): ")
    if pages == "" or int(pages) == 0:
        pages = 999999
    else:
        pages = int(pages)


    if link == "":
        link = input("Enter the link to scrape (Blank if default; Pinterest main page): ")
    if link == "":
        link = "https://pinterest.com/"

    # Create directory
    if directory[0] == "/":
        directory = directory[1:]
    directory = os.path.join(currentdir, directory)
    if not os.path.exists(directory):
        os.mkdir(directory)

    print("Open selenium...")
    p = Pinterest(email, password)

    print("Download Image")
    p.crawl(pages, link, directory)
