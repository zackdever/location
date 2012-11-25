var app = app || {};

(function () {

  // Location Collection
  // -------------------
  app.LocationList = Backbone.Collection.extend({

    url: '/api/locations/',

    model: app.Location,

    comparator: function(location) {
      return location.getTitle().toLowerCase();
    }

  });

})();
