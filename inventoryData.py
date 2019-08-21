
#Conditionally import wlstModule only when script is executed with jython
if __name__ == '__main__':
    from wlstModule import *#@UnusedWildImport

from ConfigParser import ConfigParser
from java.util import Date
from java.text import DateFormat
import os


adminsFile = ""
inventoryWLS = ""
pathConnectionProblems = ""


def getProperties():

    # Declare Properties Parameters
    global adminsFile
    global inventoryWLS
    global pathConnectionProblems
    global appsDomainInv
    global scriptHome
    global dataSourcersDomainInv


    properties = "general.properties"
    cfg = ConfigParser()
    cfg.read(properties)
    adminsFile = cfg.get("Files", "pathDomainsWLS")
    inventoryWLS = cfg.get("Files", "pathInventoryWLS")
    pathConnectionProblems = cfg.get("Files", "pathConnectionProblems")
    appsDomainInv = cfg.get("Files","appsDomainInv")
    scriptHome = cfg.get("Runtime","scriptHome")
    dataSourcersDomainInv = cfg.get("Files","dataSourcersDomainInv")

def getBasicInformation():
    print 'starting the script for ', adminServerAddress, '....'
    username = adminUser
    password = adminPassword
    url = adminServerAddress
    try:
        connect(username,password,url)
        binaryVersion = cmo.getConfigurationVersion()
        domainRuntime()
        serverNames = domainRuntimeService.getServerRuntimes()
        domainName = cmo.getName()
        print 'Getting data from domain ' , domainName
        w = open(inventoryWLS,"a")
        for s in serverNames:
            cd("/ServerRuntimes/"+s.getName())
            serverName = cmo.getName()
            serverState = cmo.getState()
            activationTime = cmo.getActivationTime()
            currentDirectory = cmo.getCurrentDirectory()
            valueThisIsAdminServer = cmo.isAdminServer()
            if valueThisIsAdminServer:
                thisAdminServer = "true"
            else:
                thisAdminServer = "false"
            currentMachine = cmo.getCurrentMachine()
            listenAddress = cmo.getListenAddress()
            listenPort = cmo.getListenPort()
            socketsOpenedTotalCount = cmo.getSocketsOpenedTotalCount()
            cd("/ServerRuntimes/"+s.getName()+ "/JVMRuntime/"+s.getName())
            javaVendor = cmo.getJavaVendor()
            javaJVMDescription = cmo.getType()
            javaVersion = cmo.getJavaVersion()
            if javaJVMDescription == "JRockitRuntime":
                numberOfProcessors = cmo.getNumberOfProcessors()
            else:
                numberOfProcessors = 0
            osJvmName = cmo.getOSName()
            osJvmVersion = cmo.getOSVersion()
            heapSizeMax = cmo.getHeapSizeMax()

            # write inventory data for this instance jvm
            timeStamping = Date()
            timeToShow = DateFormat.getDateTimeInstance(DateFormat.SHORT,DateFormat.SHORT).format(timeStamping);

            infoLineForServerInstance = str(domainName) + "|" + str(timeToShow) + "|" + str(serverName) + "|" + str(listenAddress) + "|" + str(listenPort) + "|" + str(serverState) + "|" + str(binaryVersion) + "|" + str(currentDirectory) + "|" + str(thisAdminServer) + "|" + str(currentMachine) + "|" +  str(activationTime) + "|" + str(socketsOpenedTotalCount) + "|" + str(javaVendor) +"|" + str(javaJVMDescription) + "|" + str(javaVersion) + "|" + str(osJvmName) + "|" + str(osJvmVersion) + "|" + str(numberOfProcessors) + "|" + str(heapSizeMax) + "\n"
            infoServerToWrite = infoLineForServerInstance
            w.write(infoServerToWrite)

        w.close()
        # Now, get applications deployed on Domain in specific directory
        dir = scriptHome + "/" + domainName
        if not os.path.exists(dir):
            os.makedirs(dir)
        feApp = open (dir+"/" + appsDomainInv,"a")
        domainConfig()

        dsCounter = 0
        allJDBCResources = cmo.getJDBCSystemResources()
        for jdbcResource in allJDBCResources:
            dsname = jdbcResource.getName()
            dsResource = jdbcResource.getJDBCResource()
    #        dsServer = dsResource.getJDBCDataSourceParams().getJNDINames()#[0]
            dsJNDIname = dsResource.getJDBCDataSourceParams().getJNDINames()#[0]
            dsInitialCap = dsResource.getJDBCConnectionPoolParams().getInitialCapacity()
            dsMaxCap = dsResource.getJDBCConnectionPoolParams().getMaxCapacity()
            dsParams = dsResource.getJDBCDataSourceParams()
            dsDriver = dsResource.getJDBCDriverParams().getDriverName()
            conn =  dsResource.getJDBCDriverParams().getUrl()
            test = dsResource.getJDBCDriverParams().getProperties()
            test1 = dsResource.getJDBCConnectionPoolParams()
            user = ''
            readTimeOut = ''
            conTimeOut = ''
            streamAsBlob = ''
            print 'FOR'

            timeStamping = Date()
            timeToShow = DateFormat.getDateTimeInstance(DateFormat.SHORT,DateFormat.SHORT).format(timeStamping);

            infoLineForDBDetails = str(dsname) + "|" + str(dsResource) + "|" + str(dsJNDIname) + "|" + str(dsParams) + "|" + str(dsDriver) + "|" + str(conn) + "|" + str(test1) + "\n"
            print(infoLineForDBDetails)
            dbs = open (dir+"/" + dataSourcersDomainInv,"a")
            dbs.write(infoLineForDBDetails)
            dbs.close()

            dsCounter +=1
        try :
            user = get("/JDBCSystemResources/"+ dsname +"/Resource/" + dsname + "/JDBCDriverParams/" + dsname + "/Properties/" + dsname + "/Properties/user/Value")
            readTimeOut = get("/JDBCSystemResources/"+ dsname +"/Resource/" + dsname + "/JDBCDriverParams/" + dsname + "/Properties/" + dsname + "/Properties/oracle.jdbc.ReadTimeout/Value")
            conTimeOut = get("/JDBCSystemResources/"+ dsname +"/Resource/" + dsname + "/JDBCDriverParams/" + dsname + "/Properties/" + dsname + "/Properties/oracle.net.CONNECT_TIMEOUT/Value")
            streamAsBlob = get("/JDBCSystemResources/"+ dsname +"/Resource/" + dsname + "/JDBCDriverParams/" + dsname + "/Properties/" + dsname + "/Properties/SendStreamAsBlob/Value")


        except Exception, e:
            fe = open (pathConnectionProblems,"a")
            errorLineToWrite = url + "," + username + "," + password + "," + str(e) + "\n"
            fe.write(errorLineToWrite)
            fe.close
        vasApps = cmo.getAppDeployments()
        for app in vasApps:
            appName = app.getName()
            targetAppToWrite = ""
            targetsApp = app.getTargets()
            for targetApp in targetsApp:
                targetAppToWrite = targetAppToWrite + "," + targetApp.getName()
            appDataLineToWrite = appName + targetAppToWrite + "\n"
            feApp.write(appDataLineToWrite)
        feApp.close()
        disconnect()
    except Exception, e:
        fe = open (pathConnectionProblems,"a")
        errorLineToWrite = url + "," + username + "," + password + "," + str(e) + "\n"
        fe.write(errorLineToWrite)
        fe.close
        disconnect()

### Begin Inventory Script

getProperties()
fileName = adminsFile
# reading domainsURL CSV
print('Reading File \"' + fileName + '\"' )
f = open(fileName)

for line in f.readlines():
### Strip the comment lines
    if line.strip().startswith('#'):
        continue
    else:
    ### Split the comma separated values
        items = line.split(',')
        items = [item.strip() for item in items]
        if len(items) != 3:
            print "==>Bad line: %s" % line
            print "==>Syntax: AdminServerURL,User,Password"
        else:
            (adminServerAddress, adminUser, adminPassword) = items
            getBasicInformation()

exit()
