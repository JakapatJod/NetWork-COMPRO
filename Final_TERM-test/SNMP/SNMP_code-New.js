const express = require('express');
const { Session } = require('snmp-native');

const app = express();
const port = 2000;
const ip_add = '192.168.1.21';
const community = 'private';

function createSession() {
  return new Session({ host: ip_add, community: community });
}

function closeSessionAndCallback(session, callback, error) {
  session.close();
  callback(error);
}

function managePort(portNumber, action, callback) {
  const session = createSession();
  const oid = [1, 3, 6, 1, 2, 1, 2, 2, 1, 7, portNumber];
  const type = 2;

  session.set({ oid, value: action, type }, (error) => {
    closeSessionAndCallback(session, callback, error);
  });
}

function getPortInfo(oid, callback) {
  const session = createSession();

  session.getSubtree({ oid }, (error, varbinds) => {
    const portData = {};

    for (const varbind of varbinds) {
      const portNumber = varbind.oid[varbind.oid.length - 1];
      portData[portNumber] = varbind.value;
    }

    closeSessionAndCallback(session, () => {
      if (error) {
        callback(error, null);
      } else {
        callback(null, portData);
      }
    }, null);
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
  getPortInfo([1, 3, 6, 1, 2, 1, 2, 2, 1, 7], (error, portStatus) => {
    if (error) {
      res.status(500).send(`Error fetching port data: ${error.message}`);
    } else {
      getPortInfo([1, 3, 6, 1, 2, 1, 2, 2, 1, 2], (nameError, portName) => {
        if (nameError) {
          res.status(500).send(`Error fetching port names: ${nameError.message}`);
        } else {
          const html = `
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
                        <td class="status-${status === 1 ? 'up' : 'down'}">${status === 1 ? 'Up' : 'Down'}</td>
                        <td>
                          <a href="/open/${portNumber}">เปิด</a> |
                          <a href="/close/${portNumber}">ปิด</a>
                        </td>
                      </tr>
                    `).join('')}
                </table>
              </body>
            </html>
          `;
          res.send(html);
        }
      });
    }
  });
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
