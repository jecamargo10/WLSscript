# WLSscript
Script for getting the Inventory of Applications, Resources and Monitor a WLS Domain via JMX
## Requirementes

* Have an installation of a Weblogic Server in the machine that is going to run the scripts 
* Have network access to the AdminServer
* Access to the domains that are going to be analyzed
* The path in which the script is run, should have execution permision

## How to run this Script

1. Edit the file general.properties
  >* **pathDomainsWLS:** File path containing domain information. E.g. C:\test\domains.txt. This file must be edited later.
  >* **pathInventoryWLS:** File path where the result of the revision to a domain will be placed. E.g. C:\test\InventoryWLS.txt.
  >* **pathConnectionProblems:** File path where the StackTrace of the error while running the script will be placed
  >* **appsDomainInv:** Name of the file that will have the data of the deployed Apps
  >* **monitorDomain:** Name of the file that will have the results of the monitoring
  >* **dataSourcersDomainInv:** Name of the file that will have the DataSource results
  >* **scriptHome:** The root folder of the script
  >* **monitorIntervalMils:** Is adjusted to determine how often values are monitored on the server. E.g. monitorIntervalMils = 60000 is equivalent to establishing that it is monitored every hour
  >* **hoursToMonitor:** It is set for how long you want to monitor the server. This variable accepts integer or decimal values. Eg hoursToMonitor = 0.25 equals 15 minutes of one hour
2. Edit the File domains.txt, this file has the data of the AdminServer of each domain that is going to be monitored (it allows multiple servers)
It has the following structure AdminURL,user,password
3. Run the file setWLSEnv.cmd in the WebLogic installation
4. Open the path in which the script is located
5. Run the following command:
`java -classpath /PATH_TO_WLS/weblogic.jar -Dweblogic.security.SSL.ignoreHostnameVerification=true -Dweblogic.security.TrustKeyStore=DemoTrust weblogic.WLST   /PATH_TO_SCRIPT/inventoryData.py `

The Dweblogic parameters are requires when WLS has configure a connetion with t3s
