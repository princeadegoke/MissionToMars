var pageList = new Array();
var currentPage = 1;
var resultsPerPage = 50;
var numberofPages = 0;
// Set the dataSet to data intially
var filteredData = dataSet;

// Function to get the total nummber of Pages based on the result
function PageCalculate(list){
  return Math.ceil(list.length/resultsPerPage);
}

// Next page function
function nextPage(){
  if(currentPage<PageCalculate(filteredData)){
  currentPage += 1;
  LoadList();
  }
}

// Previous page function
function previousPage(){
  if(currentPage>1){
  currentPage -= 1;
  LoadList();
  }
}

// First page function
function firstPage(){
  if(currentPage>=1){
  currentPage = 1;
  LoadList();
  }
}

// Last Page function
function lastPage(){
  if(currentPage<=PageCalculate(filteredData)){
  currentPage = PageCalculate(filteredData);
  LoadList();
  } 
}

// Load List Function=>Splitting the results into appropriate pages
function LoadList(){
  console.log(filteredData);
  var begin = ((currentPage-1)*resultsPerPage);
  console.log("Begin index:",begin+1);
  var end = begin + resultsPerPage;
  console.log("End index:",end);
  pageList = filteredData.slice(begin,end);
  console.log(pageList);
  renderTable(pageList);
  numberofPages = PageCalculate(filteredData);
  check();
  console.log("Showing Page "+currentPage + " of " + numberofPages);
  $pageresults.innerText="Showing Page "+currentPage + " of " + numberofPages;
}

// Function to disable the first and previous button if we are on page 1 
// or to diable the next and last button if we are on the last page.
function check(){
  document.getElementById("next").disabled = currentPage==numberofPages ? true:false;
  document.getElementById("previous").disabled = currentPage==1 ? true:false;
  document.getElementById("first").disabled = currentPage==1 ? true:false;
  document.getElementById("last").disabled = currentPage==numberofPages ? true:false;
}

function applyfilters(filteredData){
  var filterDate = $dateInput.value.trim();
    if(filterDate!=""){
      filteredData = filteredData.filter(function(sighting){
        var sightingDate = sighting.datetime;
        return sightingDate===filterDate;
      });
    };

    var filterCity = $cityInput.value.trim().toLowerCase();
    if(filterCity!=""){
      filteredData=filteredData.filter(function(sighting){
        var sightingCity = sighting.city;
        return sightingCity===filterCity;
      });
    };

    var filterState = $stateInput.value.trim().toLowerCase();
    if(filterState!=""){
      filteredData=filteredData.filter(function(sighting){
        var sightingState = sighting.state;
        return sightingState===filterState;
      });
    };

    var filterCountry = $countryInput.value.trim().toLowerCase();
    if(filterCountry!=""){
      filteredData=filteredData.filter(function(sighting){
        var sightingCountry = sighting.country;
        return sightingCountry===filterCountry;
      });
    };

    var filterShape = $shapeInput.value.trim().toLowerCase();
    if(filterShape!=""){
      filteredData=filteredData.filter(function(sighting){
        var sightingShape = sighting.shape;
        return sightingShape===filterShape;
      });
    };

    console.log("Filtered Data: ",filteredData);
    return filteredData;
}

// Get reference for the tbody, input datetime and button element
var $tbody = document.querySelector("tbody");
var $dateInput = document.querySelector("#datetimeInput");
var $cityInput = document.querySelector("#cityInput");
var $stateInput = document.querySelector("#stateInput");
var $countryInput = document.querySelector("#countryInput");
var $shapeInput = document.querySelector("#shapeInput");
var $searchBtn = document.querySelector("#search");
var $resetBtn =  document.querySelector("#reset");
var $pageresults = document.getElementById("pageresult")
function renderTable(dataset){
  console.log("Rendering Table");
  var firstindex = ((currentPage - 1) * resultsPerPage); 
	$tbody.innerHTML="";
  if(dataset.length>0){
    for(var i=0;i<dataset.length;i++){
      var fields=Object.keys(dataset[i]);
      var $row = $tbody.insertRow();
      var rowdata = dataset[i];
      for(var j=0;j<fields.length;j++){
        var field= fields[j];
        var $cell = $row.insertCell(j);
        $cell.innerText = rowdata[field];

      };
    };
  };	
};

function handleSearchButton(event){
  event.preventDefault();
  filteredData=dataSet;
	console.log("Button Clicked Successfully")
  filteredData = applyfilters(filteredData);
  // The new results has to be displayed from Page 1
  currentPage=1;
  LoadList();
};


// Add an event listener for the seach button and call the function upon click
$searchBtn.addEventListener("click",handleSearchButton);

// Add an event listener for the reset button and call the function upon click
$resetBtn.addEventListener("click",function(event){
  event.preventDefault();
  filteredData = dataSet;
  $dateInput.value = "";
  $shapeInput.value ="";
  $cityInput.value = "";
  $stateInput.value = "";
  $countryInput.value = "";
  LoadList();
})
LoadList();