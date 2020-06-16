var hiddenfrom = document.createElement("form");
hiddenfrom.classList.add("hiddenbox");
var input = document.createElement("input");
input.type = "text";
input.classList.add("hiddeninput");
input.id = "hiddeninput";
input.setAttribute("oninput", 'valuechange()');
hiddenfrom.appendChild(input);
var title = document.createElement("div");
title.classList.add("title");
title.id = "title";
var msgbox = document.createElement("div");
msgbox.classList.add("msgbox");
msgbox.id = "msgbox";
var message = document.createElement("div");
message.id = "message";
msgbox.appendChild(message);
var echo = document.createElement("p");
echo.classList.add("input");
echo.id = "input";
msgbox.appendChild(echo);
var array = new Array();
var idx = 0;
function recorder(str) {
	idx = array.push(str);
	func(str)
};
function func(str) {
	let node = document.createElement('p');
	node.innerText = str;
	message.appendChild(node);
	msgbox.scrollTo(0, msgbox.scrollHeight - msgbox.clientHeight)
};
function valuechange() {
	echo.innerText = input.value
};
window.onload = function() {
	var Terminalbox = document.getElementById("Terminal");
	Terminalbox.classList.add("content");
	Terminalbox.appendChild(hiddenfrom);
	Terminalbox.appendChild(title);
	Terminalbox.appendChild(msgbox);
	input.focus();
	document.body.onclick = function() {
		input.focus()
	};
	input.onkeydown = function(e) {
		if (e.keyCode == 13) {
			e.preventDefault();
			let str = input.value;
			recorder(str);
			echo.innerText = "";
			input.value = ""
		} else if (e.keyCode == 38) {
			e.preventDefault();
			if (idx > 0) {
				idx = idx - 1;
				echo.innerText = array[idx];
				input.value = array[idx]
			}
		} else if (e.keyCode == 40) {
			e.preventDefault();
			if (idx < array.length - 1) {
				idx = idx + 1 
				echo.innerText = array[idx];
				input.value = array[idx]
			}
		}
	}
}