var sweet = {
	authenticate: function(user, hash){
		$.post("http://localhost:5001/authenticate",{"user":user, "hash":hash}, function(data){

			return true;
		});
	}

};