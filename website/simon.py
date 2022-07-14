import csv
import json
import os
from pydoc import classname
import re
from sre_constants import SUCCESS
import time
# from bs4 import BeautifulSoup
import unittest
from csv import DictWriter, reader, writer
from lib2to3.pgen2.driver import Driver
from pickle import FALSE
from tkinter import W
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
from .models import Suggestions, User, Padua


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
                if k == 'paduaemail':
                    user.paduaEmail = v.rstrip()
                if k == 'paduapassword':
                    user.paduaPassword = v.rstrip()

            db.session.commit()
            
            flash('Account created!', category='success')
            return render_template('account.html', user=current_user)
        else:
            
            flash('User not found.', category='error') 
    return render_template('bettersimonlogin.html', user=current_user)

@simon.route('/bettersimonload', methods=['GET', 'POST'])
@login_required
def bettersimonload():
    user = User.query.filter_by(id=current_user.id).first()
    padua = Padua.query.filter_by(parent_id=current_user.id).first()
    # data13 = json.loads(user.classCodes)
    print(padua.classCodes)
    if padua.classCodes:
        classCodes = json.loads(padua.classCodes)
    else:
        classCodes = 'nothing'
    if padua.classNames:
        classNames = json.loads(padua.classNames)
    else:
        classNames = 'nothing'
    if padua.classDomain:
        classDomain = json.loads(padua.classDomain)
    else:
        classDomain = 'nothing'
    if padua.Grades:
        Grades = json.loads(padua.Grades)
    else:
        Grades = 'nothing'
    if padua.paduaName:
        paduaName = padua.paduaName
    else:
        paduaName = 'nothing'
    if request.method == 'POST':
        if request.form['submit_button'] == 'Grades':
            print('Grades')
            grades()
        elif request.form['submit_button'] == 'class':
            print('class')
            # cells()
    return render_template('bettersimonload.html', user=current_user, classCodes=classCodes, classNames=classNames, classDomain=classDomain,Grades=Grades,paduaName=paduaName, len=len,str=str)

# WebDriver Location = C:\Users\notje\AppData\Local\Programs\Python\Python39\Lib\site-packages\helium\_impl\webdrivers\windows

TimeTable = ('https://intranet.padua.vic.edu.au/WebModules/Timetables/StudentTimetable.aspx')
before_XPath = "//*[@id='ContentPlaceHolder1_KeysPanel']/div[1]/table/tbody/tr["
aftertd_XPath_1 = "]/td[1]"
aftertd_XPath_2 = "]/td[2]"
aftertd_XPath_3 = "]/td[3]"
aftertd_XPath_5 = "]/td[5]"
def cells():
    user = User.query.filter_by(id=current_user.id).first()
    driver = start_chrome(headless=False)
    driver.get('https://intranet.padua.vic.edu.au/Login/Default.aspx?ReturnUrl=%2F')
    write(user.paduaEmail, into='Username')
    write(user.paduaPassword, into='Password')
    click('Sign in')
    updated_values_dict = request.form.to_dict()
   
    TimeTable = ('https://intranet.padua.vic.edu.au/WebModules/Timetables/GenericStudentTimetable.aspx')

    before_XPath = "//*[@id='ContentPlaceHolder1_KeysPanel']/div[1]/table/tbody/tr["
    aftertd_XPath_1 = "]/td[1]"
    aftertd_XPath_2 = "]/td[2]"
    aftertd_XPath_3 = "]/td[3]"
    aftertd_XPath_5 = "]/td[5]"
    driver.get(TimeTable)
    PrintTimeTable = driver.find_element_by_id('ContentPlaceHolder1_ContentPlaceHolder1_PrintTimetable')

    click(PrintTimeTable)
    NoOfrows= len(driver.find_elements_by_xpath("//*[@id='ContentPlaceHolder1_KeysPanel']/div[1]/table/tbody/tr"))
    print('There are ' + str(NoOfrows) + ' rows')

    classcodeslst = []
    for t_row in range(2, (NoOfrows+ 1)):
        FinalXPath = before_XPath + str(t_row) + aftertd_XPath_1
        classcodes = driver.find_element_by_xpath(FinalXPath).text
        ClassNo = 'class'+str(t_row -1) 
        classcodestr = str( '"'+ str(ClassNo) + '":"' + str(classcodes) + '"')
        classcodeslst.append (str(classcodestr))
        #formats to usable data
        last = str(classcodeslst).replace("'",'').replace("[", "{").replace("]", "}")
        data1 = json.dumps(str(last))
        data = json.loads(str(data1))
        user.classCodes = data
    
    classNamelst = []
    for t_row in range(2, (NoOfrows+ 1)):
        FinalXPath = before_XPath + str(t_row) + aftertd_XPath_2
        classNames = driver.find_element_by_xpath(FinalXPath).text
        ClassNo = 'class'+str(t_row -1) 
        classNamestr = str( '"'+ str(ClassNo) + '":"' + str(classNames) + '"')
        classNamelst.append (str(classNamestr))
        #formats to usable data
        last = str(classNamelst).replace("'",'').replace("[", "{").replace("]", "}")
        data1 = json.dumps(str(last))
        data = json.loads(str(data1))
        user.classNames = data

    classDomainlst = []  
    for t_row in range(2, (NoOfrows+ 1)):
        FinalXPath = before_XPath + str(t_row) + aftertd_XPath_3
        classDomain = driver.find_element_by_xpath(FinalXPath).text
        ClassNo = 'class'+str(t_row -1) 
        classDomainstr = str( '"'+ str(ClassNo) + '":"' + str(classDomain) + '"')
        classDomainlst.append (str(classDomainstr))
        #formats to usable data
        last = str(classDomainlst).replace("'",'').replace("[", "{").replace("]", "}")
        data1 = json.dumps(str(last))
        data = json.loads(str(data1))
        user.classDomain = data
 
    db.session.commit()
    print('Executed cells')
    driver.close()

