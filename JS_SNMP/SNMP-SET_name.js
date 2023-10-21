const snmp = require('net-snmp');

const target = '192.168.1.21';
const community = 'private';
const oid = '1.3.6.1.2.1.1.5.0';
const value = 'Switch4';

const session = snmp.createSession(target, community, { timeout: 5000 }); 

const varbinds = [
  { oid, type: snmp.ObjectType.OctetString, value }
];

session.set(varbinds, (error, varbinds) => {
  if (error) {
    console.error('Error setting SNMP values:', error);
  } else {
    console.log('SNMP set request successful');
    varbinds.forEach((vb) => {
      console.log(`${vb.oid} = ${vb.value}`);
    });
  }
  session.close();
});
