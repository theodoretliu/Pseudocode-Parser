// store the history of inputs
codeHistory = [];
idx = 0

$("#parse-input").keydown(function(e) {
  // if the up or down arrow key is pressed
	if (e.which === 40 || e.which === 38) {
    // if down is pressed, go further in the history if we're not at the end
    if (e.which === 40) {
    	if (idx < codeHistory.length - 1) {
    		idx += 1
        // set the value of the input field to the historical value
    		$("#parse-input").val(codeHistory[idx]);
    	}
    	else if (idx === codeHistory.length - 1) {
    		$("#parse-input").val("");
    	}
    }
    // if up arrow key is pressed, go further back in the history if we're not at the beginning
    else if (e.which === 38) {
    	if (idx > 0) {
        // set the input field to the historical value
    		$("#parse-input").val(codeHistory[idx]);
    		idx -= 1
    	}
    	else if (idx === 0) {
    		$("#parse-input").val(codeHistory[idx]);
    	}
    }
	}
});