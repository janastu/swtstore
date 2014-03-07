(function(ss) {

  ss.init = function() {
    this.attachLogin();
    this.attachLogout();
    this.initPersona();
    this.activeNav();
  };

  ss.activeNav = function() {
    //$('.nav li').removeClass('active');
    // some Javascript foo!!
    var path = window.location.pathname;
    $('.nav li').find('a[href="'+path+'"]').parent().addClass('active');
  };

  ss.attachLogin = function() {
    // check if the login button exists
    if($('#login').length) {
      $('#login').click(function(e) {
        e.preventDefault();
        navigator.id.request();
      });
    }
    //this.initPersona();
  };

  ss.attachLogout = function() {
    // check if the logout button exists
    if($('#logout').length) {
      $('#logout').click(function(e) {
        e.preventDefault();
        navigator.id.logout();
      });
      //this.initPersona();
    }
  };

  ss.initPersona = function() {
    navigator.id.watch({
      loggedInUser: ss.loggedInUser(),
      //when an user logs in
      onlogin: function(assertion) {
        //verify assertion and login the user
        $.ajax({
          type: 'POST',
          url: ss.loginURL(),
          data: {assertion: assertion},
          success: function(data) {
            console.log('successful login..', data);
            window.location.reload();
          },
          error: function() {
            navigator.id.logout();
          }
        });
      },
      onlogout: function() {
        $.ajax({
          type: 'POST',
          url: ss.logoutURL(),
          success: function() {
            window.location.reload();
            console.log('logged out');
          },
          error: function() {
          }
        });
      }
    });
  };

})(ss);
