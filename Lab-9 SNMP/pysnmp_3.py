#!/usr/bin/env/python3

from pysnmp.entity.rfc3413.oneliner import cmdgen
import datetime

cmdGen = cmdgen.CommandGenerator()

host = '192.168.1.20'
community = 'public'

# Hostname OID
system_name = '1.3.6.1.2.1.1.5.0'

# Interface OID
gig0_0_in_oct = '1.3.6.1.2.1.2.2.1.10.1'
gig0_0_in_uPackets = '1.3.6.1.2.1.2.2.1.11.1'
gig0_0_out_oct = '1.3.6.1.2.1.2.2.1.16.1'
gig0_0_out_uPackets = '1.3.6.1.2.1.2.2.1.17.1'

def snmp_query(host, community , oid):
    errorIndication, errorStatus , errorIndex, varBinds = cmdgen.getCmd(
        cmdgen.CommunityData(community),
        cmdgen.UdpTransportTargent((host,161)),
        oid
    )
    # Check for errors and print out results
    if errorIndication:
        print(errorIndication)
    else:
        if errorStatus:
            print('%s at %s' %(
                errorStatus.prettyPrint(),
                errorIndex and varBinds[int(errorIndex)-1] or '?'
            )
        )
            
        else:
            for name , val in varBinds:
                return(str(val))

result = {}
result['Time'] = datetime.datetime.utcnow().isoformat()
result['hostname'] = snmp_query(host,community,system_name)
result['Gig0-0_In_Octet'] = snmp_query(host,community,gig0_0_in_oct)
result['Gig0-0_In_uPackets'] = snmp_query(host,community,gig0_0_in_uPackets)
result['Gig0-0_Out_Octet'] = snmp_query(host,community,gig0_0_out_oct)
result['Gig0-0_Out_uPackets'] = snmp_query(host,community,gig0_0_out_uPackets)

with open('C:\Users\User\Desktop\NetWork-COMPRO\Lab-9 SNMP\result1.txt') as f:
    f.write(str(result))
    f.write('\n')
