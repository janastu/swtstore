var sweet = {
	authenticate: function(url,user, hash){
		$.post(url,{"user":user, "hash":hash}, function(data){

			return true;
		});
	}

};