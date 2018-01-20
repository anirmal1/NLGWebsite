var inpF, hist;
var inpFdefault = "Enter your text here.";

window.onload = setup;

function getResponse(){
  // Pushing prompt to the history
  var prompt = inpF.value;
  if (prompt === inpFdefault || prompt === "")
    return; // show warning message?
  hist = document.getElementById("history");
  hist.innerHTML += `<div class="history user">${prompt}</div>`;
  inpF.value = "";
  console.log([inpF.value]);
  console.log(prompt);

  // Sending stuff to server (for now, no server)
  var nlgResponse = "SWABHA's MY FAVORITE NLPer!";

  //var toSend;
  //if (document.getElementById("separateTalkTurns").checked){
  var toSend = $.trim(prompt).replace(/\n/g,"|||");
  //} else {
  //  toSend = $.trim(hist.innerText).replace(/\n/g,"|||");
  //}


  var xmlHttp = new XMLHttpRequest();
  xmlHttp.onreadystatechange = function() { 
  	if (xmlHttp.readyState == 4 && xmlHttp.status == 200){
      console.log(xmlHttp.responseText);
      nlgResponse = xmlHttp.responseText;
      hist.innerHTML += `<div class="history nlg">${nlgResponse}</div>`;
      hist.innerHTML += `<hr class="removable">`;
      $(".removable").show();
      //checkboxes(document.getElementById("enableDialogue"));
      //checkboxes(document.getElementById("separateTalkTurns"));
    }
  }
	var dimension = getDimensionValue();
  console.log(dimension);
  xmlHttp.open("POST", window.location.href+"?inputText="+toSend+"&dimension="+dimension, true);
  xmlHttp.send();
}

/*
function checkboxes(cb){
	if (cb.id === "enableDialogue"){
		if (cb.checked)
			$(".nlg").addClass("dialogue")
		else
			$(".nlg").removeClass("dialogue")
	} else if (cb.id === "separateTalkTurns" ){
		if (cb.checked)
			$(".removable").show();
		else
			$(".removable").hide();
	}
}
*/

function getDimensionValue() {
	if (document.getElementById('agencyRadio').checked) {
		return document.getElementById('agencyRadio').value;
	}	else {
		return document.getElementById('powerRadio').value;
	}
}

function setup(){
  /*Input field aesthetics*/
  inpF = document.getElementById("inputfield");
  inpF.onfocus = function(){
    if(inpF.value === inpFdefault){
      inpF.style = "color: black;font-style: normal";
      inpF.value = "";
    }
  };
  inpF.onblur = function(){
    if (inpF.value === ""){
      inpF.style = "color: grey;font-style: italic;";
      inpF.value = inpFdefault;
    }
  };
  inpF.onkeyup = function(e){
    if (e.keyCode === 13 && !e.shiftKey){
      getResponse();
    }
  };
}
