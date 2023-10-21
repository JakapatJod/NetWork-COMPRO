const snmp = require('snmp-native');

const trapReceiver = '192.168.1.100';
const trapPort = 162; 
const communityString = 'public'; 

const trapOid = '1.3.6.1.6.3.1.1.5.1'; 

const session = new snmp.Session({ host: trapReceiver, port: trapPort, community: communityString });

const trapPDU = {
  oid: trapOid,
  type: snmp.PDU.Trap,
  enterprise: '1.3.6.1.4.1.12345', 
  variables: [
    { oid: '1.3.6.1.2.1.1.1.0', type: snmp.ObjectType.OctetString, value: 'SNMP Trap Test' },
  ],
};

// Send the trap
session.trap(trapPDU, (error) => {
  if (error) {
    console.error('Error sending SNMP trap:', error);
  } else {
    console.log('SNMP trap sent successfully');
  }

  // Close the SNMP session
  session.close();
});
