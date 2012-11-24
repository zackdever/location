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
    }

  });

  // Location Collection
  // -------------------
  var LocationList = Backbone.Collection.extend({

    url: '/api/locations/',
    model: Location

  });

  var locations = new LocationList;

  // Location Item View
  // ------------------
  var LocationView = Backbone.View.extend({

    tagName:  'li',

    template: _.template($('#item-template').html()),

    events: {
      'dblclick .view'  : 'edit',
      'click a.destroy' : 'clear',
      'keypress .edit'  : 'updateOnEnter'
    },

    initialize: function() {
      this.model.on('change', this.render, this);
      this.model.on('destroy', this.remove, this);
    },

    render: function() {
      this.$el.html(this.template(this.model.toJSON()));
      this.input_name = this.$('.name');
      this.input_address = this.$('.address');
      this.input_lat = this.$('.lat');
      this.input_lng = this.$('.lng');
      return this;
    },

    // Switch this view into `"editing"` mode, displaying the input field.
    edit: function() {
      this.$el.addClass('editing');
      this.input_name.focus();
    },

    // Close the `"editing"` mode, saving changes to the location.
    close: function() {
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

      this.$el.removeClass('editing');
    },

    // If you hit `enter`, we're through editing the item.
    updateOnEnter: function(e) {
      if (e.keyCode == 13) this.close();
    },

    // Remove the item, destroy the model.
    clear: function() {
      this.model.destroy();
    }

  });

  // The Application
  // ---------------

  // Our overall **AppView** is the top-level piece of UI.
  var AppView = Backbone.View.extend({

    // Instead of generating a new element, bind to the existing skeleton of
    // the App already present in the HTML.
    el: $('#app'),

    events: {
      'keypress #new-location':  'createOnEnter'
    },

    // At initialization we bind to the relevant events on the `Location`
    // collection, when items are added or changed. Kick things off by
    // loading any preexisting locations.
    initialize: function() {

      this.input = this.$('#new-location');

      locations.on('add', this.addOne, this);
      locations.on('reset', this.addAll, this);
      locations.on('all', this.render, this);

      this.footer = this.$('footer');
      this.main = $('#main');

      locations.fetch();
      this.input.focus();
    },

    render: function() {
      if (locations.length) {
        this.main.show();
      } else {
        this.main.hide();
      }
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
    },

    // If you hit return in the main input field, create new **location** model,
    // and save it.
    createOnEnter: function(e) {
      if (e.keyCode != 13) return;
      if (!this.input.val()) return;

      locations.create({ address: this.input.val() }, {
        'error': _.bind(function (model, xhr, options) {
          console.log('notify user, rollback changes, yada yada');
        }, this)
      });

      this.input.val('');
    }

  });

  // Finally, we kick things off by creating the **App**.
  var App = new AppView;

});
