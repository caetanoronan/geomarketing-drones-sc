# quick check for GIS Python bindings
import sys
out = []
try:
    import fiona
    out.append(f"fiona OK {getattr(fiona, '__version__', '')}")
except Exception as e:
    out.append(f"fiona ERROR: {type(e).__name__} {e}")
try:
    from osgeo import ogr
    out.append('osgeo.ogr OK')
except Exception as e:
    out.append(f"osgeo.ogr ERROR: {type(e).__name__} {e}")
try:
    import geopandas as gpd
    out.append(f"geopandas OK {getattr(gpd, '__version__', '')}")
except Exception as e:
    out.append(f"geopandas ERROR: {type(e).__name__} {e}")
print('\n'.join(out))
sys.exit(0)
