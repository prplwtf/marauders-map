# Marauders' map

> [!IMPORTANT]
> I am not responsible for any damages caused by this program or it's users. This is for educational purposes only. You are completely responsible for whatever you do using this program.

<br>
<br>

## Watchtower

Watchtower receives information from [probes](../probe). Initially requiring three probes in a triangle formation, but it may be possible to add more probes for better accuracy.

- Initially three probes, could be expanded upon by adding more probes once implemented in the future.
- Maybe in the future you could calibrate the probes for increased accuracy.

### vs probes

Probes will **not calculate data or communicate with each other**. Probes send their data to Watchtower, which then calculates positions using triangulation.

Watchtower will tell probes it's still alive with every request thats made to it, after 3 failed attempts, probes stop sending data until receiving a start signal.

Watchtower will also be able to send manual stop and start signals, and maybe also request information.

## Probes

Probes will send data to Watchtower. Probes do not communicate with each other, and only communicate to the Watchtower webserver.

Probes will be hosted on a local IP, and will communicate with the Watchtower server. A way to do this more easily would be to set up the network through Tailscale.
