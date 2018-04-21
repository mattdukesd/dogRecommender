
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
  rc = result[0]["Recommendation Score"];
  sx = result[0]["Sex"];
  wt = result[0]["Weight"];

  
  

  document.getElementById("recommended_breed").innerHTML+=" "+breed;


  document.getElementById("recommended_age").innerHTML+=" "+age;
  document.getElementById("recommended_sex").innerHTML+=" "+sx;
  document.getElementById("recommended_weight").innerHTML+=" "+wt;
  document.getElementById("recommended_color").innerHTML+=" "+color;
  document.getElementById("recommended_rec").innerHTML+=" "+rc;
  document.getElementById("recommended_intk_d").innerHTML+=" "+intk_d;
   document.getElementById("recommended_intk_j").innerHTML+=" "+intk_j;
   
  
});

//console.log(data);
//})