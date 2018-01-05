<?xml version="1.0" encoding="ISO-8859-1"?>
<StyledLayerDescriptor version="1.0.0" 
 xsi:schemaLocation="http://www.opengis.net/sld StyledLayerDescriptor.xsd" 
 xmlns="http://www.opengis.net/sld" 
 xmlns:ogc="http://www.opengis.net/ogc" 
 xmlns:xlink="http://www.w3.org/1999/xlink" 
 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <!-- a Named Layer is the basic building block of an SLD document -->
  <NamedLayer>
    <Name>default_raster</Name>
    <UserStyle>
    <!-- Styles can have names, titles and abstracts -->
      <Title>Default Raster</Title>
      <Abstract>A sample style that draws a raster, good for displaying imagery</Abstract>
      <!-- FeatureTypeStyles describe how to render different features -->
      <!-- A FeatureTypeStyle for rendering rasters -->
      <FeatureTypeStyle>
        <Rule>
          <RasterSymbolizer>
            <Opacity>1.0</Opacity>
            <ColorMap type="intervals">
	           <ColorMapEntry color="#FFFFFF" quantity="100" opacity="0.0" label=""/>
	           <ColorMapEntry color="#9666CD" quantity="120" label="1.1 Nature conservation" />
	           <ColorMapEntry color="#C9BEFF" quantity="130" label="1.2 Managed resource protection" />
	           <ColorMapEntry color="#DE87F3" quantity="140" label="1.3 Other minimal use" />
	           <ColorMapEntry color="#FFFFE5" quantity="220" label="2.1 Grazing native vegetation" />
	           <ColorMapEntry color="#298944" quantity="230" label="2.2 Production forestry" />	           
	           <ColorMapEntry color="#ADFFB5" quantity="320" label="3.1 Plantation forestry" />
	           <ColorMapEntry color="#FFD37F" quantity="330" label="3.2 Grazing modified pastures" />
	           <ColorMapEntry color="#FFFF00" quantity="340" label="3.3 Cropping" />
	           <ColorMapEntry color="#AB8778" quantity="350" label="3.4 Perennial horticulture" />
	           <ColorMapEntry color="#573A40" quantity="360" label="3.5 Seasonal horticulture" />
	           <ColorMapEntry color="#000000" quantity="370" label="3.6 Land in transition" />
	           <ColorMapEntry color="#ECFFE0" quantity="420" label="4.1 Irrigated plantation forestry" />
	           <ColorMapEntry color="#FFAA00" quantity="430" label="4.2 Grazing irrigated modified pastures" />
	           <ColorMapEntry color="#C9B854" quantity="440" label="4.3 Irrigated cropping" />
	           <ColorMapEntry color="#9C542E" quantity="450" label="4.4 Irrigated perennial horticulture" />
	           <ColorMapEntry color="#4F2B17" quantity="460" label="4.5 Irrigated seasonal horticulture" />
	           <ColorMapEntry color="#343434" quantity="470" label="4.6 Irrigated land in transition" />
	           <ColorMapEntry color="#FFC9BE" quantity="520" label="5.1 Intensive horticulture" />
	           <ColorMapEntry color="#FF87BE" quantity="530" label="5.2 Intensive animal husbandry" />
	           <ColorMapEntry color="#734C00" quantity="540" label="5.3 Manufacturing and industrial" />
	           <ColorMapEntry color="#FF0000" quantity="542" label="5.4.0, 5.4.1 Urban residential" />
	           <ColorMapEntry color="#9C9C9C" quantity="550" label="5.4.2; 5.4.3; 5.4.4; 5.4.5 Rural residential and farm infrastructure" />
	           <ColorMapEntry color="#9b0000" quantity="560" label="5.5.0 Services" />
	           <ColorMapEntry color="#FF7F7F" quantity="570" label="5.6 Utilities" />
	           <ColorMapEntry color="#A80000" quantity="580" label="5.7 Transport and communication" />
	           <ColorMapEntry color="#47828F" quantity="590" label="5.8 Mining" />
	           <ColorMapEntry color="#294952" quantity="600" label="5.9 Waste treatment and disposal" />
	           <ColorMapEntry color="#0000FF" quantity="620" label="6.1 Lake" />
	           <ColorMapEntry color="#00C5FF" quantity="630" label="6.2 Reservoir/dam" />
	           <ColorMapEntry color="#0070ff" quantity="640" label="6.3 River" />
	           <ColorMapEntry color="#73B2FF" quantity="650" label="6.4 Channel/aqueduct" />
	           <ColorMapEntry color="#73B2FF" quantity="660" label="6.5 Marsh/wetland" />
	           <ColorMapEntry color="#BED2FF" quantity="670" label="6.6 Estuary/coastal waters" />
            </ColorMap>
          </RasterSymbolizer>
        </Rule>
      </FeatureTypeStyle>
    </UserStyle>
  </NamedLayer>
</StyledLayerDescriptor>
