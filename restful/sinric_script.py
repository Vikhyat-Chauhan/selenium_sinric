import sys
import json
import time
import pandas as pd
import paho.mqtt.client as paho
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC

broker = "15.206.160.77" #"m12.cloudmqtt.com"
username = "thenextmove"
password = "t1n2m3@TNM"
port = 1883

options = Options()
options.add_argument('--no-sandbox')
options.add_argument('--window-size=1420,1080')
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--allow-running-insecure-content')
options.add_argument('--ignore-certificate-errors')
#options.binary_location = "/usr/local/bin/"
driver = webdriver.Chrome(chrome_options=options)

def login(email,password):
    driver.get("https://www.sinric.com")
    #print(driver.title)
    # Select the id box
    email_box = driver.find_element_by_id('mat-input-0')
    # Find password box
    pass_box = driver.find_element_by_id('mat-input-1')
    # Find login button
    login_button = driver.find_elements_by_tag_name('button')
    # Send id information
    email_box.send_keys(email)
    # Send password
    pass_box.send_keys(password)
    # Click login
    login_button[0].click()

def get_apikey():
    #Prerequest is that you must be on the logged in, hence call after login(email,password) function
    # Find with api key that is in <p> element 
    for i in range(0,10,1):
        time.sleep(1)
        #print(i)
        if(driver.find_elements_by_tag_name('h1')):
            break
    api_key = driver.find_elements_by_tag_name('p')
    return api_key[0].text

def get_deviceid_list(chipid):
    #Prerequest is that you must be on the logged in, hence call after login(email,password) function
    device_name = driver.find_elements_by_xpath("//mat-card-header[@class='mat-card-header']//mat-card-title[@class='mat-card-title']")
    device_id = driver.find_elements_by_xpath("//mat-card-header[@class='mat-card-header']//mat-card-subtitle[@class='mat-card-subtitle']")
    output_list = [] #structure will be [id1,id2]
    for x in range(2,len(device_name),1):
        details = (device_name[x].text).split('$') #lets spilit html text the device_name which is seprated by Name$CHIPID (Switch)
        name = details[0]
        chip = ((details[1]).split(' '))[0] #Getting Chipid from CHIPID (Switch)
        type = ((details[1]).split(' '))[1]
        id = ((device_id[x].text).split(": "))[1]
        if(chip == chipid):
            output_list.append(id)
            #print(name)
        #print(chip)
        #print(type)
        #print(id)
    print(output_list)
    return output_list

def del_device_list(chipid):
    #Prerequest is that you must be on the logged in, hence call after login(email,password) function
    x = 2
    time.sleep(5)
    while(1):
        device_name = driver.find_elements_by_xpath("//mat-card[@class='device-card side mat-card']/mat-card-header[@class='mat-card-header']//mat-card-title[@class='mat-card-title']")
        device_delete_button = driver.find_elements_by_xpath("//mat-card[@class='device-card side mat-card']/mat-card-actions[@class='mat-card-actions']//button[@class='mat-icon-button mat-primary']")
        if(len(device_name)<2):
            break
        if(x == len(device_name)):
            break
        details = (device_name[x].text).split('$') #lets spilit html text the device_name which is seprated by Name$CHIPID (Switch)
        name = details[0]
        chip = ((details[1]).split(' '))[0] #Getting Chipid from CHIPID (Switch)
        if(chip == chipid):
            print("Deleting " + name + " with Chipid " + chip)
            device_delete_button[(x-2)*2].click()
            time.sleep(5)
            x=x-1
        x=x+1

def add_device(devicename,devicedescription,devicetype):
    #Prerequest is that you must be on the logged in, hence call after login(email,password) function
    for i in range(0,10,1):
        time.sleep(1)
        #print(i)
        if(driver.find_elements_by_tag_name('h1')):
            break
    #print("Found h1")
    # Find add Device button
    all_button = driver.find_elements_by_tag_name('button')
    # Click add Device
    all_button[3].click()
    #print("Pressing Add Device Button")
    #Now we need to wait till the time add device page has loaded hence adding a checking statemnt for friendlyname element
    # Wait till we find friendly name element
    for i in range(0,10,1):
        time.sleep(1)
        #print(i)
        if(driver.find_elements_by_name('friendlyName')):
            break
    # Select the devicename box
    devicename_box = driver.find_element_by_xpath("//input[@placeholder='Friendly Name (Alexa invocation name)']")#driver.find_element_by_id('mat-input-3')            #name('friendlyName')
    #add the device name to the input
    devicename_box.send_keys(devicename)
    # Select the lastname box
    devicedescription_box = driver.find_element_by_xpath("//input[@placeholder='Description']")#driver.find_element_by_id('mat-input-4')     #name('description')  #this is failing
    #add the device description to the input
    devicedescription_box.send_keys(devicedescription)
    # Select the device type dropdown
    for i in range(0,10,1):
        time.sleep(1)
        #print(i)
        if(driver.find_element_by_xpath("//mat-select[@placeholder='Device Type']")):
            break
    devicetype_box = driver.find_element_by_xpath("//mat-select[@placeholder='Device Type']")
    devicetype_box.click()
    for i in range(0,10,1):
        time.sleep(1)
        #print(i)
        if(driver.find_element_by_xpath("//mat-option[@role='option']")):
            break
    if(devicetype == "Switch"):
        devicetype_dropbox = driver.find_element_by_xpath("//mat-option[@role='option']")
        devicetype_dropbox.click()
    # Select the Save button 
    all_button = driver.find_elements_by_tag_name('button')
    # Click Save Button
    all_button[0].click()
    time.sleep(1)
    

