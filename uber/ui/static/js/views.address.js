var app = app || {};

(function () {

  // Address Box View
  app.AddressView = Backbone.View.extend({
    options : {
      types: ['geocode']
    },

    el : document.getElementById('new-location'),

    initialize: function() {
      this.input = $('#new-location');

      this.bindAutoSelectOnEnterOrTab(this.el);
      this.autoComplete = new google.maps.places.Autocomplete(
                            this.el, this.options);

      // events
      google.maps.event.addListener(this.autoComplete, 'place_changed',
                                    _.bind(this.createLocation, this));

      this.input.focus();
    },

    reset : function() {
      this.input.val('');
      this.input.focus();
      this.nameLocationView.close();
      app.i.mapView.fitToLocations();
    },

    createLocation : function() {
      var place = this.autoComplete.getPlace();

      this.model = new app.Location({
        address : this.input.val(),
        lat     : place.geometry.location.lat(),
        lng     : place.geometry.location.lng(),
        name    : ''
      });

      // show it on the map
      app.i.mapView.zoomTo(this.model.getLocation());

      this.model.on('change:name', this.saveLocation, this);
      this.model.on('destroy', this.reset, this);
      this.nameLocationView = new app.NameLocationView({ model: this.model });
      this.nameLocationView.render();
    },

    saveLocation : function() {
      this.model.save(null, {

        'success': _.bind(function (model, response, options) {
          this.model.off('change', this.saveLocation, this);
          app.Locations.push(this.model);
          this.reset();
        }, this),

        'error': _.bind(function (model, xhr, options) {
          console.log('notify user, rollback changes, yada yada');
        }, this)

      });
    },

    // credit: http://stackoverflow.com/a/11703018/962091
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
