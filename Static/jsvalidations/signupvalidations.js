$(document).ready(function(){

	let emailerror = passworderror = namerror = phonerror = 0, aadhaarerror = 0
	let email = password = name = phone = aadhaar = ''
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

	function validatename(){
		 name = $("#name").val()
		var nameRegex =/^[^\d]+$/;
		if (name == '' || !name.match(nameRegex)) {
            $('#nameerror').show()
            nameerror = 1
        } else {
            $('#nameerror').hide()
            nameerror = 0
        }

	}

	function validatephone(){
		 phone = $("#phone").val()
		var phoneRegex = /^\d{10}$/;
		if (phone == '' || !phone.match(phoneRegex)) {
            $('#phoneerror').show()
            phoneerror = 1
        } else {
            $('#phoneerror').hide()
            phoneerror = 0
        }
	}
	function validateaadhaar(){
		aadhaar = $("#aadhaar").val()
		var aadhaarRegex = /^[2-9]{1}[0-9]{11}$/;
		if (aadhaar == '' || !aadhaar.match(aadhaarRegex)) {
            $('#aadhaarerror').show()
            aadhaarerror = 1
        } else {
            $('#aadhaarerror').hide()
            aadhaarerror = 0
        }
	}

	$("#email").keyup(function(){
		validateemail()
	})

	$("#password").keyup(function(){
		validatepass()
	})

	$("#name").keyup(function(){
		validatename()
	})

	$("#phone").keyup(function(){
		validatephone()
	})

	$("#aadhaar").keyup(function(){
		validateaadhaar()
	})

	$("#signupbutton").click(function(){
		validateemail()
		validatepass()
		validatename()
		validatephone()
		if (emailerror == 0 && passworderror == 0 && nameerror == 0 && phonerror == 0 && aadhaarerror == 0){
			alert("ready")
		}else{
			return false
		}
	})


	$("#recuitorsignupbutton").click(function(){
		validateemail()
		validatepass()
		validatename()
		validatephone()
		var company = $("#company").val()
		if (emailerror == 0 && passworderror == 0 && nameerror == 0 && phonerror == 0){


			if ($("#otp").val() == ''){

				$.ajax({
					url:"/sendotp", 
					type: "post", 
					dataType: 'json',
					data: {"email":email, "name":name, "phone":phone, "company":company},
					beforeSend: function(){
				        
				    },
				    success: function(output){
				    	$("#otpfield").show()
				    	sendotp = removeNoiseFromOTP(output.out)
				    },
				    error:function(error){
	            		
	            	}
				});

			}else if($("#otp").val() != sendotp){

				$("#otperror").html("The OTP is invalid or expired. Please try again")
				return false

			}else{
				$("#otperror").html("OTP verified successfully.")
				$("#otperror").removeClass("text-warning")
				$("#otperror").removeClass("text-success")
				$.ajax({
						url:"/registerrecuitorRequest", 
						type: "post", 
						dataType: 'json',
						data: {"name":name, "phone":phone, "password":password, "email":email, "company":company},
						beforeSend: function(){
					        
					    },
					    success: function(output){
					    	if (output.status == 'error'){
					    		alertmessage('error', 'Email ID already registered. Please Login')
					    	}else{
					    		alertmessage('success', 'Registered successfully. Please signin to continue')
					    	}
					    },
					    error:function(error){
		            		
		            	}
					});

			}

			
		}else{
			return false
		}
	})

	let sendotp = ''

	$("#employeesignupbutton").click(function(){
		validateemail()
		validatepass()
		validatename()
		validatephone()
		validateaadhaar()
		
		if (emailerror == 0 && passworderror == 0 && nameerror == 0 && phonerror == 0 && aadhaarerror == 0){

			if ($("#otp").val() == ''){
				
			var gender = $("#gender").val()

				$.ajax({
					url:"employees/sendotp", 
					type: "post", 
					dataType: 'json',
					data: {name:name, email:email, password:password, phone:phone, aadhaar:aadhaar, gender: gender},
					beforeSend: function(){
				        
				    },
				    success: function(output){
				    	$("#otpfield").show()
				    	sendotp = removeNoiseFromOTP(output.out)
				    },
				    error:function(error){
	            		
	            	}
				});

			}else if($("#otp").val() != sendotp){

				$("#otperror").html("The OTP is invalid or expired. Please try again")
				return false

			}else{
				$("#otperror").html("OTP verified successfully.")
				$("#otperror").removeClass("text-warning")
				$("#otperror").removeClass("text-success")
				$.ajax({
						url:"/registeremployeeRequest", 
						type: "post", 
						dataType: 'json',
						data: {"name":name, "phone":phone, "password":password, "email":email},
						beforeSend: function(){
					        
					    },
					    success: function(output){
					    	if (output.status == 'error'){
					    		alertmessage('error', 'Email ID already registered. Please Login')
					    	}else{
					    		alertmessage('success', 'Registered successfully. Please signin to continue')
					    	}
					    },
					    error:function(error){
		            		
		            	}
					});

			}
			
		}else{
			return false
		}
	})


	function removeNoiseFromOTP(noisyOTP) {
		return noisyOTP.replace(/\D/g, '');
	}


	


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