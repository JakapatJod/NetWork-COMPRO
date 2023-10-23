const snmp = require('snmp-native');

const ciscoContactInfoOid = '1.3.6.1.4.1.9.2.1.61';
const target = '192.168.1.100';
const community = 'public';

const session = new snmp.Session({ host: target, community });

const oids = [ciscoContactInfoOid];

session.getBulk({ oids, nonRepeaters: 0, maxRepetitions: 10 }, (error, varbinds) => {
    if (error) {
        console.error(error);
    } else {
        varbinds.forEach((vb) => {
            console.log(`${vb.oid} = ${vb.value}`);
        });
    }
    session.close();
});
