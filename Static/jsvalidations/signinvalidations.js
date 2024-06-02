$(document).ready(function(){

	let emailerror = passworderror = 0;
	let email = password = ''
	function validateemail(){
		 email = $("#email").val()
		var emailRegex = /^\b[A-Z0-9._%-]+@[A-Z0-9.-]+\.[A-Z]{2,4}\b$/i;
        if (email == '' || !emailRegex.test(email)) {
            $('#emailerror').show()
            emailerror = 1
        } else {
            $('#emailerror').hide()
            emailerror = 0
        }
	}

	function validatepass(){
		 password = $("#password").val()
		var passwordRegex = /^(?=.*[0-9])(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]{8,}$/;
		if (password == '' || !password.match(passwordRegex)) {
            $('#passworderror').show()
            passworderror = 1
        } else {
            $('#passworderror').hide()
            passworderror = 0
        }

	}

	$("#email").keyup(function(){
		validateemail()
	})

	$("#password").keyup(function(){
		validatepass()
	})

	$("#signinbutton").click(function(){
		validateemail()
		validatepass()
		if (emailerror == 0 && passworderror == 0){
			alert("ready")
		}else{
			return false
		}
	})

	$("#recuitorSigninButton").click(function(){
		validateemail()
		validatepass()
		if (emailerror == 0 && passworderror == 0){
			$.ajax({
				url:"/loginrecuitorRequest", 
				type: "post", 
				dataType: 'json',
				data: {"password":password, "email":email},
				beforeSend: function(){
			        
			    },
			    success: function(output){
			    	if (output.status == 'error'){
			    		alertmessage('error', 'Invalid username or password')
			    	}else{
			    		
			    		if (output == 0){
			    			alertmessage('error', 'Invalid username or password')
			    		}else if(output == 2){
			    			alertmessage('error', 'You can access the system one our admin approved your request')
			    		}else{
			    			location.href="recruitorindex"
			    		}
			    	}
			    },
			    error:function(){
            		
            		alert("Something went wrong! Please try again.")
            	}
			});
		}else{
			return false
		}
	})


	$("#employeeSigninButton").click(function(){
		validateemail()
		validatepass()
		if (emailerror == 0 && passworderror == 0){
			$.ajax({
				url:"/loginemployeeRequest", 
				type: "post", 
				dataType: 'json',
				data: {"password":password, "email":email},
				beforeSend: function(){
			        
			    },
			    success: function(output){
			    	if (output.status == 'error'){
			    		alertmessage('error', 'Invalid username or password')
			    	}else{
			    		location.href="employeeindex"
			    	}
			    },
			    error:function(){
            		
            		alertmessage("Something went wrong! Please try again.")
            	}
			});
		}else{
			return false
		}
	})




	$("#adminsigninbutton").click(function(){
		validateemail()
		validatepass()
		if (emailerror == 0 && passworderror == 0){
			$.ajax({
				url:"/loginadminrequest", 
				type: "post", 
				dataType: 'json',
				data: {"password":password, "email":email},
				beforeSend: function(){
			        
			    },
			    success: function(output){
			    	if (output == 0){
			    		alertmessage('error', 'Invalid username or password')
			    	}else{
			    		location.href="adminindex"
			    	}
			    },
			    error:function(){
            		alertmessage("Something went wrong! Please try again.")
            	}
			});
		}else{
			return false
		}
	})

function alertmessage(type, message){
	if (type == 'success'){
		$('#message').removeClass('text-danger')
		$('#message').addClass('text-success')
	}else{
		$('#message').removeClass('text-success')	
		$('#message').addClass('text-danger')
	}
	$("#message").html(message)
}


});