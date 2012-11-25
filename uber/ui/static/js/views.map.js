var app = app || {};

(function() {

  // Map View
  // --------
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

    initialize: function() {
      this.map = new google.maps.Map(this.el, this.options);
    },

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

    showWorld: function() {
      this.map.setCenter(this.options.center);
      this.map.setZoom(1);
    },

    zoomTo: function(position) {
      this.map.setCenter(position);
      this.map.setZoom(16);
    },

    render : function() {
      this.fitToLocations();
    }
  });
})();
