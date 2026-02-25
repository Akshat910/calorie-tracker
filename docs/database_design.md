Database table design:



**Users**

* id
* name
* email
* goal\_calories



**Devices**

* device\_id
* user\_id
* location



**Food**

* id
* food\_name
* calories\_per\_100g



**Logs**

* id
* user\_id
* food\_id
* weight
* calories
* confidence
* timestamp
