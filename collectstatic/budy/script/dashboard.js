var i = j = 0;
var beep1 = new Audio("/media/beep-08b.wav");
var beep2 = new Audio("/media/beep-01a.wav");
function timer(workouts, area) {
	workouts = workouts.split(",");
	timer = setInterval(timer_exec, 1000, workouts);
}

function timer_exec(workouts, time_interval) {
	if ((isNaN(workouts[i])) && (workouts.length > i)) {
		document.getElementById('exercise').innerText = workouts[i];
		i++
		beep1.play();
	}

	else if (workouts.length <= i-1) {
		document.getElementById('exercise').innerText = 'DONE!';
		document.getElementById('timelabel').innerText = '';
		beep1.play();
		beep2.play();
		clearInterval(timer)
	}
	else {
		var duration = workouts[i] - j;
		if (duration >= 0) {
			document.getElementById('timelabel').innerText = duration + ' Next exercise:' + workouts[i+2];
			j++
		}
		else {
			i++
			j=0
			document.getElementById('exercise').innerText = 'REST';
			beep1.play();
		}	
	}

}

