//Constructor
function calendar(id,d,p){
	this.id = id;
	this.dateObject = d;
	this.pix = p;
	this.write = writeCalendar;
	this.length = getLength;
	this.month = d.getMonth();
	this.date = d.getDate();
	this.day = d.getDay();
	this.year = d.getFullYear();
	this.getFormattedDate = getFormattedDate;
	//get the first day of the month's day
	d.setDate(1);
	this.firstDay = d.getDay();
	//then reset the date object to the correct date
	d.setDate(this.date);
}

var days = new Array('Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday');
var months = new Array('January','February','March','April','May','June','July','August','September','October','November','December');

function getFormattedDate(){
	return days[this.day] + ', ' + months[this.month] + ' ' + this.date + ', ' + this.year;
	//return this.month + '/' + this.date + '/' + this.year;
}

function writeCalendar(){
	var calString = '<div id="calContainer">';
	//write month and year at top of table
	calString += '<table id="cal' + this.id + '" cellspacing="0" width="200" style="border:1px black solid;">';
	//write the image – comment out to hide images
	calString += '<tr><th colspan="7"><img src="' + this.pix[this.month].src + '"/></th></tr>';
	//write the month
	calString += '<tr><th colspan="7" class="month">' + months[this.month] + ', ' + this.year + '</th></tr>';
	//write a row containing days of the week
	calString += '<tr>';
	
	for(i=0;i<days.length;i++){
		calString += '<th class="dayHeader">' + days[i].substring(0,3) + '</th>';
	}
	
	//write the body of the calendar
	calString += '<tr>';
	//create 6 rows so that the calendar doesn't resize
	for(j=0;j<42;j++){
		var displayNum = (j-this.firstDay+1);
		if(j<this.firstDay){
			//write the leading empty cells
			calString += '<td class="empty">&nbsp;</td>';
		}else if(displayNum==this.date){
			calString += '<td id="' + this.id +'selected" class="date" onClick="javascript:changeDate(this,\'' + this.id + '\')">' + displayNum + '</td>';
		}else if(displayNum > this.length()){
			//Empty cells at bottom of calendar
			calString += '<td>&nbsp;</td>';
		}else{
			//the rest of the numbered cells
			calString += '<td id="" class="days" onClick="javascript:changeDate(this,\'' + this.id + '\')">' + displayNum + '</td>';
		}
		if(j%7==6){
			calString += '</tr><tr>';
		}
	}
	//close the last number row
	calString += '</tr>';
	//write the nav row
	calString += '<tr>';
	calString += '<td class="nav" style="text-decoration:underline;" onClick="changeMonth(-12,\'' + this.id + '\')">&lt;</td>';
	calString += '<td class="nav" onClick="changeMonth(-1,\'' + this.id + '\')">&lt;</td>';
	calString += '<td class="month" colspan="3">&nbsp;</td>';
	calString += '<td class="nav" onClick="changeMonth(1,\'' + this.id + '\')">&gt;</td>';
	calString += '<td class="nav" style="text-decoration:underline;text-align:right;" onClick="changeMonth(12,\'' + this.id + '\')">&gt;</td>';
	calString += '</tr>';
	
	calString += '</table>';
	calString += '</div>';
	return calString;
}

function getLength(){
	//thirty days has September...
	switch(this.month){
		case 1:
			if((this.dateObject.getFullYear()%4==0&&this.dateObject.getFullYear()%100!=0)||this.dateObject.getFullYear()%400==0)
				return 29; //leap year
			else
				return 28;
		case 3:
			return 30;
		case 5:
			return 30;
		case 8:
			return 30;
		case 10:
			return 30
		default:
			return 31;
	}
}
function changeDate(td,cal){
	//Some JavaScript trickery
	//Change the cal argument to the existing calendar object
	//This is why the first argument in the constructor must match the variable name
	//The cal reference also allows for multiple calendars on a page
	cal = eval(cal);
	document.getElementById(cal.id + "selected").className = "days";
	document.getElementById(cal.id + "selected").id = "";
	td.className = "date";
	td.id = cal.id + "selected";
	//set the calendar object to the new date
	cal.dateObject.setDate(td.firstChild.nodeValue);
	cal = new calendar(cal.id,cal.dateObject,cal.pix);
	//here is where you could react to a date change - I'll just display the formatted date
	alert(cal.getFormattedDate());
}

function changeMonth(mo,cal){
	//more trickery!
	cal = eval(cal);
	//The Date object is smart enough to know that it should roll over in December
	//when going forward and in January when going back
	cal.dateObject.setMonth(cal.dateObject.getMonth() + mo);
	cal = new calendar(cal.id,cal.dateObject,cal.pix);
	cal.formattedDate = cal.getFormattedDate();
	document.getElementById('calContainer').innerHTML = cal.write();
	
}

