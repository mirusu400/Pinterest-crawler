from selenium import webdriver
from pinterest import Pinterest
from sys import exit
from exceptions import *
import chromedriver_autoinstaller
import json
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
    parser.add_argument('-b', '--batch', required=False, default=False, action="store_true", help='Enable batch mode (Please read README.md!!)')
    args = parser.parse_args()

    email = args.email
    password = args.password
    directory = args.directory
    link = args.link
    pages = args.page
    batch = args.batch
    
    yaml_email = ""
    yaml_password = ""
    yaml_directory = ""
    

    # Check chromedriver exists
    chromedriver_autoinstaller.install()

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
    
    dir_list = []
    link_list = []
    if batch != False:
        print("Batch mode Enabled. You will download a bunch of Images..")
        if not os.path.exists(currentdir + "/batch.json"):
            print("Batch.json file not found! Please read README.md...")
            exit()
        batch_list = json.loads(open(currentdir + "/batch.json").read())
        for item in batch_list:
            dir_list.append(item["dir"])
            link_list.append(item["link"])
    else:
        if directory == "":
            if yaml_directory:
                directory = yaml_directory
            else: 
                directory = input("Enter the directory to save the images (Blank if you set default): ")
        if directory == "":
            directory = "download"

        if link == "":
            link = input("Enter the link to scrape (Blank if default; Pinterest main page): ")
        if link == "":
            link = "https://pinterest.com/"

    if pages == "":
        page = input("Enter the number of pages to scrape (Blank if infinity): ")
    if pages == "" or int(pages) == 0:
        pages = 999999
    else:
        pages = int(pages)


    print("Open selenium...")
    p = Pinterest(email, password)

    if batch == False:
        print("Download Image")
        p.single_download(pages, link, directory)
    
    else:
        print("Download Image in Batch mode...")
        p.batch_download(pages, link_list, dir_list)

