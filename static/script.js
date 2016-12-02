codeHistory = [];
idx = 0

$("#parse-input").keydown(function(e) {
	if (e.which === 40 || e.which === 38) {
	    if (e.which === 40) {
	    	if (idx < codeHistory.length - 1) {
	    		idx += 1
	    		$("#parse-input").val(codeHistory[idx]);
	    	}
	    	else if (idx === codeHistory.length - 1) {
	    		$("#parse-input").val("");
	    	}
	    }
	    else if (e.which === 38) {
	    	if (idx > 0) {
	    		$("#parse-input").val(codeHistory[idx]);
	    		idx -= 1
	    	}
	    	else if (idx === 0) {
	    		$("#parse-input").val(codeHistory[idx]);
	    	}
	    }
	}
});