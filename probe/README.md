## Probe variations

Probes are quite simple. For them to work they need to correctly communicate with Watchtower, is reachable on the network and have the required wireless chips.

Probes send all devices and their MAC Addresses to Watchtower, every X seconds.

### Goprobe

Goprobe is a Marauders' map probe written in Node.js. You can find Goprobe in the `probe/goprobe` directory.

<br/>
<br/>

## Probe API

Probes can be paired to Watchtower. Once paired, a probe will get an ID and token assigned by Watchtower.

Probes will, while scanning, report to their Watchtower.

### `/adopt`

**REQUIRES PROBE TO BE IN A PAIRING MODE STATE** (all other paths use adoption token in the Authorization header)

The adopt path will allow Watchtower to adopt a node. The probe will log a 6-digit pairing code, that can be used by Watchtower to give it a token and add it to the Watchtower system.

```json
{
  "code": 123456,
  "ip": "192.168.1.15",
  "token": "VERY-SECURE-TOKEN"
}
```

### `/scan/start`

Will start the scanning process. Probes will report back to Watchtower every X seconds. You cannot define the probe frequency.

```json
{}
```

Example response (200)

```json
{
  "status": "probe has started scanning"
}
```

### `/scan/stop`

Will stop the scanning process.

```json
{}
```

Example response (200)

```json
{
  "status": "probe has stopped scanning"
}
```
