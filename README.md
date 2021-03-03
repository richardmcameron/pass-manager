# pass-manager
Simple password manager using SQL, tkinger and psycopg2


When a user registeres, a unique identifier is given stored along with the user's credentials. This identifier is used to make a another database with a table that is prefixed with ("accounts_" + user.ID) 

Ex. (accounts_wttxrsswlxraithzjyarqgugqwhlifbebtoudivruwwdmhjrvnlwspxsntukjjrl)

Information is stored in a 1x3 table.

[email/username], [password], [description]


![alt text](https://github.com/richardmcameron/pass-manager/blob/master/ss/26d0a0b6e43bc65f9c89b46b1ff4e753.png?raw=true)

![alt text](https://github.com/richardmcameron/pass-manager/blob/master/ss/b0069a2ca048dd9e107d7853c555dae5.png?raw=true)