def register(firstname,lastname,email,password):
    driver.get("https://www.sinric.com")
    #print(driver.title)
    # Find regiter button
    all_button = driver.find_elements_by_tag_name('button')
    # Click register
    all_button[1].click()
    # Select the firstname box
    firstname_box = driver.find_element_by_id('mat-input-2')
    # Select the lastname box
    lastname_box = driver.find_element_by_id('mat-input-3')
    # Select the id box
    email_box = driver.find_element_by_id('mat-input-4')
    # Find password box
    pass_box = driver.find_element_by_id('mat-input-5')
    # Send firstname information
    firstname_box.send_keys(firstname)
    # Send lastname information
    lastname_box.send_keys(lastname)
    # Send id information
    email_box.send_keys(email)
    # Send password
    pass_box.send_keys(password)
    # Find submit button
    all_button = driver.find_elements_by_tag_name('button')
    # Click register
    all_button[0].click()
    
def login_or_register(firstname,lastname,email,password):
    print("Trying to Login or Register with credential : "+email+" & "+password)
    login(email,password)
    # Wait till we find friendly name element
    for i in range(0,10,1):
        time.sleep(2)
        #print(i)
        if(driver.find_element_by_tag_name('alert')):
            break
    if((driver.find_element_by_tag_name('alert').text) == "User not found"):
        #print("User is not found, reload pages and registering")
        register(firstname,lastname,email,password)
        time.sleep(2)
        login(email,password)
    else:
        time.sleep(1)
        print("Logged in successfully")
    #perform your logged in tasks here


def mqttsend_apikey(chipid):
    client.publish(str(chipid)+'ESP/system/sinricapi/',get_apikey(),0,True)

def mqttsend_get_deviceid_list(chipid):
    devices_ids = get_deviceid_list(chipid)
    for i in range(0,len(devices_ids),1):
        print(devices_ids[i])
        client.publish(str(chipid)+"ESP/system/sinricrelayid/"+str(i+1)+"/",devices_ids[i],0,True)

#define callback
def on_message(client, userdata, message):
    print("received message =",message.topic + "-->" + str(message.payload.decode("utf-8")))

def echocredentials_device(username,password,chipid):
    login_or_register("Firstname","Lastname",username,password)
    mqttsend_apikey(chipid)
    mqttsend_get_deviceid_list(chipid)
    driver.close()

def add_new_device(username,password,chipid,switches):
    login_or_register("Firstname","Lastname",username,password)
    print(switches)
    del_device_list(chipid)
    for i in switches:
        add_device(str(i)+"$"+chipid,("TNM Relay Device"),"Switch")
        time.sleep(0.5)
    mqttsend_apikey(chipid)
    mqttsend_get_deviceid_list(chipid)
    driver.close()

client = paho.Client("server-001") #create client object client1.on_publish = on_publish #assign function to callback client1.connect(broker,port) #establish connection client1.publish("house/bulb1","on")
#Bind function to callback
client.on_message=on_message
#print("connecting to broker ",broker)
client.username_pw_set(username,password)#("wbynzcri","uOIqIxMgf3Dl")
client.connect(broker,port,60)#connect12233
client.loop_start() #start loop to process received messages
print("Started MQTT Communication")

email = sys.argv[1]
password = sys.argv[2]
chipid = sys.argv[3]
codename = sys.argv[4]
switches = []
for i in range(5,len(sys.argv),1):
    print(sys.argv[i]) 
    switches.append(sys.argv[i])
#echocredentials_device(json_file["email"],json_file["password"],json_file["chipid"])
add_new_device(email,password,chipid,switches)
#login_or_register("name","lastname","opschauhan1954@gmail.com","TNMcz0Qh7")
    



