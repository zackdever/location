var app = app || {};

(function () {

  // The Application
  // ---------------

  // Our overall **AppView** is the top-level piece of UI.
  app.AppView = Backbone.View.extend({

    // Instead of generating a new element, bind to the existing skeleton of
    // the App already present in the HTML.
    el: $('#app'),

    // At initialization we bind to the relevant events on the `Location`
    // collection, when items are added or changed. Kick things off by
    // loading any preexisting locations.
    initialize: function() {

      this.mapView = new app.MapView;
      this.addressView = new app.AddressView;

      app.Locations.on('add', this.addOne, this);
      app.Locations.on('reset', this.addAll, this);
      app.Locations.on('all', this.render, this);

      this.footer = this.$('footer');
      this.main = $('#main');

      app.Locations.fetch();
    },

    // Add a single location item to the list by creating a view for it, and
    // appending its element to the `<ul>`.
    addOne: function(location) {
      var view = new app.LocationView({ model: location });
      this.$('#location-list').append(view.render().el);
    },

    // Add all items in the **locations** collection at once.
    addAll: function() {
      app.Locations.each(this.addOne);
      this.mapView.render();
    }
  });

})();
