var app = app || {};

(function () {

  // Name Location View
  app.NameLocationView = Backbone.View.extend({
    el : $('#name-location'),

    template: _.template($('#name-template').html()),

    events: {
      'click .save'    : 'updateName',
      'click .cancel'  : 'cancel',
      'keypress input' : 'updateOnEnter'
    },

    updateOnEnter: function(e) {
      if (e.keyCode == 13) this.updateName();
    },

    initialize: function() {
      this.input = $('#name-location input');
    },

    updateName : function () {
      this.model.set('name', this.input.val());
    },

    render: function () {
      this.$el.html(this.template());
      this.input = $('#name-location input');
      this.input.focus();
      return this;
    },

    cancel: function () {
      this.model.destroy();
    },

    close: function () {
      this.$el.html('');
    }
  });

})();
