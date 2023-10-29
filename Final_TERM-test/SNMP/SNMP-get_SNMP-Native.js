const snmp = require('snmp-native');

const session = new snmp.Session({ host: '192.168.1.100', community: 'public' });

const oid = [1, 3, 6, 1, 2, 1, 2, 2, 1, 2, 4];

session.get({ oid }, (error, varbinds) => {
  if (!error) {
    const varbind = varbinds[0];
    console.log(`OID: ${varbind.oid.join('.')}`);
    console.log(`Value: ${varbind.value}`);
  } else {
    console.error(`Error: ${error}`);
  }

  session.close();
});
