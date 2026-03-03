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
* protein
* carbs
* fats



**Logs**

* id
* user\_id
* device\_id
* food\_id
* weight
* calculated\_calories
* confidence
* timestamp
