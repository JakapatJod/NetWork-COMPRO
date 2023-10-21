const snmp = require('net-snmp');

const ciscoContactInfoOid = '1.3.6.1.4.1.9.2.1.61.0';
const target = '192.168.1.21';
const community = 'public';
const maxRepetitions = 10; 

const session = snmp.createSession(target, community);

const oids = [ciscoContactInfoOid];
let startIndex = 0;

function doGetBulk() {
    const nextIndex = startIndex + oids.length;

    session.get(oids, (error, varbinds) => {
        if (error) {
            console.error(error);
            session.close();
        } else {
            varbinds.forEach((vb) => {
                console.log(`${vb.oid} = ${vb.value}`);
            });

            if (varbinds.length === maxRepetitions) {
                startIndex = nextIndex;
                doGetBulk(); 
            } else {
                session.close();
            }
        }
    });
}

doGetBulk();
