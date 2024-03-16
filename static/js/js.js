$(document). ready(function() {

	function validation() {
		err = 0;
		$('.form-control').each(function () {
			if($(this).val() == ''){
				$(this).addClass('is-invalid');
				err = 1
			}else{
				$(this).removeClass('is-invalid');
			}
		})
		if(window.location=='/'){
		if($('#paswd').val() != $('#passagain').val() && $('#paswd').val()!='' && $('#passagain').val()!=''){
			err = 1
			$('#paswd').addClass('is-invalid');
			$('#passagain').addClass('is-invalid');
		}else{
			$('#paswd').removeClass('is-invalid');
			$('#passagain').removeClass('is-invalid');
		}
	}
		if (err){
			return false
		}else{
			return true
		}
		
	}
	$('#reg_btn').on('click',function(){
		if(validation()){
			$.ajax({
			  method: "POST",
			  url: "/ajax/registration",
			  contentType: "application/json",
			  dataType: 'json',
			  data: JSON.stringify({ 
			  	login: $('#login').val(), 
			  	paswd: $('#paswd').val(),
			  	name: $('#name').val(),
			  	surname: $('#surname').val(),
			  	phnumber: $('#phnumber').val(),
			  	mail: $('#mail').val(),
			  }),
			})
			.done(function(result) {
			   window.location.href = '/login'; 
			});
		}
	})
		
	$('#vhod_btn').on('click',function(){
		if(validation()){
			$.ajax({
			  method: "POST",
			  url: "/ajax/login",
			  contentType: "application/json",
			  dataType: 'json',
			  data: JSON.stringify({ 
			  	login: $('#login').val(), 
			  	paswd: $('#paswd').val(),
			  }),
			})
			.done(function(result) {
			    console.log(result)
                if(result.result){
			    	window.location.href = '/shop';
			    }else{
			    	$('#login').addClass('is-invalid');
			    	$('#paswd').addClass('is-invalid');
			    	$('.invalid-feedback').html(result.error);
			    }
			});
		}

	})
}) 
