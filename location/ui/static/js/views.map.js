var app = app || {};

(function() {

  // Map View
  // --------
  // A google maps view. Because the google maps is too slow to load,
  // we just refer to the same MapView instance in the main AppView
  // rather than destroying/creating when the model changes.
  app.MapView = Backbone.View.extend({
    options : {
      center    : new google.maps.LatLng(20, -95),
      mapTypeId : google.maps.MapTypeId.ROADMAP,
      zoom      : 1,
      styles    : [{
        featureType : 'all',
        stylers     : [{
          saturation : -50
        }]
      }]
    },

    el : document.getElementById('map'),

    // Google objects are a bit weird in Backbone,
    // b/c they are their own MVC object.
    initialize: function() {
      this.map = new google.maps.Map(this.el, this.options);
    },

    // Automatically zoom/pan map to fit all Locations.
    fitToLocations : function() {
      var bounds = new google.maps.LatLngBounds();

      if (app.Locations.length) {
        app.Locations.each(function(location) {
          bounds.extend(location.getLocation());
        });

        this.map.fitBounds(bounds);
      } else {
        this.showWorld();
      }
    },

    // Show the entire world!
    showWorld: function() {
      this.map.setCenter(this.options.center);
      this.map.setZoom(1);
    },

    // Zoom map to this specific position.
    zoomTo: function(position) {
      this.map.setCenter(position);
      this.map.setZoom(16);
    },

    // Aliases fitToLocations.
    render : function() {
      this.fitToLocations();
    }
  });
})();
