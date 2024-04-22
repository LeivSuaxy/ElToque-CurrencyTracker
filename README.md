# ElToque-CurrencyTracker

<hr/>

## Description:
A script to make requests to the Web API
<a href=https://eltoque.com/ target="_blank">ElToque</a>, which extracts exchange rate information and archives the values in a database.<br/>
It also generates graphs of each established currency on the user's desktop.<br/>
ElToque is a site that records the trend of currency exchange values in Cuba with respect to the national currency (CUP).

### How to use:
<ul>
    <li>You must first request access to the <a href="https://tasas.eltoque.com/docs/" target="_blank">ElToque API</a>, after receiving the token, enter it in the <b>config.json</b> file.</li>
    <li>Create or connect to a database, with a table that has at least 4 columns: ID (Optional), Currency Name, Currency Value, Date. In addition to entering the respective data in the <b>config.json</b></li>
    <li>Once the configurations JSON is configured, you can start the Script.py</li>
</ul>

### Config JSON:

````json
{
  "config":
  {
    "token": "Put your token here", 
    "hour": "Here you put an integer value in the range 0-24 to specify the time the script will be executed"
  },
  "data":
  {
    "user": "Put your user here",
    "password": "Put your password here",
    "host": "Put the database address here",
    "database": "Connect the database",
    "table": "Put the table where you will insert the information"
  },
  "rows":
  {
    "id": "It is not necessary if you have AUTO_INCREMENT in your database.",
    "name": "Column where you will specify the currency.",
    "value": "Column where the currency value will be filed.",
    "date": "Column where you will put the date of registration."
  }
}

````