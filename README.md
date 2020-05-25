# MSM3500-SIP-TAP
Multi System Messaging build for SIP Messaging conversion to TAP 1.8 message protocol. 
This system is built to integrate SIP outputs typically from nurse call to a ethernet or USB input paging system. The system uses asterisk agi to convert the incomming SIP message to a TAP message which then send the message to your User Device. 

# Prerequisites

  Asterisk Version 14 or higher

# Installation 

This document assumes you have knowledge of install the prerequsites.

Install Asterisk - https://wiki.asterisk.org/wiki/display/AST/Installing+Asterisk
  Please see installing Asterisk from source or any other installtion you would like.

    sudo apt-get update
    
    git clone https://github.com/msaiko239/MSM3500-SIP-TAP.git

    cd MSM3500-SIP-TAP
    
    sudo chmod 777 install.sh

    sudo ./install.sh

This will download Python Version 3.6 if you would like a newer version please edit the install.sh file accordingly

This will install php and all necessary requirements. 

This will copy all the contents of the repo to your local server and create all directorys and change permissions needed.

# Testing Integration
To test the integration to your server navigate to http://"your server ip"/config.php

Enter the IP or USB settings of your paging system and hit update ini.

from the cli of your server enter the command

    python3 /var/lib/asterisk/agi-bin/test_SIP-TAP-Ethernetpage.py '<phone-you-want-to-send-to>' '<Message-Text>'
    python3 /var/lib/asterisk/agi-bin/test_SIP-TAP-USBserial.py '<phone-you-want-to-send-to>' '<Message-Text>'
    
Example

    python3 /var/lib/asterisk/agi-bin/test_SIP-TAP-Ethernetpage.py '1234' 'Hello this is a test'
    python3 /var/lib/asterisk/agi-bin/test_SIP-TAP-USBserial.py '1234' 'Hello this is a test'
    
# Enabling SIP to TAP in asterisk. 
This needs to be completed in the CLI. You will need to edit the file /etc/asterisk/extensions.conf and add the following lines to the context you are using.

;Using the SIP-TAP Scripts
;USB paging output
exten => 100,1,NoOP(${CALLERID(NAME)})
exten => 100,2,AGI(SIP-TAP-USBserial.py)
exten => 100,n,Hangup

;Ethernet paging output
exten => 101,1,NoOP(${CALLERID(NAME)})
exten => 101,2,AGI(SIP-TAP-Ethernetpage.py)
exten => 101,n,Hangup

;Both script to trigger to send to USB and Ethernet paging encoder.
;exten => (extension number or range),1,NoOP(${CALLERID(NAME)})
;exten => (extension number or range),2,AGI(siptapusb.agi)
;exten => (extension number or range),2,AGI(siptapeth.agi)
;exten => (extension number or range),n,Hangup

