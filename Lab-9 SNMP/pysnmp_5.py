from pysnmp.hlapi import *

communityName = 'public'
ipAddress = '192.168.1.20'
OID = '1.3.6.1.2.1.1.1.0'

errorIndication, errorStatus , errorIndex, varBinds = next(
    nextCmd(SnmpEngine(),
            CommunityData(communityName),
            UdpTransportTarget((ipAddress,161)),
            ContextData(),
            ObjectType(ObjectIdentity(OID)))
)

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
            print('%s = %s' % (name.prettyPrint(), str(val)))