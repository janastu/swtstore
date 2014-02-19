var sweet = {
  // takes in sweet store URL and username and password and a success callback
  // and an error callback,
  // and authenticates the user with the given sweet store.
  // If the user is authenticated, the callback is executed, passing in the
  // response from sweet store. Else, the error cb is executed.
	authenticate: function(url, user, hash, cb, errorCb) {
    // assuming jquery is available
    // TODO: fix this
    $.ajax({
      url: url,
      type: 'POST',
      data: {'user': user, 'hash': hash},
      success: function(data, textStatus) {
        cb(data);
      },
      error: function(jqxhr, textStatus, error) {
        alert('Authentication failed! Please check your username and password');
        console.log(error, textStatus);
        errorCb(textStatus, error);
      }
    });
	}
};
