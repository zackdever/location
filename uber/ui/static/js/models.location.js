var app = app || {};

(function () {

  // Location Model
  // --------------
  app.Location = Backbone.Model.extend({
    urlRoot: 'api/locations/',

    defaults: function() {
      return {
        address: '',
        lat: 0,
        lng: 0,
        name: ''
      };
    },

    // We're starting with an address, so default everything else in.
    initialize: function() {
      var defaults = this.defaults();

      if (!this.get('lat')) {
        this.set({ 'lat': defaults.lat });
      }
      if (!this.get('lng')) {
        this.set({ 'lng': defaults.lng });
      }
      if (!this.get('name')) {
        this.set({ 'name': defaults.name });
      }
    },

    // Return lat/lng as a google.maps.LatLng object for use with a map.
    getLocation: function() {
      return new google.maps.LatLng(this.get('lat'), this.get('lng'));
    },

    // Determine a title - name if it's set, the address if not.
    getTitle: function() {
      var name = this.get('name');
      return name ? name : this.get('address');
    }

  });
})();
