var app = app || {};

(function () {

  // Address Box View
  // ----------------
  // Google auto-complete location box set.
  app.AddressView = Backbone.View.extend({

    // only return address location results (not places)
    options : {
      types: ['geocode']
    },

    el : document.getElementById('new-location'),

    // Wire up the google auto-complete to the input box.
    initialize: function() {
      this.input = $('#new-location');

      this.bindAutoSelectOnEnterOrTab(this.el);
      this.autoComplete = new google.maps.places.Autocomplete(
                            this.el, this.options);

      // must use google's own events
      google.maps.event.addListener(this.autoComplete, 'place_changed',
                                    _.bind(this.createLocation, this));

      this.input.focus();
    },

    // Clear any text in the box, close the name location view,
    // and set the map back to showing all locations rather than this one.
    reset : function() {
      this.input.val('');
      this.input.focus();
      this.marker.setMap(null);
      app.i.mapView.fitToLocations();
    },

    // Create a location based on the address in the auto-complete box,
    // display it on the map, and show a form to name and save it.
    createLocation : function() {
      var place = this.autoComplete.getPlace();

      this.model = new app.Location({
        address : this.input.val(),
        lat     : place.geometry.location.lat(),
        lng     : place.geometry.location.lng(),
        name    : ''
      });

      this.model.on('change:name', this.saveLocation, this);
      this.model.on('destroy', this.reset, this);

      var view = new app.NameLocationView({ model: this.model });
      $('#name-location').html(view.render().el);
      $('#name-location input').focus();

      // show it on the map
      var location = this.model.getLocation();
      app.i.mapView.zoomTo(location);

      this.marker = new google.maps.Marker({
        map : app.i.mapView.map,
        position : location
      });
    },

    // Save the location based on the address box to the server.
    saveLocation : function() {
      this.model.save(null, {

        'success': _.bind(function (model, response, options) {
          this.model.off('change', this.saveLocation, this);
          this.model.trigger('sync');
          app.Locations.push(this.model);
          this.reset();
        }, this),

        'error': _.bind(function (model, xhr, options) {
          console.log('notify user, rollback changes, yada yada');
        }, this)

      });
    },

    // credit: http://stackoverflow.com/a/11703018/962091
    //
    // Google's auto-complete box has some annoying tendencies, like
    // not being able to auto-select the first entry, so we make it so.
    bindAutoSelectOnEnterOrTab : function(input) {
      // store the original event binding function
      var _addEventListener = (input.addEventListener) ?
        input.addEventListener : input.attachEvent;

      function addEventListenerWrapper(type, listener) {
        // Simulate a 'down arrow' keypress on hitting 'return' or 'tab'
        // when no pac suggestion is selected, and then trigger the original listener.
        if (type == 'keydown') {
          var orig_listener = listener;
          listener = function(event) {
            var suggestion_selected = $('.pac-item.pac-selected').length > 0;
            if ((event.which == 13 || event.which == 9) && !suggestion_selected) {
              var simulated_downarrow = $.Event('keydown', { keyCode: 40, which: 40 });
              orig_listener.apply(input, [simulated_downarrow]);
            }
            orig_listener.apply(input, [event]);
          };
        }
        _addEventListener.apply(input, [type, listener]);
      }
      input.addEventListener = addEventListenerWrapper;
      input.attachEvent = addEventListenerWrapper;
    }
  });

})();
