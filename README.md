# Chicago Company Map Maker 🗺️

Create a map of Chicago locations for any company.

Open the `chi_map_maker.ipynb` notebook in Colab, replace the `query` text with your desired company name, and run all cells. The notebook will output a map file using data from [OpenStreetsMap](https://wiki.openstreetmap.org/wiki/Nominatim) and the [Chicago Data Portal](https://data.cityofchicago.org/). 

Note that OpenStreetsMap queries can be unforgiving and may require some trial and error. For example, `Lou Malnatis` returns no results, but `Lou Malnati's` returns 10. Results for `Whole Foods` include the company's Pullman distribution center, but the `Whole Foods Market` results do not. Check the cell outputs for a full list of query results, then iterate as needed.
