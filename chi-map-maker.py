# Import modules.
import requests
import numpy as np
import pandas as pd
import geopandas as gpd
from shapely import geometry
import matplotlib.pyplot as plt


# Get shapefile for Chicago community areas.
def get_outlines():
  url = "https://data.cityofchicago.org/resource/igwz-8jzy.json"
  response = requests.get(url)

  df = pd.DataFrame(response.json())
  df["geom"] = df["the_geom"].apply(lambda x: geometry.shape(x))
  outlines_gdf = gpd.GeoDataFrame(df, geometry="geom", crs="EPSG:4326")
  return outlines_gdf


# Get coordinates for each location.
def get_points(query, outlines):
  url = "https://nominatim.openstreetmap.org/search?"
  payload = {
      "q" : query + ", Chicago IL", 
      "addressdetails" : 1, 
      "format" : "json", 
      "limit" : 50}
  response = requests.get(url, params=payload)
  df = pd.DataFrame(response.json())
  
  if len(df.index) == 0:
    return None

  elif len(df.index) == 50:
    print("Initial API response contained 50 results. "
          + "Implementing tiled search.") 
    tiles = create_tiles(query, outlines)
    tiled_df = pd.DataFrame()

    for i, tile in enumerate(tiles):
      print(
      "\rProcessing tile " + 
      str(i + 1) + " of " + 
      str(len(tiles.index)) + "...", 
      end="")

      tile_minx, tile_miny, tile_maxx, tile_maxy = tile.bounds
      viewbox = [
      str(tile_minx) + ", " 
      + str(tile_miny) + ", " 
      + str(tile_maxx) + ", " 
      + str(tile_maxy)
      ]
      payload["viewbox"] = viewbox
      payload["bounded"] = 1
      tiled_response = requests.get(url, params=payload)

      if len(tiled_response.json()) == 50:
          print("WARNING: Tile(s) hit the API results limit. "
                + "Increase tile_count to avoid missing data.")
                
      tiled_df = pd.concat([
          tiled_df, 
          pd.DataFrame(tiled_response.json())
      ])
      
    tiled_df = tiled_df[tiled_df["address"].apply(
        lambda x: x.get('city',"")) == "Chicago"]
    tiled_df.drop_duplicates(subset=["place_id"], inplace=True)
    tiled_df.drop_duplicates(subset=["display_name"], inplace=True)
    tiled_gdf = gpd.GeoDataFrame(
        tiled_df, 
        geometry=gpd.points_from_xy(tiled_df["lon"], tiled_df["lat"]), 
        crs="EPSG:4326"
        )
    print("\r", end="")
    return tiled_gdf

  else: 
    df = df[df["address"].apply(lambda x: x.get("city","")) == "Chicago"] 
    points_gdf = gpd.GeoDataFrame(
        df,
        geometry=gpd.points_from_xy(df["lon"], df["lat"]), 
        crs="EPSG:4326"
        ) 
    return points_gdf

# If too many results for one API call, break geography into tiles.
def create_tiles(query, outlines):
  minx, miny, maxx, maxy = outlines.unary_union.bounds

  tile_count = 81
  tile_sqrt = round(np.sqrt(tile_count))
  gx = np.linspace(minx, maxx, tile_sqrt)
  gy = np.linspace(miny, maxy, tile_sqrt)
  grid = []

  for i in range(len(gx)-1):
    for j in range(len(gy)-1):
      poly_ij = geometry.Polygon([
          [gx[i],gy[j]],
          [gx[i],gy[j+1]],
          [gx[i+1],gy[j+1]],
          [gx[i+1],gy[j]]
          ])  
      grid.append(poly_ij)

  grid_gdf = gpd.GeoDataFrame(grid, geometry=0)
  grid_gdf = grid_gdf[grid_gdf.intersects(outlines.unary_union) == True][0]

  return grid_gdf


# Plot geodata.
def plot_map(query, outlines, points):
  fig, ax = plt.subplots(figsize = (12, 12))
  ax.axis("off")

  outlines.plot(
      ax=ax, 
      facecolor="none", 
      edgecolor="#878787"
      )
  
  points.plot(
      ax=ax, 
      color="red", 
      edgecolor="black", 
      alpha=0.8
      )

  plt.savefig(query + ".png", bbox_inches="tight")


def main():
  query = input('Input your search query (e.g., Lou Malnati\'s): ')

  outlines_gdf = get_outlines()
  points_gdf = get_points(query, outlines_gdf)
  if points_gdf is None:
    print("ERROR: API returned no results. Please try a different query.")
  else:
    plot_map(query, outlines_gdf, points_gdf)
    

main()