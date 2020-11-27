Protection.py ist ein alternatives Script für die X708 USV von Geekworm

Die USV X708 lässt sich über den i2c bus auslesen und liefert als Ergebnis die Batterie Spannung und die Batterie Kapazität

Im automatischen USV Modus (Jumper Reihenfolge beachten), liefert der GPIO17 kein Signal, um festzulegen ob die Netzspannung ausgefallen ist. Dafür sorgt der automatische USV Modus dafur das bei eiber Kapzität von 25% der Raspberry und die USV X708 abgeschaltet werden, bis die Netzspannubg zuruck kehrt.
Diese Funktion ist leider nur sinnvoll für Li-Ion Akkus mit mehr als genug Kapazität für den Raspberry. (Entladungskurve der Akkus beachten!)

In mehreren Versuchen, bemerkte ich, das selbst ein einzelner 18650 LiIon mit rund 3000mAh den Raspberry und mehr versorgt, -inkl. Overclock und Overvoltage.

Bsp.: Die USV X708 versorgt 2 Lüfter und alles was am Raspberry PI 4 2GB angeschlossen ist:

GPIO Pins: 
- Homematic hm-mod-rpi-pcb
- DS18B20 Sensor
- APDS-9960
- 3,5" Paperwhite Display
- ggf. RGB LED
- PWM Steuerung für Lüfter (5V Steuerung über Transistor Schaltung)

USB Ports:
- msata SSD
- USB Dongle
- Deconz Conbee Dongle


Zusätzlich ist der Raspberry übertaktet auf 1875 Mhz mit OverVoltage=4
Der Raspberry startet per USB Boot von der Festplatte und kümmert sich um das ganze IoT Netzwerk (Debmatic, Deconz, Node-Red, Docker, Openhab und vieles mehr kann bei bedarf einfach aktiviert werden, als auch alles parallel lauffähig über Port Mappings, Virtuelle IPs, und Proxy Redirect)



Soviel zum Server - Test System. Es wird also mehr als genug Strom benötigt, um eine einzelne 18650 3000mAh LiIon Zelle zu rechtfertigen, dachte ich!

Daraufhin ebtstannt due erste Version dieses Scripts, mit Logging und LiIon Laufzeit, später dann mit einer annäherubg an die StromVerbrauchs berechnung. Der benötigte Strom kann ungefägr über die Laufzeit und die Shutdown Capacity berechnet werden.
Elektrisch gesehen ist diese StromVerbrauch Rechnung aber eher als "bessere Schätzung zu betrachten, da ich die EntladeKurve der Akkus nicht berücksichtige! Dennoch hilfreich um zu verstehen was der Raspberry mut Zusatz Hardeware so verbraucbt.


Fokgende überlegung ließ mich daran zweifeln ob ein 3000 mAh Akku wirklich notwendug ist:

- Zwei  3000 mAh 18650 Akkus versorgte das gesamte System weit über eine halbe Stubde hinaus!

- Frage: Wenn es zu einem Stromausfall kommt, wie viele Minuten meistens bei einem Stromausfall? - Meistens ist der Strom innerhalb von Sekubden wieder da.... Aber das System ist mein IoT Server, ohne Strom funktiinieren auch die meisten anderen Geräte nicht!

Bedeutet für den benötigten Akku: Ein paar Minuten reichen völlig aus um einen kurzen Ausfall zu überbrücken oder ggf. das gesante System herunter zu fahren und bei aktiver NetzSpannung wieder einzuschalten. Dann sind die Daten immet sicher und kurze unterbrechungen fallen gar nicht auf.


Schlussendlich wird dieses gesamte System von einem mikrigen 560mAh LiIon Akku mit eigener Protectiin versorgt, sollte der Strom mal ausfallen.
Wichtig dafur ist, das Akku mindestens kurzfristig gute 3500 mAh liefern könnte.
Mein verwendeter Akku könnte 20C liefern. Kurzfristig. Also kurzfristig ~ 11200 mA ~ 11A!
Allerdings sorgt die Schztzschaltung im/am Akku dafür, das ich den Akkku nur bis minmal ~66% entladen kann. Danach steht nicht megr genug Strom zur Verfügung und der Raspberry schmirt ab und startet wieder, weil am StartVorgang weniger Strom benötigt wird.
Der Grund ist der ordentliche Stromverbrauch, die Entladungskurve als auch due Schutzschaltung.

Deshalb wurde dieses Script geachrieben, man kann einfach die minimale Kapazität angeben um den Raspberry herunter zu fahren und die USV abzuschalten. Sobald die Netzspannung wieder zurückkehrt, startet das System wieder.
Zusätzlich kann die Akku Kapazität angeben werden, um den Stromverbrauch abzuschätzen.
Natürlich sind auch mehrere Sleep Zeiten definierbar um das Script fast ohne Belastung der CPU laufen zu lassen, - je nachdem wieweit der Akku bereits entladen wurde. Bzw. wird bei voll aufgeladenen Akku, versucht, alle 5s den Verbrauch oder die Aufladung des Akkus festzustellen und den Modus im Script zu wechseln.

Mit einem schön kleinen Akku, verbleibt im X857 Gehäuse mehr als genug Platz für all diese Bauteile. Evtl. könnte dann noch ein Raspberry PI Zero im Gehäuse Platz finden, nebst der ganzen GPIO verdrahtung. Falls due Pins auf dem PI 4 doch nicht ausreichen.
Der kleine 560mAh Akku überlebte jeden noch so verrückren Test, z.B.: Vollständiges System Upgrade. Ein Stresstest mithilfe von StressBerry für 3 Minuten, usw.
Im Normalen Betrieb hält der winzling knapoe 10 Minuten am leben. Danach ist ser Akku bei 70% Kapazität. Noch genug Zeit um den Raspberry in Ruhe herunter zu fahren und abzuschalten.
