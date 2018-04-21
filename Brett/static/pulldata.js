
var age,breed,text;
d3.json('/recommended', function(data){
  result = data
  age = result[0]["Age"];
  breed = result[0]["Breed"];
  color = result[0]["Color"];
  id = result[0]["ID"];
  intk_d = result[0]["Intake Date"];
  intk_j = result[0]["Intake Jurisdiction"];
  mpb = result[0]["Mapped_Breed"];

  sx = result[0]["Sex"];
  wt = result[0]["Weight"];
  lk = result[0]["link"];

  
  

  document.getElementById("recommended_breed").innerHTML+=" "+breed;


  document.getElementById("recommended_age").innerHTML+=" "+age;
  document.getElementById("recommended_sex").innerHTML+=" "+sx;
  document.getElementById("recommended_weight").innerHTML+=" "+wt;
  document.getElementById("recommended_color").innerHTML+=" "+color;
  
  document.getElementById("recommended_intk_d").innerHTML+=" "+intk_d;
   document.getElementById("recommended_intk_j").innerHTML+=" "+intk_j;
   document.getElementById("recommended_img").src=" "+lk;
   
  
});

//console.log(data);
//})