var app = app || {};

(function () {

  // Location Item View
  // ------------------
  app.LocationView = Backbone.View.extend({

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
        map : app.i.mapView.map,
        place : location
      });

      app.i.mapView.zoomTo(location);

      this.model.on('change', this.render, this);
      this.model.on('change:lat change:lng', this.focusMapToSelf, this);
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
        app.i.mapView.zoomTo(this.marker.getPosition());
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
      this.model.destroy();
      app.i.mapView.render();
    }
  });

})();

