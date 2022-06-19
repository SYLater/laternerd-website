import csv
import os
import re
import time
# from bs4 import BeautifulSoup
import unittest
from csv import DictWriter, reader, writer
from lib2to3.pgen2.driver import Driver
from pickle import FALSE
from tkinter import W
import pandas as pd
from flask import (Blueprint, flash, redirect, render_template, request,
                   send_from_directory, url_for)
from flask_login import current_user, login_required, login_user, logout_user
from helium import *
from selenium import webdriver
from selenium.webdriver.chrome import options
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common import by
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.expected_conditions import \
    presence_of_element_located
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from sqlalchemy import false, true
from tabulate import tabulate
from werkzeug.security import check_password_hash, generate_password_hash
from . import db
from .models import Suggestions, User


simon = Blueprint('simon', __name__)


@simon.route('/bettersimonlogin', methods=['GET', 'POST'])
@login_required
def bettersimon():
    if request.method == 'POST':

        updated_values_dict = request.form.to_dict()
        paduaEmail = request.form.get('paduaemail')
        paduaPassword = request.form.get('paduapassword')
        user = User.query.filter_by(id=current_user.id).first()

        if AuthenticateUser(paduaEmail, paduaPassword):
            for k, v in updated_values_dict.items():
                if k == 'paduaEmail':
                    user.paduaEmail = v.rstrip()
                if k == 'paduaPassword':
                    user.paduaPassword = v.rstrip()

            db.session.commit()
            flash('Account created!', category='success')
            return render_template('alldata.html', user=current_user)
        else:
            flash('User not found.', category='error') 
    return render_template('bettersimonlogin.html', user=current_user)

@simon.route('/bettersimonload', methods=['GET', 'POST'])
@login_required
def bettersimonload():
    if request.method == 'POST':
            cells()
    return render_template('bettersimonload.html', user=current_user)

# WebDriver Location = C:\Users\notje\AppData\Local\Programs\Python\Python39\Lib\site-packages\helium\_impl\webdrivers\windows
driver = start_chrome(headless=True)
TimeTable = ('https://intranet.padua.vic.edu.au/WebModules/Timetables/StudentTimetable.aspx')
rows = len(driver.find_elements_by_xpath("//*[@id='ContentPlaceHolder1_KeysPanel']/div[1]/table/tbody/tr"))
before_XPath = "//*[@id='ContentPlaceHolder1_KeysPanel']/div[1]/table/tbody/tr["
aftertd_XPath_1 = "]/td[1]"
aftertd_XPath_2 = "]/td[2]"
aftertd_XPath_3 = "]/td[3]"
aftertd_XPath_5 = "]/td[5]"

def cells():
    driver.get('https://intranet.padua.vic.edu.au/Login/Default.aspx?ReturnUrl=%2F')
    email = User.paduaemail.text
    write(email)
    write(User.query.filter_by(user.paduapassword).first())
    click('Sign in')
    updated_values_dict = request.form.to_dict()
    user = User.query.filter_by(id=current_user.id).first()
    TimeTable = ('https://intranet.padua.vic.edu.au/WebModules/Timetables/StudentTimetable.aspx')
    rows = len(driver.find_elements_by_xpath("//*[@id='ContentPlaceHolder1_KeysPanel']/div[1]/table/tbody/tr"))
    before_XPath = "//*[@id='ContentPlaceHolder1_KeysPanel']/div[1]/table/tbody/tr["
    aftertd_XPath_1 = "]/td[1]"
    aftertd_XPath_2 = "]/td[2]"
    aftertd_XPath_3 = "]/td[3]"
    aftertd_XPath_5 = "]/td[5]"
    driver.get(TimeTable)
    PrintTimeTable = driver.find_element_by_id('ContentPlaceHolder1_ContentPlaceHolder1_PrintTimetable')
    click(PrintTimeTable)
    for t_row in range(2, (rows + 1)):
        FinalXPath = before_XPath + str(t_row) + aftertd_XPath_1
        cell_classcodes = driver.find_element_by_xpath(FinalXPath).text
        user.classcodes = cell_classcodes
        db.session.commit()
    for t_row in range(2, (rows + 1)):
        FinalXPath = before_XPath + str(t_row) + aftertd_XPath_2
        cell_classnames = driver.find_element_by_xpath(FinalXPath).text
        new_classnames = User(classnames=cell_classnames)
        db.session.commit(new_classnames)   
    for t_row in range(2, (rows + 1)):
        FinalXPath = before_XPath + str(t_row) + aftertd_XPath_3
        cell_Domain = driver.find_element_by_xpath(FinalXPath).text
    for t_row in range(2, (rows + 1)):
        FinalXPath = before_XPath + str(t_row) + aftertd_XPath_5
        cell_Teachers = driver.find_element_by_xpath(FinalXPath).text

def AuthenticateUser(paduaemail, paduapassword) :
    driver.get('https://intranet.padua.vic.edu.au/Login/Default.aspx?ReturnUrl=%2F')
    write(paduaemail, into='Username')
    write(paduapassword, into='Password')
    click('Sign in')
    try:
        wait = WebDriverWait(driver, 3)
        wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div')))
        print('worked')
        driver.get(TimeTable)
        PrintTimeTable = driver.find_element_by_id('ContentPlaceHolder1_ContentPlaceHolder1_PrintTimetable')
        click(PrintTimeTable)
        for t_row in range(2, (rows + 1)):
            FinalXPath = before_XPath + str(t_row) + aftertd_XPath_1
            cell_classcodes = driver.find_element_by_xpath(FinalXPath).text
            print(cell_classcodes)
            User.classcodes = cell_classcodes
            db.session.commit()
        for t_row in range(2, (rows + 1)):
            FinalXPath = before_XPath + str(t_row) + aftertd_XPath_2
            cell_classnames = driver.find_element_by_xpath(FinalXPath).text
            new_classnames = User(classnames=cell_classnames)
            db.session.commit(new_classnames)   
        for t_row in range(2, (rows + 1)):
            FinalXPath = before_XPath + str(t_row) + aftertd_XPath_3
            cell_Domain = driver.find_element_by_xpath(FinalXPath).text
        for t_row in range(2, (rows + 1)):
            FinalXPath = before_XPath + str(t_row) + aftertd_XPath_5
            cell_Teachers = driver.find_element_by_xpath(FinalXPath).text
        driver.close()
        return True
    except Exception:
        print('cope')
        driver.close()
    

       

    

        
