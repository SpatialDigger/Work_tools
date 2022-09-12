'''
Creates setout points for evaluation trenches adding points at the two shortest ends of each trench
'''

import shapely.wkt
import shapely.geometry
import geopandas as gpd
import numpy as np
import pandas as pd


def rect(polygon, n=None, size=None, tol=0, clip=True, include_poly=False):
    assert (n is None and size is not None) or (n is not None and size is None)

    a, b, c, d = gpd.GeoSeries(polygon).total_bounds
    if not n is None:
        xa = np.linspace(a, c, n + 1)
        ya = np.linspace(b, d, n + 1)
    else:
        xa = np.arange(a, c + 1, size[0])
        ya = np.arange(b, d + 1, size[1])

    # offsets for tolerance
    if tol != 0:
        tol_xa = np.arange(0, tol * len(xa), tol)
        tol_ya = np.arange(0, tol * len(ya), tol)

    else:
        tol_xa = np.zeros(len(xa))
        tol_ya = np.zeros(len(ya))

    # combine placements of x&y with tolerance
    xat = np.repeat(xa, 2)[1:] + np.repeat(tol_xa, 2)[:-1]
    yat = np.repeat(ya, 2)[1:] + np.repeat(tol_ya, 2)[:-1]

    # create a grid
    grid = gpd.GeoSeries(
        [
            shapely.geometry.box(minx, miny, maxx, maxy)
            for minx, maxx in xat[:-1].reshape(len(xa) - 1, 2)
            for miny, maxy in yat[:-1].reshape(len(ya) - 1, 2)
        ]
    )

    # make sure all returned polygons are within boundary
    if clip:
        # grid = grid.loc[grid.within(gpd.GeoSeries(np.repeat([polygon], len(grid))))]
        grid = gpd.sjoin(
            gpd.GeoDataFrame(geometry=grid),
            gpd.GeoDataFrame(geometry=[polygon]),
            how="inner",
            predicate="within",
        )["geometry"]
    # useful for visualisation
    if include_poly:
        grid = pd.concat(
            [
                grid,
                gpd.GeoSeries(
                    polygon.geoms
                    if isinstance(polygon, shapely.geometry.MultiPolygon)
                    else polygon
                ),
            ]
        )
    return grid


# let's test it...
polygon1 = shapely.wkt.loads(
    "POLYGON ((0.0 0.0, 1000.0 0.0, 1000.0 1000.0, 0.0 1000.0,  0.0 0.0))"
)
polygon2 = shapely.wkt.loads(
    "POLYGON ((0.0 0.0, 1000.0 0.0, 1000.0 1000.0, 500.0 2000.0, 0.0 1000.0,  0.0 0.0))"
)

import matplotlib.pyplot as plt
fig, ax = plt.subplots(3, 2, figsize=(16,10))

rect(polygon1, n=8, tol=0).exterior.plot(ax=ax[0,0])
rect(polygon1, n=8, tol=25).exterior.plot(ax=ax[0,1])
rect(polygon2, n=8, tol=25, include_poly=True).exterior.plot(ax=ax[1,0])
rect(polygon2, size=(35, 35), tol=25).exterior.plot(ax=ax[1,1])

# more complex polygon
world = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
bel_4326 = world.loc[world["iso_a3"].eq("BEL"), "geometry"].values[0]
rect(bel_4326, n=20, include_poly=True).exterior.plot(ax=ax[2,0])
# multi-polygon, use UTM so params can be defined in meters
uk = world.loc[world["iso_a3"].eq("GBR"), "geometry"]
uk = uk.to_crs(uk.estimate_utm_crs())
rect(uk.values[0], size=(3*10**4, 4*10**4), tol=10000, include_poly=True).exterior.plot(ax=ax[2,1])


# rect(polygon, n=5, size=50, 2, tol=0, clip=True, include_poly=False)