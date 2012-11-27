$(function(){

  // let's start the show...

  // The `i` hack is dirty, but it let's us easily get to
  // the google maps view `app.i.mapView`.
  //
  // We sort of just need to keep it around rather than
  // making/destroying everytime the model changes b/c it's expensive.
  app.i = new app.AppView;

});
