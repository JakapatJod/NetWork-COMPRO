const express = require('express');                 // http://localhost:3005
const { Session } = require('snmp-native');0

const app = express();
const port = 3005;
const ip_add = '192.168.1.100'; 
const community = 'private'; 

function managePort(portNumber, action, callback) {
    const session = new Session({ host: ip_add, community: community });
    const oid = [1, 3, 6, 1, 2, 1, 2, 2, 1, 7, portNumber];
  
    // Set the type to INTEGER (2) for SNMP SET operation
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

function getPortStatus(callback) {
  const session = new Session({ host: ip_add, community: community });
  const oid = [1, 3, 6, 1, 2, 1, 2, 2, 1, 2];

  session.getSubtree({ oid }, (error, varbinds) => {
    if (error) {
      callback(error, null);
    } else {
      const portStatus = {};

      for (const varbind of varbinds) {
        const portNumber = varbind.oid[varbind.oid.length - 1];
        const status = varbind.value;
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
      res.send(`
        <html>
          <head>
            <title>SNMP Port Status</title>
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
                    <td>Ethernet${portNumber}</td>
                    <td>${status}</td>
                    <td>
                      <a href="/open/${portNumber}">Open</a> |
                      <a href="/close/${portNumber}">Close</a>
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
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
