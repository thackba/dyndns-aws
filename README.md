# DynDNS AWS

Dies ist ein kleines Beispiel für ein DynDNS-System, das auf der AWS-Cloud 
deployed werden kann. Es besteht aus einer Python
[Lambda-Function](https://aws.amazon.com/de/lambda/), die über ein 
[API-Gateway](https://aws.amazon.com/de/api-gateway/) aufgerufen
werden kann.

Die Cloud-Ressourcen werden mit Hilfe des [CDKs](https://aws.amazon.com/de/cdk/) angelegt.
Ist CDK installier, kann man das Ressourcen mit `make deploy` anlegen. 

In der Datei `cdk/lib/names.ts` wird der Domainname definiert, der genutzt werden soll.

Wenn jemand das liest und Fragen hat: Schickt mir doch einfach eine Nachricht. :)