// Load the application once the DOM is ready, using `jQuery.ready`:
$(function(){

    // Location Model
  // --------------
  var Location = Backbone.Model.extend({

    defaults: function() {
      return {
        address: '',
        lat: 0,
        lng: 0,
        name: ''
      };
    },

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

    getLocation: function() {
      return new google.maps.LatLng(this.get('lat'), this.get('lng'));
    },

    getTitle: function() {
      var name = this.get('name');
      return name ? name : this.get('address');
    }

  });

  // Location Collection
  // -------------------
  var LocationList = Backbone.Collection.extend({

    url: '/api/locations/',
    model: Location,

    comparator: function(location) {
      return location.getTitle().toLowerCase();
    }

  });

  var locations = new LocationList;

  // Location Item View
  // ------------------
  var LocationView = Backbone.View.extend({

    tagName:  'li',

    template: _.template($('#item-template').html()),

    events: {
      'click .view'         : 'focusMapToSelf',
      'dblclick .view'      : 'edit',
      'click a.destroy'     : 'clear',
      'keypress .edit'      : 'updateOnEnter',
      'click button.save'   : 'update',
      'click button.cancel' : 'cancel'
    },

    initialize: function() {
      var location = this.model.getLocation();

      this.marker = new google.maps.Marker({
        map : app.mapView.map,
        place : location
      });

      app.mapView.zoomTo(location);

      this.model.on('change', this.render, this);
      this.model.on('destroy', this.remove, this);
    },

    render: function() {
      this._renderTemplate();

      this.input_name = this.$('input.name');
      this.input_address = this.$('input.address');
      this.input_lat = this.$('input.lat');
      this.input_lng = this.$('input.lng');

      this.marker.setPosition(this.model.getLocation());
      this.marker.setTitle(this.model.getTitle());

      return this;
    },

    _renderTemplate: function() {
      this.$el.html(this.template(this.model.toJSON()));
    },

    focusMapToSelf: function() {
      var map = this.marker.getMap();

      // map will be null if we've just deleted it.
      if (map) {
        app.mapView.zoomTo(this.marker.getPosition());
      }
    },

    // Switch this view into `"editing"` mode, displaying the input field.
    edit: function() {
      this.$el.addClass('editing');
      this.input_name.focus();
    },

    // Close the `"editing"` mode, saving changes to the location.
    close: function(save) {
      if (save) {
        var values = {
          name: this.input_name.val(),
          address: this.input_address.val(),
          lat: this.input_lat.val(),
          lng: this.input_lng.val()
        }

        this.model.save(values, {
          'error': _.bind(function (model, xhr, options) {
            console.log('notify user, rollback changes, yada yada');
          }, this)
        });
      } else {
        // undo any changes they may have made
        this._renderTemplate();
      }

      this.$el.removeClass('editing');
    },

    // If you hit `enter`, we're through editing the item.
    updateOnEnter: function(e) {
      if (e.keyCode == 13) this.update();
    },

    update: function(e) {
      this.close(true);
    },

    cancel: function(e) {
      this.close(false);
    },

    // Remove the item, destroy the model.
    clear: function() {
      this.marker.setMap(null);
      app.mapView.render();
      this.model.destroy();
    }

  });

  // Map View
  // --------
  var MapView = Backbone.Model.extend({
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

      locations.each(function(location) {
        bounds.extend(location.getLocation());
      });

      this.map.fitBounds(bounds);
    },

    zoomTo: function(position) {
      this.map.setCenter(position);
      this.map.setZoom(16);
    },

    render : function() {
      this.fitToLocations();
    }

  });

  // Address Box View
  var AddressView = Backbone.Model.extend({
    options : {
      //bounds: ,
      types: ['geocode']
    },

    events: {
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
      //this.autoComplete.unbindAll();
      //this.autoComplete = new google.maps.places.Autocomplete(
                            //this.el, this.options);
    },

    createLocation : function() {
      var place = this.autoComplete.getPlace();
      var data = {
        address: this.input.val(),
        name: '',
        lat: place.geometry.location.lat(),
        lng: place.geometry.location.lng()
      };

      locations.create(data, {
        'error': _.bind(function (model, xhr, options) {
          console.log('notify user, rollback changes, yada yada');
        }, this)
      });

      this.input.val('');
      this.reset();
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

  // The Application
  // ---------------

  // Our overall **AppView** is the top-level piece of UI.
  var AppView = Backbone.View.extend({

    // Instead of generating a new element, bind to the existing skeleton of
    // the App already present in the HTML.
    el: $('#app'),

    // At initialization we bind to the relevant events on the `Location`
    // collection, when items are added or changed. Kick things off by
    // loading any preexisting locations.
    initialize: function() {

      this.mapView = new MapView;
      this.addressView = new AddressView;

      locations.on('add', this.addOne, this);
      locations.on('reset', this.addAll, this);
      locations.on('all', this.render, this);

      this.footer = this.$('footer');
      this.main = $('#main');

      locations.fetch();
    },

    // Add a single location item to the list by creating a view for it, and
    // appending its element to the `<ul>`.
    addOne: function(location) {
      var view = new LocationView({ model: location });
      this.$('#location-list').append(view.render().el);
    },

    // Add all items in the **locations** collection at once.
    addAll: function() {
      locations.each(this.addOne);
      this.mapView.render();
    },


  });

  // Finally, we kick things off by creating the **App**.
  var app = new AppView;

});
