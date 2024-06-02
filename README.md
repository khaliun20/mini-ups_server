# Online Order Delivery System 

This is a full-stack online order delivery system modeling UPS completed with 2 other team members for our Server Software course at Duke. I designed and implemented the back end of the project and my teammates worked on the front end! 

## Backend

Tech Used: Python, SQLAlchemy, PostgreSQL, Docker 

### Networking

* Accepts connection requests from Amazon partner.
* Accepts connection requests from clients who made orders on Amazon.
* Connects with the UPS truck inventory server.

### Communication

* Communication protocol is built for Amazon and UPS servers. We used Google protobuf! 

### Database

* We used PostgreSQL to store:
    1. delivery information
    2. communication ACKs

### General Business Logic 

* Receive order delivery requests from Amazon.
* Assign packages to trucks based on availability.
* Update delivery statuses as the deliveries are made and share them with Amazon customers and Amazon. 
   Note: Delivery statuses include "truck assigned", "package picked up from Amazon warehouse", and "on route to client" etc.
* If delivery addresses change, Amazon notifies UPS and delivery is made to the new address.

## Front End

* Amazon customers can log in to UPS to see their order statuses
