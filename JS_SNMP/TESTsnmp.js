const snmp = require('net-snmp');

const target = '192.168.1.100';
const community = 'private';

const portToDisable = 3;

const session = snmp.createSession(target, community);

// Define the correct OID as a string
const oid = `1.3.6.1.2.1.2.2.1.7.${portToDisable}`;
const value = 2; // 2 for disabling the port, 1 for enabling it

const varbinds = [
  { oid, type: snmp.ObjectType.Integer, value }
];

session.set(varbinds, (error, varbinds) => {
  if (error) {
    console.error(`เกิดข้อผิดพลาดในการปิด port ${portToDisable}: ${error}`);
  } else {
    varbinds.forEach((vb) => {
      console.log(`${vb.oid} = ${vb.value}`);
    });
    console.log(`ปิด port ${portToDisable} สำเร็จ`);
  }
  session.close();
});
