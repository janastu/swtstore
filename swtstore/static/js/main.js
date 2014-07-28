(function(ss) {

  ss.init = function() {
    this.attachLogin();
    this.attachLogout();
    this.initPersona();
    this.activeNav();
    $('.edit-sweet').click(ss.editSweet);
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

  ss.editSweet = function(event) {
    event.preventDefault();
    var target = $(event.currentTarget).attr('for');
    var how = JSON.parse($(event.currentTarget).siblings('.how').html());
    //console.log(how);
    // update sweet function
    function updateSweet(event) {
      var changed = false;
      for(var field in how) {
        var data = $('#edit-sweet-modal .modal-body textarea[name="'+field+'"]').val();
        var item = (typeof how[field] === 'object') ? JSON.stringify(how[field]) :
          how[field];
        if(data !== item) {
          changed = true;
          how[field] = data;
          console.log('Updated '+ field + ' with data: ', data);
        }
      }
      if(changed) {
        $('#save-edited-sweet').text('Saving Changes');

        $.ajax({
          type: 'PUT',
          url: '/api/sweets/'+target,
          contentType: 'application/json',
          data: JSON.stringify(how),
          success: function(data) {
            console.log('Updated swt from the server ', data);
            $('#save-edited-sweet').text('Save Changes');
            $('#edit-sweet-modal').modal('hide');
          },
          error: function() {
            $('#save-edited-sweet').text('Save Changes');
          }
        });
      }
      else {
        return;
      }
    }
    // prepare the edit view
    $('#edit-sweet-modal .modal-body').html('');
    for(var field in how) {
      var item = (typeof how[field] === 'object') ? JSON.stringify(how[field]) :
        how[field];

      $('#edit-sweet-modal .modal-body').append('<div class="form-group"> <b>'+
          field+'</b>');
      /*$('<input>',
          {name: field, value: item, class: 'form-control', type: 'text'}).
        appendTo('#edit-sweet-modal .modal-body');*/
      $('#edit-sweet-modal .modal-body').append('<textarea name="'+field+'" class="form-control">'+item+'</textarea>');

      $('#edit-sweet-modal').append('</div>');
    }
    // launch the modal
    $('#edit-sweet-modal').modal();

    // attach event handlers
    $('#save-edited-sweet').off('click');
    $('#save-edited-sweet').on('click', updateSweet);

  };

})(ss);
