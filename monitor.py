
#Conditionally import wlstModule only when script is executed with jython
if __name__ == '__main__': 
    from wlstModule import *#@UnusedWildImport

from ConfigParser import ConfigParser
from java.util import Date
from java.text import DateFormat

def getProperties():
    
    # Declare Properties Parameters
    global adminsFile
    global monitorDomain
    global scriptHome
    global interval
    global maxTimesToMonitor
        
    properties = "general.properties"
    cfg = ConfigParser()
    cfg.read(properties)
    monitorDomain = cfg.get("Files","monitorDomain")
    scriptHome = cfg.get("Runtime","scriptHome")
    adminsFile = cfg.get("Files", "pathDomainsWLS")
    interval = int(cfg.get("Runtime", "monitorIntervalMils"))
    milisecondsToMonitor = float(3600*1000*(float(cfg.get("Runtime","hoursToMonitor"))))
    maxTimesToMonitor = abs(milisecondsToMonitor/interval)
    
def heap_details(server_name):
    
    global hfree
    global hsize
    global hpercent
    global utime
    
    
    cd('ServerRuntimes/'+server_name+'/JVMRuntime/'+server_name)
    hfree = float(get('HeapFreeCurrent'))/1024
    hsize = float(get('HeapSizeCurrent'))/1024
    hpercent = float(get('HeapFreePercent'))
    utime = float(((get('Uptime'))/1000)/60)

    

# definition to print a running servers thread details

def thread_details(server_name):

    global completedRequestCount
    global executeThreadIdleCount
    global executeThreadTotalCount
    global hoggingThreadCount
    global pendingUserRequestCount
    global queueLength
    global standbyThreadCount
    global throughput
    
    cd('ServerRuntimes/'+server_name+'/ThreadPoolRuntime/ThreadPoolRuntime')
    completedRequestCount = float(get('CompletedRequestCount'))
    executeThreadIdleCount = get('ExecuteThreadIdleCount')
    executeThreadTotalCount = get('ExecuteThreadTotalCount')
    hoggingThreadCount = get('HoggingThreadCount')
    pendingUserRequestCount = get('PendingUserRequestCount')
    queueLength = get('QueueLength')
    standbyThreadCount = get('StandbyThreadCount')
    throughput = get('Throughput')



def monitorDomains():
    print 'starting the script for ', adminServerAddress, '....'
    username = adminUser
    password = adminPassword
    url = adminServerAddress 
    try:
        connect(username,password,url)
        
        domainRuntime()
        serverNames = domainRuntimeService.getServerRuntimes() 
        domainName = cmo.getName()
        print 'Getting data from domain ' , domainName
        fileToWrite = scriptHome + "/" + domainName + "/" + monitorDomain
        w = open(fileToWrite,"a")
        for s in serverNames:
            socketsOpenedTotalCount = s.getSocketsOpenedTotalCount()
            heap_details(s.getName())
            thread_details(s.getName())
            # Assign performance data
            
            # write monitor data for this instance jvm to monitorDomain
            timeStamping = Date()
            timeToShow = DateFormat.getDateTimeInstance(DateFormat.SHORT,DateFormat.SHORT).format(timeStamping);
             
            infoLineMonitorData = domainName + "," + timeToShow + "," + s.getName() + "," + str(hfree) + "," + str(hsize)+ "," + str(hpercent) + "," + str(utime) + "," + str(socketsOpenedTotalCount) + "," + str(completedRequestCount) + "," + str(executeThreadIdleCount) + "," + str(executeThreadTotalCount) + "," + str(hoggingThreadCount) + "," + str(pendingUserRequestCount) + "," + str(queueLength) + "," + str(standbyThreadCount) + "," + str(throughput) +"\n"
            w.write(infoLineMonitorData) 
                     
        w.close()
        
        disconnect()
    except Exception, e:
        disconnect()


### Begin Inventory Script

getProperties()
fileName = adminsFile
count = float(0)
while count < maxTimesToMonitor:
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
                monitorDomains()
    java.lang.Thread.sleep(interval)
    count = count + 1
exit()
