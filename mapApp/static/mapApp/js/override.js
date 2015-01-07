// Overrides the default leaflet layer control to allow for checkboxes that control sublayers
L.Control.Layers = L.Control.Layers.extend({
  _onInputClick: function () {
    var inputs = this._form.getElementsByClassName('leaflet-control-layers-selector'), //this is the line changed from the source code, selects by class rather than selecting all input tags
    input, layer, hasLayer;
    var addedLayers = [],
    removedLayers = [];

    this._handlingClick = true;

    for (var i = 0, len = inputs.length; i < len; i++) {
      input = inputs[i];
      layer = this._layers[input.layerId].layer;
      hasLayer = this._map.hasLayer(layer);

      if (input.checked && !hasLayer) {
        addedLayers.push(layer);

      } else if (!input.checked && hasLayer) {
        removedLayers.push(layer);
      }
    }

    // Bugfix issue 2318: Should remove all old layers before readding new ones
    for (i = 0; i < removedLayers.length; i++) {
      this._map.removeLayer(removedLayers[i]);
    }
    for (i = 0; i < addedLayers.length; i++) {
      this._map.addLayer(addedLayers[i]);
    }

    this._handlingClick = false;

    this._refocusOnMap();
  },
});
