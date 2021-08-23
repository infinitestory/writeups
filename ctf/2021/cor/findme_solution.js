mqtt = require('mqtt')

const id = 'zwnj0';
const host = 'wss://findme-broker.be.ax';
const will = {
    topic: 'bad',
    payload: 'foo',
    qos: 0,
    retain: true,
}
const client = mqtt.connect(host, { clientId: id, will: will });

// client.on('packetreceive', console.log);
client.on('connect', () => {
    client.on('message', (topic, msg, packet) => {
        console.log('['+topic+'] : '+msg);
    });

    client.subscribe('$SYS/e273cbbe-a7e5-4d3a-a765-811857ecdf0a/new/subscribes')

    /* use this to find broker uuid

    client.subscribe('errors/' + id);
    client.subscribe('messages/' + id + '/normal');
    
    id1 = 'zwnj00';
    client.subscribe('errors/' + id1);
    const client1 = mqtt.connect(host, { clientId: id1, will: will});
    client1.on('connect', () => {
        client1.end(true)
    });
    */
});