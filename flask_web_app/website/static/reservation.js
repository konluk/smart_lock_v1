function deleteReservation(resID) {               
    fetch("/deleteReservation", {
         method: "POST",
         body: JSON.stringify({ resID: resID }),
    }).then((_res) => {
         window.location.href = "/home";
    });
}        

$(function() {
    var dt = new Date();
    var date = dt.getDate() + "-" + (dt.getUTCMonth()+1) + "-" + dt.getUTCFullYear();            
    
    usr1.value = date;          
    
    addOption(dt.getDate(), dt.getUTCMonth());
    
    $('.dates #usr1').datepicker({
         'format': 'dd-mm-yyyy',
         'autoclose': true,
         'todayHighlight' : true,
         'startDate' : date                    
    }).on('changeDate', function(e) {
         
         var jsDate = $('#usr1').datepicker('getDate');
         jsDate instanceof Date; // -> true
         
         jsDate.getDate();
         jsDate.getMonth();
         jsDate.getFullYear();

         addOption(jsDate.getDate(),jsDate.getMonth())                    
    });

    function addOption(day,month) {         
         
         var x = document.getElementById("hours");              
         while(x.length != 0){
              var x = document.getElementById("hours");
              x.remove(x.length-1);
              
         }                   

         var x = document.getElementById("hours");
         var option = document.createElement("option");
         option.text = "Vyberte si cas";
         option.value = "";
         option.selected = true;
         option.disabled = true;
         option.hidden = true;
         x.add(option);  

         var dt = new Date();

         for (let i = 0; i < 24; i++) {
              if(i >= dt.getHours() && dt.getDate()==day && dt.getUTCMonth() == month){
                   var x = document.getElementById("hours");
                   var option = document.createElement("option");    
                   var cas = i.toString();   
                   var casplusjeden = i+1;
                   casplusjeden.toString();
                   var celycas = ":00 - " 
                   cas = cas.concat(celycas);
                   cas = cas.concat(casplusjeden);
                   cas = cas.concat(":00");
                   
                   option.text = cas;
                   x.add(option);          
              }
              
              if(dt.getDate() != day || dt.getUTCMonth() != month){
                   var x = document.getElementById("hours");
                   var option = document.createElement("option");    
                   var cas = i.toString();   
                   var casplusjeden = i+1;
                   casplusjeden.toString();
                   var celycas = ":00 - " 
                   cas = cas.concat(celycas);
                   cas = cas.concat(casplusjeden);
                   cas = cas.concat(":00");

                   option.text = cas;
                   x.add(option);          
              }                         
         
         }                   
         
         fetch('/getReservation').then(function(response){
              return response.json();
         }).then(function(obj){                                            
                 
              var i = 1;
              while(1){
                   if(obj[i]==undefined)return;
                   
                   //console.log(i + ". " + obj[i].day);                              
                   var jsDate = $('#usr1').datepicker('getDate');
                   jsDate instanceof Date; // -> true
              
                   if(obj[i].day==jsDate.getDate() && obj[i].month==jsDate.getMonth()+1 && obj[i].year==jsDate.getFullYear()){
                        var op = document.getElementById("hours").getElementsByTagName("option");
                       for (var j = 0; j < op.length; j++) {
                             value = op[j].value.toLowerCase();
                             value = value.split(":")
                             if (parseInt(value[0]) == obj[i].hour) {
                                  op[j].disabled = true;
                                  op[j].style.color = "red"
                             //op[j].style.backgroundColor = "gray"
                             }
                       }
                   }                        
                   i++;
              }      
    })  
    return
    }            
});      