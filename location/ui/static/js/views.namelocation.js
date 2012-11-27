var app = app || {};

(function () {

  // Name Location View
  // ------------------
  // The view where you can name the location you just typed in.
  app.NameLocationView = Backbone.View.extend({
    tagName: 'div',

    template: _.template($('#name-template').html()),

    events: {
      'click .save'    : 'updateName',
      'click .cancel'  : 'cancel',
      'keypress input' : 'updateOnEnter'
    },

    // If the enter key was pressed, update the name.
    updateOnEnter: function(e) {
      if (e.keyCode == 13) this.updateName();
    },

    initialize: function() {
      this.model.on('destroy sync', this.remove, this);
    },

    // Update the name with the input value.
    updateName : function () {
      this.model.set('name', this.input.val());
    },

    // Render a new template into this el.
    render: function () {
      this.$el.html(this.template());
      this.input = this.$('input');

      return this;
    },

    // Cancel the location naming by destroying the model.
    cancel: function () {
      this.model.destroy();
    },
  });

})();
