from pysnmp.hlapi import *

SnmpEngine()

[x for x in dir() if 'Cmd' in x]
getCmd

g = getCmd(SnmpEngine(),
            CommunityData('public'),
            UdpTransportTarget(('demo.snmplabs.com',161)),
            ContextData(),
            ObjectType(objectIdentity=('SNMPv2-MIB','sysDesec')))

