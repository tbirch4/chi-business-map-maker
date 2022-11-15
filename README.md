# Chicago Company Map Maker 🗺️

Create a map of Chicago locations for any company.

Function `make_map` takes a company name and outputs a map file using data from [OpenStreetsMap](https://wiki.openstreetmap.org/wiki/Nominatim) and the [Chicago Data Portal](https://data.cityofchicago.org/). Open `chi_map_maker_example.ipynb` in Colab to create your own map!

Note: OpenStreetsMap queries may require some trial and error. If ran successfully, the script will output a .csv containing all query results; review and iterate if necessary. For example:

  * `Lou Malnatis` returns no results, but `Lou Malnati's` returns 10. 
  
  * Results for `Whole Foods` include the company's Pullman distribution center, but the `Whole Foods Market` results do not.
