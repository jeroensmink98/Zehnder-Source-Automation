# CBS Statline Snippets
This document will be used to paste nice CBS Statline API snippets



## Snippets

### Filter
In order to filter something you can add the following after your API url

```py
Perioden?$filter=substring(Key,0,4) ge '2010' and substring(Key,4,2) eq 'JJ'
```

Here "ge" stands for "greater than" and we select the string ```key``` and only want the values that contain 'JJ' since those are the values that are for the entire year.



