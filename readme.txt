###########################################################################
#
# ASAT4J 
# APPLICATION SERVER ASSESSMENT TOOL FOR JAVA
# Author:  Marco Righetti (marco.righetti@oracle.com)
# Date: Oct-2010
#
# Application Server Assessment Tool for Java is the first initiave scripting to garthering
# App Server infrastructure where
#
# 1- customer has huge App Server Deployments (WebLogic and IAS)
# 2- customer can be driven for App Server Standardization Initiative
# 3- customer inventory data for App server deployment is not trustable
# 4- customer does not have Grid Control for App Server
# 5- customer does not want intrusive assessment tools
#
##################################################################################

About version 1.0

- This version has been tested in a real customer environment to help ULAxBAU decision making
- This version is WLST based (applies only for WebLogic, version 9.x and higher)
- This version has basic information for scripting (domain topology and deployed apps)
- This version has monitor scripting to help to investigate Coherence Value Proposition for Web Apps

Future versions

- output data file management
- crypto passwords utility for domains.txt file
- Support WLS 8.x
- Support IAS 10.x


Basic usage instructions

- this scripting has been tested under Windows XP
- Install WLS binaries (WLST Jython scripting needs WLST. Scripting has been tested with WLS 10.3.3)
- Unzip ASAT4J_1_0.zip in any directory for your preference (D:\inventoryWLS, for example)
- Open general.properties file
- This file must have your system parameters (paths)
- Script inventoryData get all WLS JVM instance data per domain. So, its execution is coordinated by InventoryWLS.txt file
- Change domains.txt to have all ip:port, user and password for each domain that you want to get
- run setWLSEnv.cmd under your WLS installation directory
- run java weblogic.WLST inventoryData.py

- Inventory Data is available at inventoryWLS.txt
- Any JMX access error is generated at domainsToReview.txt
- One directory is create for each domain where deployedApps.txt data is available

- after that, monitor.py can be run for a specific time of day (check session RUNTIME at general.properties to monitor control) 

