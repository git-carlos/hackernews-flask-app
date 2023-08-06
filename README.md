# Full Stack Python Web Application
Constructed by Carlos Pantoja-Malaga & Matthew Kolnicki.

Revisions done by Carlos Pantoja-Malaga for GitHub Repository ```hackernews-flask-app```.

## Description
Semester project for Secure, Parallel, and Distributed with Python. A full stack python web application which utilizes a Gunicorn Python Flask application hosted on an NGINX web server. The web application itself utilizes the HackerNews API to formulate JSON requests and populate a HTML templated page with available news articles. In regard to security, Auth0 has been implemented to allow secure authentication of users on the web application.

For client-side security, the web-application utilizes Auth0 to authenticate users connected to the service. They are unable to access the multiple tabs such as admin or profile on the site unless they are currently present in an Auth0 session. HTTPS is also active on the web-server to allow for secure connection, with HTTP traffic being redirected to HTTPS.
For server-side security, password login through SSH is disabled. Private/Public key login is the only form of allowed login through SSH.  Two-factor authentication through cellular devices is enabled for each of our server-host accounts. We have also whitelisted the IP's for linprog.cs.fsu.edu, allowing ssh connections to the server after first connecting to linprog. Fail2ban has also been added to server to prevent brute for key attacks.

## Project Milestones
|Milestone|Description|
|---|---|
|1|Acquire server instance which operates on Ubuntu 20.04.|
|2|Create administrative users with sudo privelleges.|
|3|Securely connect through SSH utilizing keys, disable password login.|
|4|Install and configure NGINX.|
|5|Install and configure Gunicorn-Flask Application.|
|6|Allow secure traffic to domain through SSL-certification.|
|7|Configure and launch Auth0 to authenticate users.|
|8|Handle populating news.html with JSON-requests from HackerNews API.|
|9|Configure and install SQLLite Database on web-server.|
|10|Handle interaction between web application and SQLLite Database.|
|11|Construct scheme of ordering news articles.|

## Revision Documentation

## Epilogue
