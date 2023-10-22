const express = require('express');
const { Session } = require('snmp-native');   // http://localhost:3005

const app = express();
const port = 3005;
const ip_add = '192.168.1.100';
const community = 'private';

function managePort(portNumber, action, callback) {
  const session = new Session({ host: ip_add, community: community });
  const oid = [1, 3, 6, 1, 2, 1, 2, 2, 1, 7, portNumber];
  const type = 2;

  session.set({ oid, value: action, type }, (error) => {
    if (error) {
      callback(error);
    } else {
      callback(null);
    }

    session.close();
  });
}


function getPortName(callbacks) {
  const session = new Session({ host: ip_add, community: community });
  const oid = [1, 3, 6, 1, 2, 1, 2, 2, 1, 2];

  session.getSubtree({ oid }, (error, varbinds) => {
    if (error) {
      callbacks(error, null);
    } else {
      const portstatus = {};

      for (const varbind of varbinds) {
        const portNumber = varbind.oid[varbind.oid.length - 1];
        const status = varbind.value;
        portstatus[portNumber] = status;
      }

      callbacks(null, portstatus);
    }

    session.close();
  });
}





function getPortStatus(callback) {
  const session = new Session({ host: ip_add, community: community });
  const oidStatus = [1, 3, 6, 1, 2, 1, 2, 2, 1, 7]; // OID for port status

  session.getSubtree({ oid: oidStatus }, (error, varbinds) => {
    if (error) {
      callback(error, null);
    } else {
      const portStatus = {};

      for (const varbind of varbinds) {
        const portNumber = varbind.oid[varbind.oid.length - 1];
        const status = varbind.value === 1 ? 'Up' : 'Down';
        portStatus[portNumber] = status;
      }

      callback(null, portStatus);
    }

    session.close();
  });
}

app.get('/open/:portNumber', (req, res) => {
  const portNumber = req.params.portNumber;
  managePort(portNumber, 1, (error) => {
    if (error) {
      res.status(500).send(`Error opening port: ${error.message}`);
    } else {
      res.redirect('/');
    }
  });
});

app.get('/close/:portNumber', (req, res) => {
  const portNumber = req.params.portNumber;
  managePort(portNumber, 2, (error) => {
    if (error) {
      res.status(500).send(`Error closing port: ${error.message}`);
    } else {
      res.redirect('/');
    }
  });
});

app.get('/', (req, res) => {
  getPortStatus((error, portStatus) => {
    if (error) {
      res.status(500).send(`Error fetching port data: ${error.message}`);
    } else {
      // First, get the port names using getPortName
      getPortName((nameError, portName) => {
        if (nameError) {
          res.status(500).send(`Error fetching port names: ${nameError.message}`);
        } else {
          res.send(`
            <html>
              <head>
                <title>SNMP Port Status</title>
                <style>
                  .status-up { color: green; }
                  .status-down { color: red; }
                </style>
              </head>
              <body>
                <h1>SNMP Port Status</h1>
                <table>
                  <tr>
                    <th>Port Name</th>
                    <th>Status</th>
                    <th>Actions</th>
                  </tr>
                  ${Object.entries(portStatus)
                    .map(([portNumber, status]) => `
                      <tr>
                        <td>${portName[portNumber] || 'Port ' + portNumber}</td>
                        <td class="status-${status.toLowerCase()}">${status}</td>
                        <td>
                          <a href="/open/${portNumber}">เปิด</a> |
                          <a href="/close/${portNumber}">ปิด</a>
                        </td>
                      </tr>
                    `)
                    .join('')}
                </table>
              </body>
            </html>
          `);
        }
      });
    }
  });
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
