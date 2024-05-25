$(document).ready(function(){

	let emailerror = addresserror = nameerror = phoneerror = collegenameerror = courseerror = scoreerror = affilateduniversityerror = academicyearerror = 0 ;

	function validateemail(){
		var email = $("#email").val()
		var emailRegex = /^\b[A-Z0-9._%-]+@[A-Z0-9.-]+\.[A-Z]{2,4}\b$/i;
        if (email == '' || !emailRegex.test(email)) {
            $('#emailerror').show()
            emailerror = 1
        } else {
            $('#emailerror').hide()
            emailerror = 0
        }
	}

	function validatefname(){
		var name = $("#firstname").val()
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
		var phone = $("#phone").val()
		var phoneRegex = /^\d{10,12}$/;
		if (phone == '' || !phone.match(phoneRegex)) {
            $('#phoneerror').show()
            phoneerror = 1
        } else {
            $('#phoneerror').hide()
            phoneerror = 0
        }
	}

	function validateaddress(){
		var address = $("#address").val()
		if (address == '') {
            $('#addresserror').show()
            addresserror = 1
        } else {
            $('#addresserror').hide()
            addresserror = 0
        }
	}




	function validatecollegename(){
		var collegename = $("#collegename").val()
		if (collegename == '') {
	        $('#collegenameerror').show()
	        collegenameerror = 1
	    } else {
	        $('#collegenameerror').hide()
	        collegenameerror = 0
	    }
	}

	function validatescore(){
        var score = $("#score").val()
        if (score == '') {
            $('#scoreerror').show()
            scoreerror = 1
        } else {
            $('#scoreerror').hide()
            scoreerror = 0
        }
    }

	function validateaffilateduniversity(){
        var affilateduniversity = $("#affilateduniversity").val()
        if (affilateduniversity == '') {
            $('#affilateduniversityerror').show()
            affilateduniversityerror = 1
        } else {
            $('#affilateduniversityerror').hide()
            affilateduniversityerror = 0
        }
    }

	function validateacademicyear(){
        var academicyear = $("#academicyear").val()
        if (academicyear == '') {
            $('#academicyearerror').show()
            academicyearerror = 1
        } else {
            $('#academicyearerror').hide()
            academicyearerror = 0
        }
    }

    function validatecourse(){
		var course = $("#course").val()
		if (course == '') {
            $('#courseerror').show()
            courseerror = 1
        } else {
            $('#courseerror').hide()
            courseerror = 0
        }
	}

	


	//Employee
	$("#email").keyup(function(){
		validateemail()
	})
	$("#password").keyup(function(){
		validatepass()
	})
	$("#firstname").keyup(function(){
		validatefname()
	})
	$("#phone").keyup(function(){
		validatephone()
	})
	$("#address").keyup(function(){
		validateaddress()
	})


	//Academic
	$("#academicyear").keyup(function(){
        validateacademicyear()
    })
    $("#collegename").keyup(function(){
        validatecollegename()
    })
    $("#score").keyup(function(){
        validatescore()
    })
    $("#course").keyup(function(){
        validatecourse()
    })
    $("#affilateduniversity").keyup(function(){
        validateaffilateduniversity()
    })

  

	$("#verifybutton").click(function(){
		validateemail()
		validatefname()
		validatephone()
		validateaddress()
		validateacademicyear()
		validatescore()
		validatecollegename()
		validatecourse()

		if (emailerror == 0 && addresserror == 0 && nameerror == 0 && phoneerror == 0 && collegenameerror == 0 && courseerror == 0 && scoreerror == 0 && affilateduniversityerror == 0 && academicyearerror == 0){
			alert("ready")
		}else{
			return false
		}
	})




});