def grades():
    user = User.query.filter_by(id=current_user.id).first()
    url = ('https://intranet.padua.vic.edu.au/Login/Default.aspx?ReturnUrl=%2F')
    Grades = ('https://intranet.padua.vic.edu.au/WebModules/LearningAreas/LearningAreasWorkDesk.aspx')

    driver = start_chrome(headless=False)
    driver.get(url)
    driver.delete_all_cookies()
    WebDriverWait(driver, 10)
    write(user.paduaEmail, into='Username')
    write(user.paduaPassword, into='Password')
    click('Sign in')
    
    driver.get(Grades)
    dropdown= Select(driver.find_element_by_xpath('//*[@id="classesTab"]/select[1]'))
    
    wait = WebDriverWait(driver, 60)
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="classesTab"]/select[1]/option[2]')))
    time.sleep(1)
    dropdown.select_by_visible_text('2022, Semester 1')
    classes = driver.find_element_by_xpath('//*[@id="primaryScrollPanel"]/div/div[2]/ul/li[1]')
    results = driver.find_element_by_xpath('//*[@id="primaryScrollPanel"]/div/div[2]/ul/li[5]')
    time.sleep(1)
    click(results)
    time.sleep(1)

    DropDown_before_XPath = '//*[@id="resultsTab"]/div[1]/div['
    DropDown_aftertd_XPath_1 = "]/div[1]/span[3]"
    DropDown_aftertd_XPath_2 = "]/div[1]/span[1]"

    SubjectClass_before_XPath = "//*[@id='SubjectClass"
    SubjectClass_after_XPath_1 = "']/ul/li"

    Noclasses = len(driver.find_elements_by_xpath("//*[@id='resultsTab']/div[1]/div"))
    print("you have " + (str(Noclasses)) + " classes with results")
    classNamelst = []
    for t_row1 in range((Noclasses)):
        subjectclasses = SubjectClass_before_XPath + str(t_row1) + SubjectClass_after_XPath_1
        print("class "+str(t_row1))

        Nogrades = len(driver.find_elements_by_xpath(subjectclasses))

        Dropdownclick = DropDown_before_XPath + str(t_row1 + 1) + DropDown_aftertd_XPath_1
        classname = DropDown_before_XPath + str(t_row1 + 1) + DropDown_aftertd_XPath_2
        classnameText = driver.find_element_by_xpath(classname).text
        click(driver.find_element_by_xpath(Dropdownclick))
        time.sleep(0.5)

        print("you have "+(str(Nogrades))+" results")

        Grades_before_XPath = subjectclasses + "["
        Grades_aftertd_XPath_1 = "]/span[1]"
        Grades_aftertd_XPath_2 = "]/a/span[3]"

        
        for t_row in range(1, (Nogrades+1)):
            Grades_Xpath = Grades_before_XPath + str(t_row) + Grades_aftertd_XPath_1
            Assesment_Xpath = Grades_before_XPath + str(t_row) + Grades_aftertd_XPath_2
            Grades = driver.find_element_by_xpath(Grades_Xpath).text
            Assesment = driver.find_element_by_xpath(Assesment_Xpath).text
            classDomainstr = str('"' + str(Grades) + '"')
            classNamelst.append (str(classDomainstr))
            #formats to usable data
        # last = '"'+ classnameText + '":'+ str(classNamelst).replace("'",'')
        last =  str(classNamelst).replace("'",'').replace("[", "")
        data1 = json.dumps(str(last))
        data = json.loads(str(data1))
        Final = ('{"Grades":['+data + '}') 
        user.Grades = Final
    db.session.commit()
    print('Executed cells')
    driver.close()

def AuthenticateUser(paduaemail, paduapassword) :
    user = User.query.filter_by(id=current_user.id).first()
    driver = start_chrome(headless=False)
    
    driver.get('https://intranet.padua.vic.edu.au/Login/Default.aspx?ReturnUrl=%2F')
    write(paduaemail, into='Username')
    write(paduapassword, into='Password')
    click('Sign in')

    try:
        wait = WebDriverWait(driver, 3)
        wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div')))
        def name():
            time.sleep(5)
            sidepanel4  = driver.find_element(By.XPATH, "//*[@id='app']/div[1]/header/div/button[3]")
            sidepanel4.click()
            time.sleep(5)
            name = driver.find_element_by_xpath('//*[@id="app"]/div[2]/nav/div[1]/div[1]/div[2]/span').text
            user.paduaName = name
            print(name)
            print('worked')
        name()
        driver.close()
        return True
    except Exception:
        print('cope')
        driver.close()

    

       

    

        
