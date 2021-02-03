function init()
{
	var tables = document.getElementsByClassName("editabletable");
	var i;
	for (i = 0; i < tables.length; i++)
	{
		makeTableEditable(tables[i]);
	}
}

function makeTableEditable(table)
{
	var rows = table.rows;
	var r;
	for (r = 0; r < rows.length; r++)
	{
		var cols = rows[r].cells;
		var c;
		for (c = 0; c < cols.length; c++)
		{
			var cell = cols[c];
			var listener = makeEditListener(table, r, c);
            cell.addEventListener('input', listener, false);
		}
	}
}

function makeEditListener(table, row, col)
{
	return function(event)
	{
        var cell = getCellElement(table, row, col);
        var text = cell.innerHTML.replace(/<br>$/, '');
        if(isNaN(text)) {
            if (text=='-'){return;}
            else if (text==','){
                var items = split(text);
		        if (items.length === 1)
		        {
			    // Text is a single element, so do nothing.
			    // Without this each keypress resets the focus.
			    return;
		        }
            }
            else{
                alert("Invalid input!");
                cell.innerHTML=''
            }
        }
        else{
		var items = split(text);
		if (items.length === 1)
		{
			// Text is a single element, so do nothing.
			// Without this each keypress resets the focus.
			return;
		}

		var i;
		var r = row;
		var c = col;
		for (i = 0; i < items.length && r < table.rows.length; i++)
		{
			cell = getCellElement(table, r, c);
			cell.innerHTML = items[i]; // doesn't escape HTML

			c++;
			if (c === table.rows[r].cells.length)
			{
				r++;
				c = 0;
			}
		}
        cell.focus();
        }
	};
}

function getCellElement(table, row, col)
{
	// assume each cell contains a div with the text
	return table.rows[row].cells[col].firstChild;
}

function split(str)
{
	// use comma and whitespace as delimiters
	return str.split(/,|\s|<br>/);
}

init();



//show the data filled into the empTable in the upper original table:
    function showTableData() {
       
       
       //x-value
       
        document.getElementById('info').innerText = "";
        var myTab = document.getElementById('empTable');

        // LOOP THROUGH EACH ROW OF THE TABLE AFTER HEADER.
        for (i = 1; i < myTab.rows.length; i++) {

            // GET THE CELLS COLLECTION OF THE CURRENT ROW.
            var objCells = myTab.rows.item(i).cells.item(0);
                info.innerText = info.innerText + objCells.innerText;
                

            // READ CELL VALUE OF THE CURENT ROW.
            if (i < myTab.rows.length -1){
            info.innerText = info.innerText + ',';     // ADD A Comma
            } else{
            info.innerText = info.innerText;

            }
            info.innerText = info.innerText.split(" ").join(""); 
        }
        document.getElementById('x-values').value = info.innerText; //Write the column content into Data Table



        //y-value
        document.getElementById('info').innerText = "";
        var myTab = document.getElementById('empTable');

        // LOOP THROUGH EACH ROW OF THE TABLE AFTER HEADER.
        for (i = 1; i < myTab.rows.length; i++) {

            // GET THE CELLS COLLECTION OF THE CURRENT ROW.
            var objCells = myTab.rows.item(i).cells.item(1);
                info.innerText = info.innerText + objCells.innerText;
                

            // READ CELL VALUE OF THE CURENT ROW.
            if (i < myTab.rows.length -1){
            info.innerText = info.innerText + ',';     // ADD A Comma
            } else{
            info.innerText = info.innerText;

            }
            info.innerText = info.innerText.split(" ").join(""); 
        }
        document.getElementById('y-values').value = info.innerText; //Write the column content into Data Table
    
    
    
        //Bubblesize
        document.getElementById('info').innerText = "";
        var myTab = document.getElementById('empTable');

        // LOOP THROUGH EACH ROW OF THE TABLE AFTER HEADER.
        for (i = 1; i < myTab.rows.length; i++) {

            // GET THE CELLS COLLECTION OF THE CURRENT ROW.
            var objCells = myTab.rows.item(i).cells.item(2);
                info.innerText = info.innerText + objCells.innerText;
                

            // READ CELL VALUE OF THE CURENT ROW.
            if (i < myTab.rows.length -1){
            info.innerText = info.innerText + ',';     // ADD A Comma
            } else{
            info.innerText = info.innerText;

            }
            info.innerText = info.innerText.split(" ").join(""); 
        }
        document.getElementById('Error-bar').value = info.innerText; //Write the column content into Data Table
       

    }    
    
//showTableData()    

//ADD AND DELETE ROWS!!

function AddRowFunction() {
  var myTab = document.getElementById('empTable');
  var row = myTab.insertRow(myTab.rows.length);
  var cell1 = row.insertCell(0);
  var cell2 = row.insertCell(1);
  var cell3 = row.insertCell(2);
  var cell4 = row.insertCell(3);
  cell1.innerHTML = '<div contenteditable></div>';
  cell2.innerHTML = '<div contenteditable></div>';
  cell3.innerHTML = '<div contenteditable></div>';
  cell4.innerHTML = '<button type="button" class="ibtnDel btn btn-md btn-danger" onclick="myDeleteFunction()">Delete</button>';
}


function myDeleteFunction() {
  var myTab = document.getElementById('empTable');
  document.getElementById('empTable').deleteRow(myTab.rows.length  - 1);
}


function fillmyTable(){
var myTab = document.getElementById('empTable');
//var row = myTab.insertRow(0);
var myX = '{{ mypkX }}';
//alert(myX);
var myXs = myX.split(',');
var myY = '{{ mypkY }}';
var myYs = myY.split(',');
var myError = '{{ mypkError }}';
var myErrors = myError.split(',');

for (var i=0; i< myXs.length; i++) {
    if (i<3){
    var myrow = myTab.rows[i+1];
    
    var cell1 = myrow.cells.item(0);
    var cell2 = myrow.cells.item(1);
    var cell3 = myrow.cells.item(2);
    var cell4 = myrow.cells.item(3);}
    
    else{
    var myrow = myTab.insertRow(i+1);
    var cell1 = myrow.insertCell(0);
    var cell2 = myrow.insertCell(1);
    var cell3 = myrow.insertCell(2);
    var cell4 = myrow.insertCell(3);}
    
    cell1.innerHTML = '<div contenteditable>'+ myXs[i]+'</div>';
    cell2.innerHTML = '<div contenteditable>'+ myYs[i]+'</div>';
    cell3.innerHTML = '<div contenteditable>'+ myErrors[i]+'</div>';    
    cell4.innerHTML = '<button type="button" class="ibtnDel btn btn-md btn-danger" onclick="myDeleteFunction()">Delete</button>';    
    
}
}
   

function SubmitAll(){
showTableData()
//document.getElementById("form1").submit();
document.getElementById('trackme').click();
}

